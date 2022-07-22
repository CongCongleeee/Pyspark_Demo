# ：16_udf_create
# coding:utf8
import os
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    spark = SparkSession.builder.appName("16_udf_create").\
        config("spark.sql.shuffle.partitions", 2).\
        master("local[*]").getOrCreate()
    sc = spark.sparkContext

    rdd = sc.parallelize([1,2,3,4,5,6,7,8,9]).zipWithUniqueId()
    # print(rdd.collect())
    df = rdd.toDF(['num','id'])
    df.show()

    # udf类型
    def num_10_fun(data):
        return data*10
    num_10_udf = F.udf(num_10_fun,IntegerType())
    #执行函数
    df.select(num_10_udf(df['num'])).show()

    # udf--register
    num_10_reg_udf = spark.udf.register("num_10_reg_udf_nm",num_10_fun,IntegerType())
    #执行函数
    df.select(num_10_reg_udf(df['num'])).show()
    df.selectExpr("num_10_reg_udf_nm(num)").show()