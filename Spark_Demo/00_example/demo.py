from pyspark import SparkConf,SparkContext
import os
os.environ['JAVA_HOME'] = 'C:\Program Files\Java\jdk1.8.0_202'  # 这里的路径为java的bin目录所在路径
if __name__ == '__main__':
    conf = SparkConf().setAppName('00_00')
    sc = SparkContext(conf=conf)
