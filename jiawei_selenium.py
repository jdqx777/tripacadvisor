#coding=utf-8
'''
功能：见微网上，获取上市公司信息；查询条件：时间、公告类型、关键词；
网址：https://www.jianweidata.com/
其他：该方式采用selenium模拟浏览器操作，来进行登录查询并获取结果；
'''

#导入模块
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import openpyxl
import sys
import traceback

def isElementExist_byXpath(driver,xpath):
    #利用xpath判断元素是否存在，存在返回True，不存在返回False
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except Exception as e:
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)
        return False

def isElementExist_byId(driver,id):
    #利用id判断元素是否存在，存在返回True，不存在返回False
    try:
        driver.find_element_by_id(id)
        return True
    except Exception as e:
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)
        return False

def downloadPdf(url,root,filename):
    #下载pdf文件，url为pdf链接，root为下载保存路径，filename为文件名
    try:
        resp = requests.get(url)
        with open(root+filename, 'wb+') as f:
            f.write(resp.content)
        print('利用{}下载{}文件成功'.format(url, filename))
    except Exception as e:
        print('利用{}下载{}文件失败'.format(url, filename))
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)


def analyzeHtml(html):
    # 分析页面，获取相应数据并写入excel文件
    # 转换为beautifulsoup格式
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find('div', attrs={'id': 'div_results'}).find_all('div', attrs={'class': 'search-result-area real'})

    # 打开excel文件
    try:
        wb = openpyxl.load_workbook('simple.xlsx')
        ws = wb.active

        #遍历
        for result in results:
            title = result.find('a', attrs={'class': 'filing-title'}).get('title')
            code = result.find('a', attrs={'class': 'btn btn-default filing-stock border-jw'}).text
            url = result.find('a', attrs={'class': 'filing-source iconfont icon-yuan'}).get('href')
            print(code, '   ', title)
            #写入excel
            ws.append([code, title, url])
            time.sleep(1)

            downloadPdf(url=url, root='', filename=title+'.pdf')
            time.sleep(1)

        wb.save('simple.xlsx')

    except Exception as e:
        exc_type, exc_value, exc_obj = sys.exc_info()
        traceback.print_tb(exc_obj)

def switchPage(browser):
    #遍历当前屏中的各页
    for i in range(2,12,1):

        #利用xpath遍历每一页
        xpath = '//*[@id="div_pages"]/a[{}]'.format(i)
        #判断xpath是否存在
        flag = isElementExist_byXpath(driver=browser, xpath=xpath)
        if flag:
            page = browser.find_element_by_xpath(xpath)
            browser.execute_script("arguments[0].click();", page)

            #利用页面分析函数，获取当页内容
            analyzeHtml(html=browser.page_source)
            time.sleep(2)

        else:
            print('利用xpath：{}找不到存在的元素，退出'.format(xpath))
            break

def getAllPage(browser):
    #遍历所有屏
    for i in range(1,501,1):
        #利用下一屏id遍历
        id = 'btn_loadNext'
        #判断id是否存在
        flag = isElementExist_byId(driver=browser, id=id)
        if flag:
            nextlist = browser.find_element_by_id(id)
            browser.execute_script("arguments[0].click();", nextlist)

            #获取当屏第一个页面数字
            soup = BeautifulSoup(browser.page_source, 'lxml')
            page_num = soup.find('div', attrs={'id': 'div_pages'}).findAll('a')[1].text
            if page_num.isdigit():
                print(page_num)
                time.sleep(2)

                #获取当前屏中每一页数据
                switchPage(browser=browser)
            else:
                print('此屏获取不到页面，退出')
                break

        else:
            print('利用id：{}已找不到元素'.format(id))
            break

def main():

    #进入网站
    browser = webdriver.Chrome(executable_path='chromedriver_80.0.3\chromedriver.exe')
    url = 'https://www.jianweidata.com/'
    browser.get(url)
    time.sleep(2)

    #用户名密码登录
    username = '18363992707'
    password = 'jdqx0812'
    browser.find_element_by_id('input_loginUid').send_keys(username)
    time.sleep(2)
    browser.find_element_by_id('input_loginPwd').send_keys(password)
    time.sleep(2)
    browser.find_element_by_id('btn_login').click()
    time.sleep(2)

    #选择年度报告
    browser.find_element_by_xpath('//*[@id="div_search_inputs"]/div[6]/a[2]').click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="div_notice_filter_rank1"]/div[9]/a/span[1]').click()
    time.sleep(2)
    browser.find_element_by_id('btn_sureFilter').click()
    time.sleep(2)

    #选择条件
    browser.find_element_by_id('input_subtitle_must').send_keys('中国')
    browser.find_element_by_xpath('//*[@id="btn_search"]').click()


    #选择时间范围(采用先清空数据后填充时间方式)
    input_date = browser.find_element_by_id("input_date")
    input_date.clear()
    start_end_time = '2019/09/01 - 2020/01/01'
    browser.find_element_by_id('input_date').send_keys(start_end_time)
    time.sleep(2)
    #print('时间范围选择完成----------------------------------------------------------')

    #输入关键字，并进行搜索
    key_word = '套期保值'
    browser.find_element_by_id('input_content_must').send_keys(key_word)
    time.sleep(2)
    browser.find_element_by_id('btn_search')
    time.sleep(2)

    #点击首屏，获取各页结果
    browser.find_element_by_id('btn_loadFirst').click()
    time.sleep(2)
    switchPage(browser=browser)

    #获取后面多屏结果
    getAllPage(browser=browser)

if __name__ == "__main__":
    main()