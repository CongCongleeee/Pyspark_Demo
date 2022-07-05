# ：31_rdd_broadcast_accumulator

# coding:utf8
from pyspark import SparkConf, SparkContext
import os,re

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    conf = SparkConf().setAppName('31_rdd_broadcast_accumulator').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.textFile('./accumulator_broadcast_data.txt')
    # print(rdd.collect())

    #特殊字符
    abnormal_char = [",", ".", "!", "#", "$", "%"]
    # 定义广播变量
    bc = sc.broadcast(abnormal_char)
    #定义累加器
    acmlt = sc.accumulator(0)

    #去除空行
    without_bline_rdd = rdd.filter(lambda line: line.strip())
    #去除空字符串
    without_bstr_rdd = without_bline_rdd.map(lambda line: line.strip())
    pre_word_rdd = without_bstr_rdd.flatMap(lambda line: re.split('\s+',line))
    print('pre_word_rdd: ',pre_word_rdd.collect())
    # pre_word_rdd:  [['hadoop', 'spark', '#', 'hadoop', 'spark', 'spark'], ['mapreduce', '!', 'spark', 'spark', 'hive', '!'], ['hive', 'spark', 'hadoop', 'mapreduce', 'spark', '%'], ['spark', 'hive', 'sql', 'sql', 'spark', 'hive', ',', 'hive', 'spark', '!'], ['!', 'hdfs', 'hdfs', 'mapreduce', 'mapreduce', 'spark', 'hive'], ['#']]
    def filter_fuction(data):
        global acmlt
        if data in bc.value:
            acmlt +=1
            return False
        else:
            return True
    #筛选出特殊字符
    word_rdd = pre_word_rdd.filter(filter_fuction)
    res_rdd = word_rdd.map(lambda word: (word,1)).reduceByKey(lambda a,b : a+b)
    print(res_rdd.collect())
    print('特殊符号总数:',acmlt)




