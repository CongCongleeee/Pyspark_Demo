# coding:utf8
from pyspark import SparkConf,SparkContext
import os

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

#yarn 配置
os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    conf = SparkConf().setMaster("local[*]").setAppName('helloworld')
    sc = SparkContext(conf=conf)

    # 生成rdd,不指定分区数
    rdd = sc.parallelize([1,2,3,4,5,6,7,8,9])
    #默认分区数
    print('默认分区数',rdd.getNumPartitions())
    print(rdd.glom().collect())