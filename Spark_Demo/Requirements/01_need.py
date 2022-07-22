# ：01_need
# coding:utf8
import os
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.storagelevel import StorageLevel

os.environ['JAVA_HOME'] = '/export/server/jdk'
os.environ['PYSPARK_PYTHON'] = '/export/server/anaconda3/envs/pyspark/bin/python'

# yarn 配置
# os.environ['HADOOP_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'
# os.environ['YARN_CONF_DIR'] = '/export/server/hadoop/etc/hadoop'

"""
需求1: 各省销售额的统计
需求2: TOP3销售省份中, 有多少店铺达到过日销售额1000+
需求3: TOP3省份中, 各省的平均单单价
需求4: TOP3省份中, 各个省份的支付类型比例

receivable: 订单金额
storeProvince: 店铺省份
dateTS: 订单的销售日期
payType: 支付类型
storeID:店铺ID

2个操作
1. 写出结果到MySQL
2. 写出结果到Hive库
"""
if __name__ == '__main__':
    # 生成SparkContext对象
    spark = SparkSession.builder.appName("01_need").master("local[*]"). \
        config("spark.sql.shuffle.partitions", 2). \
        config("spark.sql.warehouse.dir", 'hdfs://node1:8020/user/hive/warehouse'). \
        config("hive.metastore.uris", 'thrift://node1:9083'). \
        enableHiveSupport(). \
        getOrCreate()
    sc = spark.sparkContext
    # 1. 读取数据
    # 省份信息, 缺失值过滤, 同时省份信息中 会有"null" 字符串
    # 订单的金额, 数据集中有的订单的金额是单笔超过10000的, 这些是测试数据
    # 列值裁剪(SparkSQL会自动做这个优化)

    df = spark.read.format('json').load('hdfs://node1:8020/input/mini.json')
    df = df.dropna(how='any', thresh=1, subset='storeProvince')
    df = df.filter(df['storeProvince'] != 'null').filter(df['receivable'] <= 10000)
    df = df.select(["storeProvince", "storeID", "receivable", "dateTS", "payType"])

    # df.show(10, truncate=False)

    # TODO 需求1: 各省 销售额统计
    province_sale_df = df.groupBy('storeProvince').agg(F.sum('receivable')) \
        .withColumnRenamed('sum(receivable)', 'total_money') \
        .withColumn('total_money', F.round('total_money', 2)) \
        .sort('total_money', ascending=False)  # df列没有变,但是表字段名已经改变,所以withColumn用'Str'风格

    province_sale_df.write.mode("overwrite").saveAsTable("itheima.province_sale", "parquet")

    # TODO 需求2: TOP3销售省份中, 有多少店铺达到过日销售额1000+
    # 2.1 先找到TOP3的销售省份

    top3_province_df = province_sale_df.limit(3).select('storeProvince'). \
        withColumnRenamed('storeProvince', 'top3_Province')
    # top3_province_df.show()

    # 2.2 和 原始的DF进行内关联, 数据关联后, 就是全部都是TOP3省份的销售数据了
    top3_province_df_joined = df.join(top3_province_df, on=df['storeProvince'] == top3_province_df['top3_Province'])
    #永久储存
    top3_province_df_joined.persist(StorageLevel.MEMORY_AND_DISK)
    # 2.3 筛选金额>1000,时间为每天
    province_hot_store_count_df = top3_province_df_joined.groupBy('storeProvince','storeID',F.from_unixtime(df['dateTS'].substr(0,10),'yyyy-MM-dd').alias('day')).\
        sum('receivable').withColumnRenamed("sum(receivable)",'money').filter('money >1000').\
        dropDuplicates(subset=['storeID']).groupBy('storeProvince').count()
    province_hot_store_count_df.show()

    #存入hive
    province_hot_store_count_df.write.mode('overwrite').saveAsTable('itheima.province_hot_store_count',"parquet")

    # TODO 需求3: TOP3 省份中 各个省份的平均订单价格(单单价)
    top3_province_order_avg_df = top3_province_df_joined.groupBy('storeProvince').avg('receivable').\
        withColumnRenamed('avg(receivable)','money').\
        withColumn('money',F.round('money',2)).\
        orderBy('money',asconding=False)
    top3_province_order_avg_df.show()
    top3_province_order_avg_df.write.mode('overwrite').saveAsTable('itheima.top3_province_order_avg','parquet')

    # TODO 需求4: TOP3 省份中, 各个省份的支付比例
    # 湖南省 支付宝 33%
    # 湖南省 现金 36%
    # 广东省 微信 33%
    def my_udf(data):
        return str(round(data*100, 2))+'%'
    my_udf = F.udf(my_udf,StringType())
    top3_province_df_joined.createOrReplaceTempView('province_pay')
    pay_type_df = spark.sql('''
        SELECT storeProvince, payType, (COUNT(payType) / total) AS percent FROM
        (SELECT storeProvince, payType, count(1) OVER(PARTITION BY storeProvince) AS total FROM province_pay) AS sub
        GROUP BY storeProvince, payType, total
    ''').withColumn('percent', my_udf('percent'))
    pay_type_df.show()
    pay_type_df.write.mode("overwrite").saveAsTable("itheima.pay_type", "parquet")



    top3_province_df_joined.unpersist()