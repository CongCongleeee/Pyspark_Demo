# ：05_rdd_operators_flatMap

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
    conf = SparkConf().setAppName('05_rdd_operators_flatMap').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # rdd = sc.parallelize(['hadoop hadoop flink','kafka flink','hadoop spark hadoop'])
    # rdd1 = rdd.map(lambda x: x.split(" "))
    # print(rdd1.collect())
    # rdd2 = rdd1.map(lambda x: (x,1))
    # rdd3 = rdd2.reduceByKey(lambda a,b: a+b)
    # print(rdd3.collect())



    rdd = sc.parallelize(['hadoop hadoop flink','kafka flink','hadoop spark hadoop'])
    rdd1 = rdd.flatMap(lambda x: x.split(" "))
    rdd2 = rdd1.map(lambda x: (x, 1))
    print(rdd2.collect())
    rdd3 = rdd2.reduceByKey(lambda a,b: a+b)
    print(rdd3.collect())
