#coding=utf-8

import pandas as pd
import numpy as np

'''
Pandas 的数据结构：
Pandas 主要有 Series（一维数组），DataFrame（二维数组），Panel（三维数组），Panel4D（四维数组），PanelND（更多维数组）等数据结构。
其中 Series 和 DataFrame 应用的最为广泛。
- Series 是一维带标签的数组，它可以包含任何数据类型。包括整数，字符串，浮点数，Python 对象等。Series 可以通过标签来定位。
- DataFrame 是二维的带标签的数据结构。我们可以通过标签来定位数据。这是 NumPy 所没有的。
'''

#一、series创建
#1、从列表创建series
arr = [5,1,'m',3,4,'a']
s1 = pd.Series(arr)
print(s1)
#打印结果，前部分为索引，后部分为索引处对应值

#2、从Ndarray创建Series
n = np.random.random(5)
print(n)
index = ['m','b','c','d','e']
s2 = pd.Series(data=n, index=index)
print(s2)

#3、从字典创建series
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
s3 = pd.Series(data=d, index=index)
print(s3)

#二、Series 运算
d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}  # 定义示例字典
s1 = pd.Series(d)
arr = [1,2,3,-4,5]
index = ['A','B','C','d','e']
s2 = pd.Series(data=arr, index=index)
print(s1)
print(s2)

s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s)

dates = pd.date_range('20130101', periods=6)
print(dates)






