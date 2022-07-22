# coding:utf8

from pyhive import hive

if __name__ == '__main__':
    # 获取到Hive(Spark ThriftServer的链接)
    conn = hive.Connection(host="node1", port=10000, username="root")

    # 获取一个游标对象
    cursor = conn.cursor()

    # 执行SQL
    cursor.execute("SELECT * FROM itheima.t_2")

    # 通过fetchall API 获得返回值
    result = cursor.fetchall()

    print(result)
