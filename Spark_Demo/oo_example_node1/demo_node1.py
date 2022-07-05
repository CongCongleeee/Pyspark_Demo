from pyspark import SparkConf,SparkContext
import os
os.environ['JAVA_HOME'] = '/export/server/jdk'  # 这里的路径为java的bin目录所在路径
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python3.8'
# os.environ['SPARK_HOME'] = '/export/server/spark'
if __name__ == '__main__':
    conf = SparkConf().setAppName('00_00').setMaster('yarn')
    sc = SparkContext(conf=conf)
