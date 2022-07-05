# ：09_sql_DSL
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
    spark = SparkSession.builder.appName("09_sql_DSL").master("local[*]").getOrCreate()
    sc = spark.sparkContext

    # df = spark.read.csv(path='./stu_score.txt',sep=',',schema=['id','name','score'])
    df = spark.read.format('csv')\
        .schema('id STRING,name STRING,score INT')\
        .load('./stu_score.txt')
        # .withColumnRenamed("_c0", "id")\
        # .withColumnRenamed("_c1", "name")\
        # .withColumnRenamed("_c2", "score")
    df.show(truncate=False)

    # # 列对象的获取
    # print(df['name'])
    #
    # #select
    # df.select('name','score').show()
    # df.select(['name','score']).show()
    # df.select(df['name'],df['score']).show()

    # #where
    # df.where('score = 97').show()
    # df.where(df['score'] == 97).show()

    # # filter
    # df.filter('score = 99').show()
    # df.filter(df['score'] == 99).show()

    #groupby
    df.groupby('name').count().show()
    df.groupby('name').sum('score').show()
    # df.groupby('name').count().where('name = 语文').show()

