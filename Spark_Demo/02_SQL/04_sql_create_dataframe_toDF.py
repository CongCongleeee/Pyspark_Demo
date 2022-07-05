# ：04_sql_create_dataframe3

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
    # conf = SparkConf().setAppName('04_sql_create_dataframe3').setMaster("local[*]")
    # sc = SparkContext(conf=conf)
    # 生成sparkcontext对象
    spark = SparkSession.builder.appName("04_sql_create_dataframe3").master("local[*]").getOrCreate()
    sc = spark.sparkContext

    rdd = sc.textFile('hdfs://node1:8020/input/people.txt'). \
        map(lambda x: x.split(',')). \
        map(lambda x: (x[0], int(x[1])))

    schema = StructType().add('name', StringType(), nullable=True). \
        add('age', IntegerType(), nullable=False)

    rdd.toDF(schema=['name','age']).show()
    rdd.toDF(schema=schema).show()
