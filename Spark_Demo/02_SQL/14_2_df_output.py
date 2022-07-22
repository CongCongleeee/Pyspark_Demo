# ：14_df_output
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
    spark = SparkSession.builder.appName("14_df_output").master("local[*]").getOrCreate()
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
        load("./u.data")
    df.show()

    # Write text 写出, 只能写出一个列的数据, 需要将df转换为单列df
    df.select(F.concat_ws("---", "user_id", "movie_id", "rank", "ts")).\
        write.\
        mode("overwrite").\
        format("text").\
        save("./text")

    # Write csv
    df.write.mode("overwrite").\
        format("csv").\
        option("sep", ";").\
        option("header", True).\
        save("./csv")

    # Write json
    df.write.mode("overwrite").\
        format("json").\
        save("./json")

    # Write parquet
    df.write.mode("overwrite").\
        format("parquet").\
        save("./parquet")


