# ：22_rdd_saveAsTextFile

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
    conf = SparkConf().setAppName('22_rdd_saveAsTextFile').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    #如果路径已存在会报错
    # rdd = sc.parallelize([1,2,3],1)
    # rdd.saveAsTextFile('../../InputData/out1')

    #写入hdfs
    # rdd2 = sc.parallelize([1,2,3,4, 5, 6,7,8,9],3)
    # rdd2.saveAsTextFile('hdfs://node1:8020/output/out1')
    #读取