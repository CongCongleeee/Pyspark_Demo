# ：25_rdd_cache

# coding:utf8
from pyspark import SparkConf, SparkContext
import os,time
from pyspark.storagelevel import StorageLevel



os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # # 生成sparkcontext对象
    # conf = SparkConf().setAppName('25_rdd_cache').setMaster("local[*]")
    # sc = SparkContext(conf=conf)
    #
    # rdd = sc.textFile('hdfs://node1:8020/input/words.txt')
    # rdd2 = rdd.flatMap(lambda line: line.split(" ")).map(lambda word:(word,1))
    # print(rdd2.collect())
    # # [('hello', 1), ('spark', 1), ('hello', 1), ('hadoop', 1), ('hello', 1), ('flink', 1)]
    #
    # rdd3 = rdd2.reduceByKey(lambda a,b:a+b)
    # print(rdd3.collect())
    # # [('hadoop', 1), ('hello', 3), ('spark', 1), ('flink', 1)]
    #
    # rdd4 = rdd2.groupByKey()
    # print(rdd4.collect())
    # # [('hadoop', < pyspark.resultiterable.ResultIterable object at 0x7f0ba342cf40 >),
    # #  ('hello', < pyspark.resultiterable.ResultIterable object at 0x7f0ba3433f10 >),
    # #  ('spark', < pyspark.resultiterable.ResultIterable object at 0x7f0ba3433fa0 >),
    # #  ('flink', < pyspark.resultiterable.ResultIterable object at 0x7f0ba3444040 >)]
    # print(rdd4.mapValues(lambda x:list(x)).collect())
    # rdd5 = rdd4.mapValues(lambda x: sum(x))
    # print(rdd5.collect())
    # rdd6 = rdd4.map(lambda x: (x[0],sum(x[1])))
    # print(rdd6.collect())

    # cache()
    # 生成sparkcontext对象
    conf = SparkConf().setAppName('25_rdd_cache').setMaster("local[*]")
    sc = SparkContext(conf=conf)

    rdd = sc.textFile('hdfs://node1:8020/input/words.txt')
    rdd2 = rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1))
    # [('hello', 1), ('spark', 1), ('hello', 1), ('hadoop', 1), ('hello', 1), ('flink', 1)]
    # print('$%^&*')  #第二此不运行,只运行rdd

    #rdd持久化
    # rdd2.cache() #储存在内存
    rdd2.persist(storageLevel= StorageLevel.MEMORY_AND_DISK_2)

    rdd3 = rdd2.reduceByKey(lambda a, b: a + b)
    print(rdd3.collect())
    # [('hadoop', 1), ('hello', 3), ('spark', 1), ('flink', 1)]

    rdd4 = rdd2.groupByKey()
    rdd5 = rdd4.mapValues(lambda x: sum(x))
    print(rdd5.collect())
    # [('hadoop', 1), ('hello', 3), ('spark', 1), ('flink', 1)]

    #释放存储
    rdd2.unpersist()

    time.sleep(1000000)