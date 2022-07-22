# ：18_udf_dist
# coding:utf8
import os,string
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

if __name__ == '__main__':
    # 生成sparkcontext对象
    spark = SparkSession.builder.appName("18_udf_dist").master("local[*]"). \
        config("spark.sql.shuffle.partitions", 2). \
        getOrCreate()
    sc = spark.sparkContext

    # 假设 有三个数字  1 2 3  我们传入数字 ,返回数字所在序号对应的 字母 然后和数字结合形成dict返回
    # 比如传入1 我们返回 {"num":1, "letters": "a"}
    rdd = sc.parallelize([[1],[2],[3]])
    df = rdd.toDF(['num'])

    def num_dist(data):
        return {'num':data,'letters':string.ascii_letters[data]}


    """
        UDF的返回值是字典的话, 需要用StructType来接收
    """
    #定义并执行函数
    struct_type = StructType().\
        add('num',IntegerType(),nullable=True).\
        add('letters',StringType(),nullable=True)
    num_dist_udf = F.udf(num_dist,struct_type)

    df2 = df.select(num_dist_udf(df['num'])).show()
    """
    +-------------+
    |content      |
    +-------------+
    |{1, b}       |
    |{2, c}       |
    |{3, d}       |
    +-------------+
    """
