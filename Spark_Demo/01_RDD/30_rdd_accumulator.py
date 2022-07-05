# ：30_rdd_accumulator

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
    conf = SparkConf().setAppName('30_rdd_accumulator').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1,2,3,4,5,6,7,8,9,10],2)
    # count = 0
    count = sc.accumulator(0)
    def map_function(data):
        global count
        count+=1
        print(count)
        return data

    res_rdd = rdd.map(map_function)
    #转入内存
    res_rdd.cache()
    res_rdd.collect()
    # print('res_rdd',res_rdd)
    print('******')


    res_rdd2 = res_rdd.map(lambda x:x).collect()
    # print('res_rdd2',res_rdd2.collect())
    print('count: ',count)

    #释放内存
    res_rdd.unpersist()