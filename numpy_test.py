#coding=utf-8

#一、有1、2、3、4个数字，能组成多少个互不相同且无重复数字的三位数
def a1():
    numcount = 0
    for i in range(1,5):
        for j in range(1,5):
            for k in range(1,5):
                if i != j and i != k and j != k:
                    num = i*100+j*10+k
                    print(num)
                    numcount += 1
    print(numcount)
print('一、有1、2、3、4个数字，能组成多少个互不相同且无重复数字的三位数')
a1()

#二、一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？
import math
def a2():
    num = 1
    while True:
        if (math.sqrt(num+100) - int(math.sqrt(num+100)) == 0) and (math.sqrt(num+168) - int(math.sqrt(num+168)) == 0):
            print(num)
            break
        num += 1
print('二、一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？')
a2()

#三、