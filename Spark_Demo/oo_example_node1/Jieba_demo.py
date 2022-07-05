# ：First_demo

# coding:utf8
from pyspark import SparkConf, SparkContext
import os
import jieba

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    # conf = SparkConf().setAppName('First_demo').setMaster("local[*]")
    # sc = SparkContext(conf=conf)

    content = "小明硕士毕业于中国科学院计算所,后在清华大学深造"
    # print(list(jieba.cut(content,True)))
    # print(list(jieba.cut(content,False)))

    #搜索模式
    result = jieba.cut_for_search(content)
    # print(content)
    print(result)
    # print(','.join(result))