# ：defs

# coding:utf8
from pyspark import SparkConf, SparkContext
import os
import jieba

def context_jieba(data):
    result = list(jieba.cut_for_search(data))
    return result

    #通过jieba分词工具 进行分词操作
    # seg = jieba.cut_for_search(data)
    # l = list()
    # for word in seg:
    #     l.append(word)
    # return l

def contex_filter(data):
    """过滤不要的 谷 \ 帮 \ 客"""
    return data not in ('谷','帮','客')

def context_append(data):
    if data == '传智播': data = '传智播客'
    if data == '院校': data = '院校帮'
    if data == '博学': data = '博学谷'
    return (data,1)

def user_content_filter(data):
    user = data[0]
    content = data[1]
    words = context_jieba(content)
    words_list = []
    for word in words:
        contex_filter(word)
        words_list.append((user+'_'+context_append(word)[0],1))
    return words_list
if __name__ == '__main__':
    print(user_content_filter(('lc','hadoop')))