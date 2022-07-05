# ：15_rdd_Case

# coding:utf8
from pyspark import SparkConf, SparkContext
import os,json
from defs import area_category

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    conf = SparkConf().setAppName('16_rdd_Case_yarn').setMaster("yarn")
    #添加依赖文件 或者 zip包
    conf.set('spark.submit.pyFiles','defs.py')
    sc = SparkContext(conf=conf)

    file_rdd = sc.textFile('hdfs://node1:8020/Input/order.text')
    json_rdd = file_rdd.flatMap(lambda line: line.split("|"))
    print(json_rdd.collect())
    dist_rdd = json_rdd.map(lambda json_str: json.loads(json_str))
    beijing_rdd = dist_rdd.filter(lambda dist: dist['areaName'] == '北京')
    print(beijing_rdd.collect())
    result_rdd = beijing_rdd.map(area_category)
    distinct_result_rdd = result_rdd.distinct()
    print(distinct_result_rdd.collect())



