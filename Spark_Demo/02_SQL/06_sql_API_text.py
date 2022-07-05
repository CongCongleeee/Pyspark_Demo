# ：04_sql_create_dataframe4

# coding:utf8
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
import os
from pyspark.sql.types import *

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':

    # 0. 构建执行环境入口对象SparkSession
    spark = SparkSession.builder. \
        appName("test"). \
        master("local[*]"). \
        getOrCreate()
    sc = spark.sparkContext

    # 构建StructType, text数据源, 读取数据的特点是, 将一整行只作为`一个列`读取, 默认列名是value 类型是String
    df = spark.read.format("text"). \
        schema("name STRING"). \
        load("./people.txt")

    df.printSchema()
    df.show()

