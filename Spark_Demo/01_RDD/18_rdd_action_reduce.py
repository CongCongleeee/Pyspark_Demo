# ：18_rdd_action_reduce

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
    conf = SparkConf().setAppName('18_rdd_action_reduce').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # #字符串reduce
    # rdd = sc.textFile('hdfs://node1:8020/Input/words.txt')
    # word_rdd= rdd.flatMap(lambda line: line.split(' '))
    # print(word_rdd.collect())
    # #输出 ['hello', 'spark', 'hello', 'hadoop', 'hello', 'flink']
    # print(word_rdd.reduce(lambda a,b: a+'_'+b ))
    # #输出 hello_spark_hello_hadoop_hello_flink

    #数字reduce
    rdd = sc.parallelize([1,2,3,4,5,6,7])
    print(rdd.reduce(lambda a, b: a + b))

    #reduceByKey
    rdd = sc.textFile('hdfs://node1:8020/Input/words.txt')
    word_rdd = rdd.flatMap(lambda line: line.split(' ')).map(lambda word: (word,1))
    reduce_rdd= word_rdd.reduceByKey(lambda a,b: a+b)
    print(reduce_rdd.collect())

