# ：20_rdd_first_take

# coding:utf8
from pyspark import SparkConf, SparkContext
import os
#本地
# os.environ['JAVA_HOME'] = 'C:\Program Files\Java\jdk1.8.0_202'  # 这里的路径为java的bin目录所在路径
# os.environ['JAVA_HOME'] = 'C:\Program Files\Java\jdk1.8.0_202'  # 这里的路径为java的bin目录所在路径

#node1
os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    conf = SparkConf().setAppName('20_rdd_first_take').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    # first/take/top
    # rdd = sc.parallelize([1,2,3,4,5,6,7,8,9,0])
    # print(rdd.first())
    # print(rdd.take(3))
    # print(rdd.top(3))

    # takeSample 参数1:是否取同一个数字 参数2:取几个数 参数3:随机种子,数字随意取
    # rdd = sc.parallelize([1,2,3])
    # print(rdd.takeSample(True, 20))
    # print(rdd.takeSample(False, 20))

    # 样本不重复是对于单次运行的代码,不是迭代不重复
    # print(rdd.takeSample(False, 2))
    # print(rdd.takeSample(False, 2))
    # print(rdd.takeSample(False, 2))

    # 随机数不变,指定随机数
    # print(rdd.takeSample(False, 20,2))
    # print(rdd.takeSample(False, 20,2))
    # print(rdd.takeSample(False, 20,2))

    #takeOrdered 取数排序
    rdd = sc.parallelize([12,23,13,4,55,6])
    print(rdd.takeOrdered(3))
    print(rdd.takeOrdered(3,lambda x: -x))

    # first_take_top_takeSample_takeOrdered

