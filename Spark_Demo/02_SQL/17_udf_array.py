# ：17_udf_array
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
    spark = SparkSession.builder.appName("17_udf_array").master("local[*]"). \
        config("spark.sql.shuffle.partitions", 2). \
        getOrCreate()
    sc = spark.sparkContext

    rdd = sc.parallelize([['我 爱 你'],['I Love You']])
    df = rdd.toDF(['content'])
    df.show()
    '''
    +----------+
    |   content|
    +----------+
    |  我 爱 你 |
    |I Love You|
    +----------+
    '''
    def split_str(data):
        return data.split(' ')

    #第一种register
    split_str_udf = spark.udf.register('split_str_udf',split_str,ArrayType(StringType()))
    #执行
    df.select(split_str_udf(df['content'])).show()
    df.createOrReplaceTempView('demo_table')
    spark.sql('select split_str_udf(content) from demo_table').show()

    #第二种
    split_str_udf2 = F.udf(split_str,ArrayType(StringType()))
    df.select(split_str_udf2(df['content'])).show()
