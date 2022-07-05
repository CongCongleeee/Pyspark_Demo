# coding:utf8
from pyspark import SparkConf,SparkContext
import os

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

#yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    # conf = SparkConf().setAppName('read file').setMaster("local[*]")
    conf = SparkConf().setAppName('read file')
    sc = SparkContext(conf=conf)

    #读取本地文件
    rdd = sc.textFile('./words.txt')
    print(rdd.collect())

    # #少数分区
    # rdd = sc.textFile("hdfs://node1:8020/Input/words.txt",5)
    # print(rdd.getNumPartitions())
    # print(rdd.collect())
    #
    # #超多分区
    # print("&&&&&")
    # rdd = sc.textFile("hdfs://node1:8020/Input/words.txt", 300)
    # print(rdd.getNumPartitions())
    # print(rdd.collect())