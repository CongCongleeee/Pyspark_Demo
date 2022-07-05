# ：14_rdd_sortByKey

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
    conf = SparkConf().setAppName('14_rdd_sortByKey').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([('a', 1), ('E', 1), ('C', 1), ('D', 1), ('b', 1), ('g', 1), ('f', 1),
                          ('y', 1), ('u', 1), ('i', 1), ('o', 1), ('p', 1),
                          ('m', 1), ('n', 1), ('j', 1), ('k', 1), ('l', 1)], 3)

    print(rdd.sortByKey(numPartitions=1,ascending=True,keyfunc=lambda x: x.upper()).collect())
    print(rdd.sortByKey(keyfunc = lambda x: x.lower()).collect())