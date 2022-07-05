# ：12_movie_demo
# coding:utf8
import os,time
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
    spark = SparkSession.builder.appName("12_movie_demo").master("local[*]").getOrCreate()
    sc = spark.sparkContext

    #读取数据
    schema = StructType().\
        add('user_id',StringType(),nullable=True).\
        add('movie_id',StringType(),nullable=True). \
        add('rank',IntegerType(),nullable=True).\
        add('ts',StringType(),nullable=True)
    df = spark.read.format('csv').\
        option('encoding','utf8').\
        option('header',False).\
        option('sep','\t').\
        schema(schema=schema).\
        load('./u.data')
    # df.show(n=5,truncate=False)
    '''
    +-------+--------+----+---------+
    |user_id|movie_id|rank|ts       |
    +-------+--------+----+---------+
    |196    |242     |3   |881250949|
    |186    |302     |3   |891717742|
    |22     |377     |1   |878887116|
    |244    |51      |2   |880606923|
    |166    |346     |1   |886397596|
    +-------+--------+----+---------+
    '''

    # 需求1:查询用户平均分
    # requirement1 = df.groupBy('user_id').avg('rank').\
    #     withColumnRenamed('avg(rank)','avg_rank').\
    #     withColumn('avg_rank',F.round('avg_rank',2)).\
    #     orderBy('avg_rank',ascending=False)
    # requirement1.show(5)
    #第二种方式:
    df.groupBy('user_id').\
        agg(F.round(F.avg('rank'),2).alias("avg_rank")).\
        orderBy('avg_rank', ascending=False).\
        show(5)


    # 需求2: 查询电影平均分
    movie_id_col = df['movie_id']
    requirement2 =df.groupBy(movie_id_col).\
        agg(F.avg('rank').alias("avg_rank")).\
        sort('avg_rank',ascending=False)
    requirement2.show(5)
    # requirement2.collect()
    #方式二
    # df.createTempView("movie")
    # spark.sql("""
    #         SELECT movie_id, ROUND(AVG(rank), 2) AS avg_rank FROM movie GROUP BY movie_id ORDER BY avg_rank DESC
    #     """).show(5)

    #需求3:查询大于平均分的电影
    print(df.where(df['rank'] > df.select(F.avg(df['rank'])).first()['avg(rank)']).count())
    # print(df.where(df['rank'] > F.avg(df['rank'])).count())
    print(df.select( F.avg(df['rank'])).count())
    df.select(F.avg(df['rank'])).show()

    #需求4
    print('需求4:')
    user_id_score = df.where(df['rank']>3).\
        groupBy('user_id').count()\
        .sort('count',ascending=False).limit(1)\
        .first()['user_id']
    df.where(df['user_id'] == user_id_score).select(F.round(F.avg(df['rank']),2)).show()

    #需求5
    print('需求5')
    df.groupBy('user_id').agg(
        F.round(F.avg('rank'),2).alias('avg_rank'),
        F.round(F.max('rank'),2).alias('avg_rank'),
        F.round(F.min('rank'),2).alias('avg_rank')
    ).show()

    #需求6
    print('需求6')
    # df.groupBy('movie_id').agg(
    #     F.count('rank').alias('cnt'),
    #     F.round(F.avg('rank'),2).alias('avg_rank')
    # ).where('cnt>100').sort('avg_rank',ascending=False).limit(10).show()

    df6 =  df.groupBy('movie_id').agg(
        F.count('rank').alias('cnt'),
        F.round(F.avg('rank'), 2).alias('avg_rank')
    )
    df6.filter('cnt>100').sort('avg_rank',ascending=False).limit(10).show()

    time.sleep(10000)
