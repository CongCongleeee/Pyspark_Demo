# ：demo
# coding:utf8
import os
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
import pandas as pd
import numpy as np
import pyspark.pandas as ps

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'
os.environ['PYARROW_IGNORE_TIMEZONE'] = '1'


# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    spark = SparkSession.builder.appName("demo").master("local[*]"). \
        config("spark.sql.shuffle.partitions", 2). \
        getOrCreate()
    sc = spark.sparkContext

    df = ps.DataFrame(dict(
        date=list(pd.date_range('2012-1-1 12:00:00', periods=3, freq='M')),
        country=['KR', 'US', 'JP'],
        code=[1, 2, 3]), columns=['date', 'country', 'code'])
    print(df)
