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
    df = spark.read.format('csv').option('sep',';').option('header',True).load('./people.csv')
    df.show()

    ## 存储文件 目前只可以保存到hdfs
    df.write.mode('overwrite').format('json')\
        .save('hdfs://node1/output/people_out_json')
        # .save('./people_out_json')
    df.write.mode('overwrite').format('parquet') \
        .save('hdfs://node1/output/people_out_parquet')
        # .save('./people_out_parquet')
    df.write.mode('overwrite').format('csv')\
        .option('sep',';')\
        .option('header',True)\
        .save('hdfs://node1/output/people_out_csv')
        # .save('./people_out_csv')

    df.select(F.concat_ws('--','name','age','job'))\
        .write.mode('overwrite').format('text')\
        .save('hdfs://node1/output/people_out_txt')
        # .save('./people_out_txt')

    print('*******')