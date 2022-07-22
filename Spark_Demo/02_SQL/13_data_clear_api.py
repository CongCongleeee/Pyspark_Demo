# ：13_data_clear_api.py
# coding:utf8
import os
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    spark = SparkSession.builder.appName("13_data_clear_api.py").master("local[*]").getOrCreate()
    sc = spark.sparkContext

    df = spark.read.format('csv').option('sep',';').option('header',True).load('./people.csv')
    # df.show(5)
    # 去重函数  doc=":func:`drop_duplicates` is an alias for :func:`dropDuplicates`.",
    # df.drop_duplicates().show()
    # df.drop_duplicates(['name','job']).show()

    # 去除空值
    # df.dropna().show()
    # df.dropna(how='any',thresh=3,subset= ['name','age','job']).show()
    # df.dropna(how='any',thresh=2,subset= ['name','age']).show()

    #填充空值
    df.fillna('你好').show()
    df.fillna('你好',subset=['job']).show()
    df.fillna({'job':'你好'}).show()

