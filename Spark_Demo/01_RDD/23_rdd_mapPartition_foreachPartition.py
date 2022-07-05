# ：23_rdd_partitionBy

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
    conf = SparkConf().setAppName('23_rdd_partitionBy').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # rdd = sc.textFile('hdfs://node1:8020/input/words.txt')
    # rdd = sc.parallelize([1, 2, 3,4,5,6,7,8,9],3)
    # 迭代器 mapPartition , foreachPartition,
    # #partitionBy(分区数,自定义分区规则), repartition(分区数),coalesce(分区数,shuffle)

    # def progress(data):
    #     result=[]
    #     for iter in data:
    #         result.append(iter*10)
    #     return result
    #
    # print(rdd.mapPartitions(progress).collect())

    #foreachPartition
    rdd = sc.parallelize([1, 2, 3,4,5,6,7,8,9],3)

    def progress2(data):
        result = []
        for iter in data:
            result.append(iter * 10)
        print(result)


    rdd.foreachPartition(progress2)