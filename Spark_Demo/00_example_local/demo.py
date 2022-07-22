from pyspark import SparkConf,SparkContext
import os
os.environ['JAVA_HOME'] = 'C:\\Program Files\Java\jdk-10.0.1'  # 这里的路径为java的bin目录所在路径
if __name__ == '__main__':
    conf = SparkConf().setAppName('00_00')
    sc = SparkContext(conf=conf)

    rdd = sc.parallelize([1,2,3,4,5,6])
    print(rdd.collect())