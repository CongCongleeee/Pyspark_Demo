# ：15_df_JDBC
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
    # 0. 构建执行环境入口对象SparkSession
    spark = SparkSession.builder. \
        appName("test"). \
        master("local[*]"). \
        config("spark.sql.shuffle.partitions", 2). \
        getOrCreate()
    sc = spark.sparkContext

    # 1. 读取数据集
    schema = StructType().add("user_id", StringType(), nullable=True). \
        add("movie_id", IntegerType(), nullable=True). \
        add("rank", IntegerType(), nullable=True). \
        add("ts", StringType(), nullable=True)
    df = spark.read.format("csv"). \
        option("sep", "\t"). \
        option("header", False). \
        option("encoding", "utf-8"). \
        schema(schema=schema). \
        load("../data/input/sql/u.data")

    # # 1. 写出df到mysql数据库中
    # df.write.mode("overwrite").\
    #     format("jdbc").\
    #     option("url", "jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true").\
    #     option("dbtable", "movie_data").\
    #     option("user", "root").\
    #     option("password", "2212072ok1").\
    #     save()

    df2 = spark.read.format("jdbc"). \
        option("url", "jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true"). \
        option("dbtable", "movie_data"). \
        option("user", "root"). \
        option("password", "2212072ok1"). \
        load()

    df2.printSchema()
    df2.show()
"""
JDBC写出, 会自动创建表的.
因为DataFrame中有表结构信息, StructType记录的 各个字段的 名称 类型  和是否运行为空
"""
