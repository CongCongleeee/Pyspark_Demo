# ：10_sql_SQL
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
    spark = SparkSession.builder.appName("10_sql_SQL").master("local[*]").getOrCreate()
    sc = spark.sparkContext

    df = spark.read.format('csv') \
        .schema('id STRING,name STRING,score INT') \
        .load('./stu_score.txt')

    df.show(truncate=False)

    df.createTempView('stu_score')
    df.createOrReplaceTempView('stu_score2')
    df.createGlobalTempView('stu_score3')

    spark.sql('select name, count(1) from stu_score group by name  ').show()
    spark.sql('select name, count(1) from stu_score2 group by name  ').show()
    spark.sql('select name, count(1) from global_temp.stu_score3 group by name  ').show()



