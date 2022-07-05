# ：11_sql_wordscount
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
    spark = SparkSession.builder.appName("11_sql_wordscount").master("local[*]").getOrCreate()
    sc = spark.sparkContext

    rdd = sc.textFile('./words.txt').flatMap(lambda line: line.split(' ')).map(lambda x: [x])
    # print(rdd.collect())
    df = rdd.toDF(schema=['word'])

    df.createOrReplaceTempView('words')
    # spark.sql('select word, count(word) as cnt from words group by word order by cnt desc').show()

    #DSL
    # df.groupBy('word').count().orderby()
    #提取数据1
    df = spark.read.format('text').schema('word STRING').load('./words.txt')
    # 提取数据 默认列名value
    # df_value = spark.read.format('text').load('./words.txt')
    # df_value.show()

    # 拆分数据 withColumn 参数一 列名 有则替换,无则添加
    df.withColumn('value',F.split(df['word'],' ')).show()
    '''
        +------------+---------------+
        |        word|          value|
        +------------+---------------+
        | hello spark| [hello, spark]|
        |hello hadoop|[hello, hadoop]|
        | hello flink| [hello, flink]|
        +------------+---------------+
    '''
    df2 = df.withColumn('word',F.explode(F.split(df['word'],' ')))
    # df2.show()
    df2.groupBy('word').count().\
        withColumnRenamed('count','cnt').\
        orderBy('cnt',ascending=False).\
        show()


