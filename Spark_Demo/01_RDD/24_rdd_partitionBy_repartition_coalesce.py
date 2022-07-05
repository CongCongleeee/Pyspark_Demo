# ：24_rdd_partitionBy_repartition_coalesce

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
    conf = SparkConf().setAppName('24_rdd_partitionBy_repartition_coalesce').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    #partitionBy
    #(K,V)
    # rdd = sc.parallelize(([1, 2, 3,4,5,6,7,8,9],3))
    # def progress(data):
    #     for i in data:
    #         if i in (1,2): return 1
    #         if i in (3,4): return 2
    #         if i in (5,6): return 3
    #         if i in (7,8): return 4
    #         return 5
    #
    # print(rdd.partitionBy(5, progress).glom().collect())

    # rdd = sc.parallelize([('hadoop', 1), ('spark', 1), ('hello', 1), ('flink', 1), ('hadoop', 1), ('spark', 1)])
    # # 使用partitionBy 自定义 分区
    # def process(k):
    #     if 'hadoop' == k or 'hello' == k: return 0
    #     if 'spark' == k: return 1
    #     return 2
    # print(rdd.partitionBy(3, process).glom().collect())

    #repartition
    rdd = sc.parallelize(([1, 2, 3,4,5,6,7,8,9],3))
    print(rdd.repartition(5).getNumPartitions())
    print(rdd.coalesce(5, shuffle=True).getNumPartitions())
    print(rdd.coalesce(5, shuffle=False).getNumPartitions())