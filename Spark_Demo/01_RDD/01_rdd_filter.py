# ：01_rdd_filter

# coding:utf8
from pyspark import SparkConf, SparkContext
import os

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    conf = SparkConf().setAppName('01_rdd_filter').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd= sc.parallelize([1,2,3,4,5,6])
    print(rdd.filter(lambda x: x % 2 == 0).collect())