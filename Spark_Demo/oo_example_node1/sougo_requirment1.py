# ：sougo_requirment1

# coding:utf8
from pyspark import SparkConf, SparkContext
import os,jieba,time
from defs import *
from pyspark.storagelevel import StorageLevel

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    conf = SparkConf().setAppName('sougo_requirment1').setMaster('yarn')
    #yarn模式下添加依赖文件
    conf.set('spark.submit.pyFiles','./defs.py')
    sc = SparkContext(conf=conf)

    file_rdd = sc.textFile('/input/SogouQ.txt')
    # print(file_rdd.take(5))
    line_rdd = file_rdd.map(lambda line: line.split("\t"))
    line_rdd.persist(storageLevel=StorageLevel.DISK_ONLY)

    # TODO: 需求1: 用户搜索的关键`词`分析
    # 主要分析热点词
    # 将所有的搜索内容取出
    context_rdd = line_rdd.map(lambda line:line[2])
    #['传智播客', '黑马程序员', '传智播客', '博学谷', 'IDEA', '传智专修学院']
    words_rdd = context_rdd.flatMap(context_jieba)
    # print(words_rdd.takeSample(True,30))
    # 院校 帮 -> 院校帮
    # 博学 谷 -> 博学谷
    # 传智播 客 -> 传智播客
    filter_rdd = words_rdd.filter(contex_filter)
    # 将关键词转换: 穿直播 -> 传智播客
    final_word_rdd =  filter_rdd.map(context_append)
    # print(final_word_rdd.takeSample(True,10))
    # [('传智', 1), ('博学谷', 1), ('spark', 1), ('仓库', 1), ('传智', 1), ('flume', 1), ('DataLake', 1), ('黑马', 1)]
    result1 = final_word_rdd.reduceByKey(lambda a,b:a+b).sortBy(lambda x:x[1],ascending=False,numPartitions=1).take(5)
    print(result1)

    # TODO: 需求2: 用户和关键词组合分析
    # 1, 我喜欢传智播客
    # 1+我  1+喜欢 1+传智播客
    user_content_rdd = line_rdd.map(lambda line:(line[2],line[3]))
    user_filter_rdd = user_content_rdd.flatMap(user_content_filter)
    user_reduce_rdd = user_filter_rdd.reduceByKey(lambda a,b: a+b)
    result2_rdd = user_reduce_rdd.sortBy(lambda x: x[1], ascending=False, numPartitions=1).take(5)
    print('热门分析:',result2_rdd)

    # TODO: 需求3: 热门搜索时间段分析
    # 取出来所有的时间
    print(line_rdd.top(10))
    time_rdd = line_rdd.map(lambda line: line[0])
    time_deal_rdd = time_rdd.map(lambda time: (time.split(':')[0],1))
    result3_rdd = time_deal_rdd.reduceByKey(lambda a,b : a+b)
    print(result3_rdd.sortBy(lambda x: x[1], ascending=False, numPartitions=1).take(5))

    # 释放内存
    line_rdd.unpersist()

    time.sleep(10000)



