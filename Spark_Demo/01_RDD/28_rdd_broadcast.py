# ：28_rdd_broadcast_accumulator

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
    conf = SparkConf().setAppName('28_rdd_broadcast_accumulator').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    stu_info_list = [(1, '张大仙', 11),
                     (2, '王晓晓', 13),
                     (3, '张甜甜', 11),
                     (4, '王大力', 11)]
    #定义广播变量
    """
    场景: 本地集合对象 和 分布式集合对象(RDD) 进行关联的时候
    需要将本地集合对象 封装为广播变量
    可以节省:
    1. 网络IO的次数
    2. Executor的内存占用
    """
    stu_info_broadcast = sc.broadcast(stu_info_list)

    score_info_rdd = sc.parallelize([
        (1, '语文', 99),
        (2, '数学', 99),
        (3, '英语', 99),
        (4, '编程', 99),
        (1, '语文', 99),
        (2, '编程', 99),
        (3, '语文', 99),
        (4, '英语', 99),
        (1, '语文', 99),
        (3, '英语', 99),
        (2, '编程', 99)
    ])

    def map_function(data):
        global stu_info_broadcast
        name =''
        for i in stu_info_broadcast.value:
            if data[0]==i[0]:
                name = i[1]
                data = (data[0],name,data[1],data[2])
        return data

    #映射
    map_rdd = score_info_rdd.map(map_function)
    print(map_rdd.collect())
