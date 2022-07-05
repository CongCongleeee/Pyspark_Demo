# ：17_action_countByKey

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
    conf = SparkConf().setAppName('17_action_countByKey').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # #countByKey
    # rdd = sc.textFile('hdfs://node1:8020/Input/words.txt')
    # word_rdd= rdd.flatMap(lambda line: line.split(' ')).map(lambda word: (word,1))
    # # print(word_rdd.collect())
    # print(word_rdd.countByKey())

    # #countByValue
    # rdd = sc.textFile('hdfs://node1:8020/Input/words.txt')
    # word_rdd = rdd.flatMap(lambda line: line.split(' '))
    # # print(word_rdd.collect())
    # print(word_rdd.countByValue())

    #flatMap 列表应用
    r1 = sc.parallelize(
        [("fruites", ["apple", "banana", "lemon"]), ("vegetables", ["tomato", "cabbage"])]).flatMapValues(lambda x: x)
    print(r1.collect())
    #输出: [('fruites', 'apple'), ('fruites', 'banana'), ('fruites', 'lemon'), ('vegetables', 'tomato'), ('vegetables', 'cabbage')]
    print(r1.countByKey())
    # 输出: defaultdict(int, {'fruites': 3, 'vegetables': 2})

