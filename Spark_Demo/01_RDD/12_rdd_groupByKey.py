# ：12_rdd_groupByKey

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
    conf = SparkConf().setAppName('12_rdd_groupByKey').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize(([('a', 1), ('a', 1), ('b', 1), ('b', 1), ('b', 1)]))
    print(rdd.groupByKey().collect())
    print(rdd.groupByKey().mapValues(lambda x:list(x)).collect())
    print(rdd.groupByKey().map(lambda x:(x[0],list(x[1]))).collect())