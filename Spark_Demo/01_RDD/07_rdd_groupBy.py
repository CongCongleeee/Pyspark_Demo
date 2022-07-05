# ：07_rdd_groupBy

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
    conf = SparkConf().setAppName('07_rdd_groupBy').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([('hadoop', 1,'a'), ('hadoop', 1,'a'), ('hadoop', 1,'b'), ('flink', 2,'a'),('flink', 2,'b'), ('flink', 2,'b')])
    result = rdd.groupBy(lambda x:x[0])
    print(result.collect())
    print(result.map(lambda x:(x[0],list(x[1]))).collect())

    #案例
    rdd = sc.parallelize([('a', 1), ('a', 1), ('b', 1), ('b', 2), ('b', 3)])
    # 通过groupBy对数据进行分组
    # groupBy传入的函数的 意思是: 通过这个函数, 确定按照谁来分组(返回谁即可)
    # 分组规则 和SQL是一致的, 也就是相同的在一个组(Hash分组)
    result = rdd.groupBy(lambda t: t[0])
    print(result.map(lambda t: (t[0], list(t[1]))).collect())

