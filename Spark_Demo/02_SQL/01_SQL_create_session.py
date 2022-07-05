# ：01_SQL_create

# coding:utf8
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
import os

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    # conf = SparkConf().setAppName('01_SQL_create').setMaster("local[*]")
    # sc = SparkContext(conf=conf)
    # 生成sparkcontext对象
    spark = SparkSession.builder.appName("01_SQL_create").master("local[*]").getOrCreate()
    sc = spark.sparkContext

    #helloworld
    data = spark.read.csv('hdfs://node1/input/stu_score.txt',sep=',',header = False)
    df = data.toDF('id','name','source')
    df.show()
    #查看结构
    df.printSchema()

    #创建临时表
    df.createTempView('score')
    # 表查询
    df.where('name ="语文" ').limit(6).show(truncate=False)

    #sql查询
    spark.sql('select * from score where name = "语文" limit 3 ').show(truncate=False)