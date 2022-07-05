# ：09_rdd_join

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
    conf = SparkConf().setAppName('09_rdd_join').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.parallelize([(1001, "zhangsan"), (1002, "lisi"), (1003, "wangwu"), (1004, "zhaoliu")])
    rdd2 = sc.parallelize([(1001, "销售部"), (1002, "科技部")])

    #join 内连接(key,value) on=key
    print(rdd1.join(rdd2).collect())
    #leftOutJoin() 左外连接
    print(rdd1.leftOuterJoin(rdd2).collect())
    #rightOutJoin()右外连接
    print(rdd1.rightOuterJoin(rdd2).collect())
