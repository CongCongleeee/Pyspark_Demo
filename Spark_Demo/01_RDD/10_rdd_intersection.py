# ：10_rdd_intersection

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
    conf = SparkConf().setAppName('10_rdd_intersection').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd1 = sc.parallelize([(1001,'张三','财务部'),(1002,'李四','销售部'),(1003,'王五','销售部')])
    rdd2 = sc.parallelize([(1001,'张三','财务部'),(1002,'李四','销售部'),(1003,'刘秀','政治部')])

    #交集intersection
    print(rdd1.intersection(rdd2).collect())
