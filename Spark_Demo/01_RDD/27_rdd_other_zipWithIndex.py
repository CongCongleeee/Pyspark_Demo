# ：27_rdd_other_zipWithIndex

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
    conf = SparkConf().setAppName('27_rdd_other_zipWithIndex').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    #zipWithIndex()
    rdd = sc.parallelize(['spark','hadoop','flink'])
    rdd2 = rdd.zipWithIndex()
    print(rdd2.collect())

    # collectAsMap()
    rdd3 = rdd2.collectAsMap()
    print(rdd3)
    print(f'{rdd3["spark"]}--{rdd3["hadoop"]}--{rdd3["flink"]}')