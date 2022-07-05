# ：DenseVector和sparseVector

# coding:utf8
from pyspark import SparkConf, SparkContext
import os
from pyspark.ml.linalg import DenseVector, Vector
import numpy as np
import scipy.sparse
from pyspark.ml.linalg import Vectors, _convert_to_vector, VectorUDT, DenseVector
from pyspark.sql.functions import udf, col
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType,StructField, StringType, IntegerType


os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    spark = SparkSession.builder.appName("Recommonder").master("local[*]").getOrCreate()
    sc = spark.sparkContext

    df = sc.parallelize(
        [(1, DenseVector([57.0, 1.0, 0.0, 0.0])),
        (2, DenseVector([63.0, float("NaN"), 0.0, 0.0])),
        (3, DenseVector([74.0, 1.0, 3.0, float("NaN")])),
        (4, DenseVector([67.0, float("NaN"), 0.0, 0.0])),
        (5, DenseVector([float("NaN"), 1.0, float("NaN"), float("NaN")])),
        ]).toDF(["id", "features"])

    print(df.show())
    '''
    +---+------------------+
    | id | features |
    +---+------------------+
    | 1 | [57.0, 1.0, 0.0, 0.0] |
    | 2 | [63.0, NaN, 0.0, 0.0] |
    | 3 | [74.0, 1.0, 3.0, NaN] |
    | 4 | [67.0, NaN, 0.0, 0.0] |
    | 5 | [NaN, 1.0, NaN, NaN] |
    +---+------------------+
    '''
    ########################################
    ## DensVector to SparseVector



    def dense_to_sparse(vector):
        return _convert_to_vector(scipy.sparse.csc_matrix(vector.toArray()).T)


    to_sparse = udf(dense_to_sparse, VectorUDT())
    df = df.withColumn("sparse", to_sparse(col("features")))
    print(df.show(truncate=False))
    '''
    +---+------------------+--------------------------------+
    | id | features | sparse |
    +---+------------------+--------------------------------+
    | 1 | [57.0, 1.0, 0.0, 0.0] | (4, [0, 1], [57.0, 1.0]) |
    | 2 | [63.0, NaN, 0.0, 0.0] | (4, [0, 1], [63.0, NaN]) |
    | 3 | [74.0, 1.0, 3.0, NaN] | (4, [0, 1, 2, 3], [74.0, 1.0, 3.0, NaN]) |
    | 4 | [67.0, NaN, 0.0, 0.0] | (4, [0, 1], [67.0, NaN]) |
    | 5 | [NaN, 1.0, NaN, NaN] | (4, [0, 1, 2, 3], [NaN, 1.0, NaN, NaN]) |
    +---+------------------+--------------------------------+
    '''

    ###################################
    ## SparseVector to DenseVector

    def sparse2dense(v):
        return DenseVector(v.toArray())


    s2d = udf(sparse2dense, VectorUDT())

    df = df.withColumn('dense', s2d(col('sparse')))
    df.show()
    '''
    +---+------------------+--------------------------------+------------------+
    | id | features | sparse | dense |
    +---+------------------+--------------------------------+------------------+
    | 1 | [57.0, 1.0, 0.0, 0.0] | (4, [0, 1], [57.0, 1.0]) | [57.0, 1.0, 0.0, 0.0] |
    | 2 | [63.0, NaN, 0.0, 0.0] | (4, [0, 1], [63.0, NaN]) | [63.0, NaN, 0.0, 0.0] |
    | 3 | [74.0, 1.0, 3.0, NaN] | (4, [0, 1, 2, 3], [74.0, 1.0, 3.0, NaN]) | [74.0, 1.0, 3.0, NaN] |
    | 4 | [67.0, NaN, 0.0, 0.0] | (4, [0, 1], [67.0, NaN]) | [67.0, NaN, 0.0, 0.0] |
    | 5 | [NaN, 1.0, NaN, NaN] | (4, [0, 1, 2, 3], [NaN, 1.0, NaN, NaN]) | [NaN, 1.0, NaN, NaN] |
    +---+------------------+--------------------------------+------------------+
    '''
