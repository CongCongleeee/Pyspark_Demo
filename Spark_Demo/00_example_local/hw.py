
# coding:utf8
from pyspark import SparkConf, SparkContext
from pyspark.sql.functions import *
import os
# os.environ['JAVA_HOME'] = 'C:\\Program Files\\Java\\jdk1.8.0_202'  # 这里的路径为java的bin目录所在路径
os.environ['PYSPARK_DRIVER_PYTHON'] = 'C:\\Users\YP715HX\Documents\Documents\Python Item\venv\Scripts\python.exe'

if __name__ == '__main__':
    conf = SparkConf().setAppName('00_00')
    # 通过SparkConf对象构建SparkContext对象
    sc = SparkContext(conf=conf)

    # 需求 : wordcount单词计数, 读取HDFS上的words.txt文件, 对其内部的单词统计出现 的数量
    # 读取文件
    file_rdd = sc.textFile("./words.txt")
    # file_rdd = sc.textFile("hdfs://node1:8020/Input/words.txt")

    # 将单词进行切割, 得到一个存储全部单词的集合对象
    words_rdd = file_rdd.flatMap(lambda line: line.split(" "))

    # 将单词转换为元组对象, key是单词, value是数字1
    words_with_one_rdd = words_rdd.map(lambda x: (x, 1))

    # 将元组的value 按照key来分组, 对所有的value执行聚合操作(相加)
    result_rdd = words_with_one_rdd.reduceByKey(lambda a, b: a + b)

    # 通过collect方法收集RDD的数据打印输出结果
    # print(result_rdd)
    print(result_rdd.collect())
