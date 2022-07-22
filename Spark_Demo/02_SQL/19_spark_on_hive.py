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
    # 0. 构建执行环境入口对象SparkSession
    spark = SparkSession.builder.\
        appName("test").\
        master("local[*]").\
        config("spark.sql.shuffle.partitions", 2).\
        config("spark.sql.warehouse.dir", "hdfs://node1:8020/user/hive/warehouse").\
        config("hive.metastore.uris", "thrift://node1:9083").\
        enableHiveSupport().\
        getOrCreate()
    sc = spark.sparkContext

    spark.sql("SELECT * FROM itheima.pay_type").show()


