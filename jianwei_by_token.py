#coding=utf-8
'''
功能：见微网上，获取上市公司信息；查询条件：时间、公告类型、关键词；
网址：https://www.jianweidata.com/
其他：该方式利用token，直接进行网络下方请求获取响应结果；
'''

import requests
import re
import json
import traceback
import sys
import openpyxl

def downloadPdf(url,root,filename):
    #下载pdf文件，url为pdf链接，root为下载保存路径，filename为文件名
    #root写法：r'C:\Users\admin\Desktop\3月18日测试题\3月18日测试题\3月18日测试题.zip'
    try:
        resp = requests.get(url)
        with open(root+filename, 'wb+') as f:
            f.write(resp.content)
        print('利用{}下载{}文件成功'.format(url, filename))
    except Exception as e:
        print('利用{}下载{}文件失败'.format(url, filename))
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)

def analyHtml(html):
    #页面分析函数，分析结果并写入excel
    try:
        wb = openpyxl.load_workbook('simple.xlsx')
        #wb1 = openpyxl.workbook()
        ws = wb.active
        Hits = html.get('Hits') # Hits = html['Hits']
        for Hit in Hits:
            Source = Hit.get('Source')
            title = Source.get('Title')
            url = Source.get('Url')
            stockcode = Source.get('StockCode')
            time = re.findall(r'\d+', title)

            print(time[0], stockcode, title, url)

            ws.append([time[0], stockcode, title, url])

            #downloadPdf(url=url, root='', filename=title + '.pdf')

        wb.save('simple.xlsx')

    except Exception as e:
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)

def getHtml(pagenum):
    #获取请求响应页面
    if isinstance(pagenum,int):
        url = 'https://www.jianweidata.com/data/api/FinancialNew/SearchFillingInfos'
        data = {
             "label": "",
             "titleMust": "",
             "titleShould": "",
             "titleMustNot": "",
             "contentMust": "套期保值",
             "contentShould": "",
             "contentMustNot": "",
             "subTitleMust": "",
             "subTitleShould": "",
             "subTitleMustNot": "",
             "startDate": "2000/01/01 ",
             "endDate": " 2020/03/14",
             "isSimpleQuery": "false",
             "adjacentTitle": "",
             "adjacentTitleMustNot": "",
             "adjacentDayAhead": "15",
             "adjacentDayBehind": "15",
             "sort": 2,
             "CorpPageNum": 1,
             "CorpPageSize": 20,
             "pageNum": pagenum,
             "pageSize": "1",
             "searchType": 1,
             "sector": 1,
             "isLockedAsset": "false",
             "platform": "web_common",
             "token": "y64Wol%2bu4NHIoj1YpW%2bMzwDJSW9F5k3sCVXFUyKF1VgR4LvmTfRisvnT2GLRq7k4cckH1IlfqbFuNUUwoeT7HcmA7qMKHVnMqDcCGsA2LlimzJzdl3qO4IWG3%2bXrApcKNRBvjklvy6gQzFAl8f9rKg%3d%3d",
             "highlightFilters": [],
             "filters": [{"field": 2,"value": "1","label": "年度报告"}],
             "nearMode": "0",
             "accountDatas": [],
             "enterpriseType": 0,
             "SearchHistoryRecord": 0,
             "searchId": "5df270e3a7565e7a9f89b4f699bd4b0b"
            }
        data = json.dumps(data)
        headers = {
                "Host": "www.jianweidata.com",
                "Connection": "keep-alive",
                "Content-Length": "921",
                "Accept": "*/*",
                "Sec-Fetch-Dest": "empty",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
                "Content-Type": "application/json",
                "Origin": "https://www.jianweidata.com",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Referer": "https://www.jianweidata.com/",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9"
            }
        resp = requests.post(url=url, data=data, headers=headers)
        status_code = resp.status_code
        if status_code == 200:
            resp_dict = json.loads(resp.text)
            return resp_dict
        else:
            print('请求结果异常，请求响应代码为：{}'.format(status_code))
            return
    else:
        print('传入的pagenum：{}不为int类型'.format(pagenum))


def main():
    #获取响应页面，并获取结果总数进而得到页数
    response = getHtml(1)
    total = response.get('Total')
    pagenums = int(total/20)+2

    #pagenums = 20

    #遍历所有页，获取结果
    for pagenum in range(1,pagenums):
        print('*'*50)
        resp = getHtml(pagenum=pagenum)
        print(resp)
        analyHtml(html=resp)

if __name__ == "__main__":
    main()
