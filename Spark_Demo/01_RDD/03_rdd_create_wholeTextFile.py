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
    conf = SparkConf().setAppName('read file').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # rdd = sc.textFile("hdfs://node1:8020/Input/tiny_files/1.txt")
    # print(rdd.collect())

    # 测试参数
    rdd = sc.wholeTextFiles("hdfs://node1:8020/Input/tiny_files")
    # rdd = sc.wholeTextFiles("hdfs://node1:8020/Input/tiny_files",100)
    # rdd = sc.wholeTextFiles("../../InputData/tiny_files",4)
    # print(rdd.collect())
    print('默认分区数: ',rdd.getNumPartitions())
    rdd1 = rdd.map(lambda x:x[1])
    print('数据抽取: ',rdd1.glom().collect())





