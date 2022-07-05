# ：05_sql_create_dataframe5_csv

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
    # 生成sparkcontext对象
    spark = SparkSession.builder.appName("04_sql_create_dataframe4").master("local[*]").getOrCreate()
    sc = spark.sparkContext

    df = spark.read.format("csv").\
        option("sep",';').\
        option('header','TRUE').\
        option("encoding", "utf-8").\
        schema("name STRING,age INT,job STRING").\
        load("./people.csv")

    df.printSchema()
    df.show()
