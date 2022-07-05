# ：07_sql_API_pandas_parquate
# coding:utf8
import os
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pandas as pd

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    spark = SparkSession.builder.appName("07_sql_API_pandas_parquate").master("local[*]").getOrCreate()
    sc = spark.sparkContext

    data = [{'name':'bob','age':18},{'name':'steven','age':20},{'name':'lee','age':23}]
    pdf = pd.DataFrame(data)
    # print(pdf)

    sdf = spark.createDataFrame(pdf)
    sdf.show()

    # 读取parquet数据
    df = spark.read.format('parquet').load('./users.parquet')
    df.printSchema()
    df.show()
