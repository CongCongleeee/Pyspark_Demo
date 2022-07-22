# ：18_2_udf_udaf
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
    spark = SparkSession.builder.appName("18_2_udf_udaf").master("local[*]"). \
        config("spark.sql.shuffle.partitions", 2). \
        getOrCreate()
    sc = spark.sparkContext

    rdd = sc.parallelize([1,2,3,4,5,6,7,8,9],3).map(lambda x:[x])
    df = rdd.toDF(['num'])

    # DF转化RDD --> rdd1 = df.rdd
    # 折中的方式 就是使用RDD的mapPartitions 算子来完成聚合操作
    # 如果用mapPartitions API 完成UDAF聚合, 一定要单分区
    single_partition_rdd = df.rdd.repartition(1)
    print(single_partition_rdd.collect())

    def process(iter):
        sum_num = 0
        for row in iter:
            sum_num+= row['num']
        # yield sum_num
        return [sum_num]


    print(single_partition_rdd.mapPartitions(process).collect())

