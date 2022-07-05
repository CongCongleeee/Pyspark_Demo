# ：13_rdd_sortBy

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
    conf = SparkConf().setAppName('13_rdd_sortBy').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([('c', 3), ('f', 1), ('b', 11), ('c', 3), ('a', 1), ('c', 5), ('e', 1), ('n', 9), ('a', 1)], 3)

    #按照value排序
    print(rdd.sortBy(lambda x: x[1],ascending=True,numPartitions=3).glom().collect())
    print(rdd.sortBy(lambda x: x[1],True,3).glom().collect())
    #按照key排序
    print(rdd.sortBy(lambda x: x[0],ascending=True,numPartitions=3).glom().collect())

    # 整体排序
    print('整体排序')
    print(rdd.sortBy(lambda x: x[1],ascending=True,numPartitions=1).glom().collect())
    print(rdd.sortBy(lambda x: x[0],ascending=True,numPartitions=1).glom().collect())

