# ：15_rdd_Case

# coding:utf8
from pyspark import SparkConf, SparkContext
import os,json

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    conf = SparkConf().setAppName('15_rdd_Case').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    file_rdd = sc.textFile('hdfs://node1:8020/Input/order.text')
    json_rdd = file_rdd.flatMap(lambda line: line.split("|"))
    print(json_rdd.collect())
    dist_rdd = json_rdd.map(lambda json_str: json.loads(json_str))
    beijing_rdd = dist_rdd.filter(lambda dist: dist['areaName'] == '北京')
    print(beijing_rdd.collect())
    result_rdd = beijing_rdd.map(lambda x: x['areaName']+'-'+x['category'])
    distinct_result_rdd = result_rdd.distinct()
    print(distinct_result_rdd.collect())

    # # 读取数据文件
    # file_rdd = sc.textFile('hdfs://node1:8020/Input/order.text')
    #
    # # 进行rdd数据的split 按照|符号进行, 得到一个个的json数据
    # jsons_rdd = file_rdd.flatMap(lambda line: line.split("|"))
    # print(jsons_rdd.collect())
    # # 通过Python 内置的json库, 完成json字符串到字典对象的转换
    # dict_rdd = jsons_rdd.map(lambda json_str: json.loads(json_str))
    #
    # # 过滤数据, 只保留北京的数据
    # beijing_rdd = dict_rdd.filter(lambda d: d['areaName'] == "北京")
    #
    # # 组合北京 和 商品类型形成新的字符串
    # category_rdd = beijing_rdd.map(lambda x: x['areaName'] + "_" + x['category'])
    #
    # # 对结果集进行去重操作
    # result_rdd = category_rdd.distinct()
    #
    # # 输出
    # print(result_rdd.collect())

