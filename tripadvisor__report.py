#coding=utf-8
'''
功能：以爬取猫途鹰网站上的英文评论（以“慕田峪长城”为例）
网址：https://www.tripadvisor.cn/Attraction_Review-g294212-d325811-Reviews-Mutianyu_Great_Wall-Beijing.html
'''
#导入模块
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree

#1、需要爬取的为英文评论，猫途鹰支撑此网址进行英文类评论筛选，则最好采用post方式获取英文评论；
#2、英文评论中每条评论均有一个“更多”的按钮查看评论全部内容，则需要进一步分析获取每一条评论全部内容。


#获取英文评论内容
def get_reports():
    #获取评论响应结果
    urls = [
        'https://www.tripadvisor.cn/Attraction_Review-g294212-d325811-Reviews-or{}-Mutianyu_Great_Wall-Beijing.html'.format(str(i + 10)) for i in range(0, 10, 10)
    ]
    data = {
        'preferFriendReviews': 'FALSE',
        't': '',
        'q': '',
        'filterSeasons': '',
        'filterLang': 'en',
        'filterSafety': 'FALSE',
        'filterSegment': '',
        'trating': '',
        'reqNum': '1',
        'isLastPoll': 'false',
        'paramSeqId': '1',
        'waitTime': '107',
        'changeSet': 'REVIEW_LIST',
        'puid': 'Xkvrr8CoASkABrD8V34AAAGL'
    }
    headers = {
        'Accept': 'text/html, */*',
        'Connection': 'keep-alive',
        'Content-Length': '191',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'TART=%1%enc%3AsOCgP97OMc94qTI7BbqgvJQJCDUDFss0n3x%2FZ%2Fd6XM8rnz7FqGQc%2FLugm%2F%2F0288qOIAVHiKul%2B0%3D; TAUnique=%1%enc%3AtldHBELviqGpBw07J2agR%2Fh5NzRGtcROrG%2FndUeNzaA3Ld2Nq8Qi%2Fg%3D%3D; TASSK=enc%3AAJpg4anlEb%2Fy78qh4oqLBdI6%2BaDGUCf54WvbP2G3NacydYkpvvBNbaP78PeAJZq8hpjaN8qEGtpiCDa%2B%2Ff8mH2G9lEOxYgYdEi96%2FMH4X35EhZV8K6f3jQSERO%2FKDFTQYg%3D%3D; _ga=GA1.2.904448747.1548682673; _gid=GA1.2.1300052258.1548682673; _smt_uid=5c4f05b1.155ab2bd; __gads=ID=e479a7f803325efe:T=1548682674:S=ALNI_MbCp05Ak_tfFsAWIrbTOWSJYQE_EA; TATravelInfo=V2*AY.2019*AM.2*AD.10*DY.2019*DM.2*DD.11*A.2*MG.-1*HP.2*FL.3*DSM.1548687914272*RS.1; CommercePopunder=SuppressAll*1548687992996; TALanguage=ALL; ServerPool=A; VRMCID=%1%V1*id.16631*llp.%2F-m16631-a_ttcampaign%5C.MTYpc-a_ttgroup%5C.title*e.1549330640723; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C4%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CCCUVOwnPers%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7CCCUVOwnSess%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7C; TAReturnTo=%1%%2FAttraction_Review-g294212-d325811-Reviews-Mutianyu_Great_Wall-Beijing.html; roybatty=TNI1625!AJhFLb2y1T2wjWIj0nZ%2Fn2y4GflEeZBMemyC6d%2F8wchv1Dczm9RbSQQeA97E7bMrwRblS2I0%2BtTLucrkB5pBCrTH561lfiNtsd7ZC0i2bvNZ5SzdEJ6L9beTk6vyZ5ZAjSY4LM9oEmvAuOpXvVB5maxfbgx0XPutfzEN5uTmrJCo%2C1; TASession=%1%V2ID.09B9CACFFB2F6B5B99B3E1309F5F2BE0*SQ.24*MC.16631*LR.https%3A%2F%2Fsp0%5C.baidu%5C.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc%5C.php%3Fssl_s%3D1%26ssl_c%3Dssl1_1689740e32a%26h_search_ext%3D%257B%2522count%2522%253A4%252C%2522list%2522%253A%255B%257B%2522txt%2522%253A%2522%255Cu59dc%255Cu6210%255Cu52cb%255Cu88ab%255Cu7206%255Cu8d2a%255Cu6c61%2522%252C%2522cid%2522%253A%252246606222%2522%252C%2522sellv%2522%253A*LP.%2F-m16631-a_ttcampaign%5C.MTYpc-a_ttgroup%5C.title*LS.DemandLoadAjax*GR.41*TCPAR.97*TBR.65*EXEX.10*ABTR.89*PHTB.11*FS.48*CPU.4*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.zhCN*FA.1*DF.0*TRA.false*LD.325811; TAUD=LA-1548682670471-1*RDD-1-2019_01_28*HC-71023*HDD-5243681-2019_02_10.2019_02_11*LD-43273088-2019.2.10.2019.2.11*LG-43273090-2.1.F.',
        'Host': 'www.tripadvisor.cn',
        'Origin': 'https://www.tripadvisor.cn',
        'Referer': 'https://www.tripadvisor.cn/Attraction_Review-g294212-d325811-Reviews-Mutianyu_Great_Wall-Beijing.html',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36',
        'X-Puid': 'XE@utMCoCwwAAEmaUNMAAAAP',
        'X-Requested-With': 'XMLHttpRequest',
    }

    #分析不同分页的url，并利用各个url获取各个页面评论，具体如下
    for url in urls:
        response = requests.post(url=url, data=data, headers=headers)
        status_code = response.status_code
        if str(status_code) != '200':
            print('请求响应异常，请检查相关参数')

        else:
            html = response.text
            #获取评论更多中评论人id，方法一，利用etrr中xpath方式
            # elements = etree.HTML(response.text)
            # report_id = elements.xpath('//*[@class="reviewSelector"]/@data-reviewid')
            # reviewid = ",".join(report_id)
            # print(reviewid)

            #获取评论更多中评论人id，方法二，利用BeautifulSoup中find方式
            reviewid_list = []
            soup = BeautifulSoup(html, 'lxml')
            reports = soup.find_all('div', attrs={"class":"review-container"})
            for report in reports:
                report_id = report['data-reviewid']
                reviewid_list.append(report_id)
            reviewid = ",".join(reviewid_list)

            #调用获取全部评论的函数
            get_all_report(reviewid)



#获取点击“更多”后的全部评论
def get_all_report(reviews):
    url = 'https://www.tripadvisor.cn/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS_RESP&metaReferer='
    data = {
        'reviews': reviews,
        'contextChoice': 'DETAIL',
        'loadMtHeader': 'true',
        'haveJses': 'earlyRequireDefine,amdearly,promise-polyfill-standalone,global_error,long_lived_global,apg-Attraction_Review,apg-Attraction_Review-in,bootstrap,responsive-calendar-templates-dust-zh_CN,@ta/common.global,@ta/tracking.interactions,@ta/public.maps,@ta/overlays.pieces,@ta/overlays.shift,@ta/overlays.internal,@ta/overlays.attached-overlay,@ta/overlays.managers,@ta/overlays.attached-arrow-overlay,@ta/overlays.popover,social.share-cta,attractions.tab-bar-commerce,@ta/overlays.fullscreen-overlay,@ta/overlays.modal,attractions.attraction-detail-about-card,@ta/daodao.mobile-app-smartbutton,@ta/platform.import,@ta/platform.runtime,masthead_search_late_load,p13n_masthead_search__deferred__lateHandlers',
        'haveCsses': 'apg-Attraction_Review-in,responsive_calendars_control',
        'Action': 'install'
    }
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Connection': 'keep-alive',
        'Content-Length': '1069',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'TART=%1%enc%3AsOCgP97OMc94qTI7BbqgvJQJCDUDFss0n3x%2FZ%2Fd6XM8rnz7FqGQc%2FLugm%2F%2F0288qOIAVHiKul%2B0%3D; TAUnique=%1%enc%3AtldHBELviqGpBw07J2agR%2Fh5NzRGtcROrG%2FndUeNzaA3Ld2Nq8Qi%2Fg%3D%3D; TASSK=enc%3AAJpg4anlEb%2Fy78qh4oqLBdI6%2BaDGUCf54WvbP2G3NacydYkpvvBNbaP78PeAJZq8hpjaN8qEGtpiCDa%2B%2Ff8mH2G9lEOxYgYdEi96%2FMH4X35EhZV8K6f3jQSERO%2FKDFTQYg%3D%3D; _ga=GA1.2.904448747.1548682673; _gid=GA1.2.1300052258.1548682673; _smt_uid=5c4f05b1.155ab2bd; __gads=ID=e479a7f803325efe:T=1548682674:S=ALNI_MbCp05Ak_tfFsAWIrbTOWSJYQE_EA; CommercePopunder=SuppressAll*1548687992996; TALanguage=ALL; ServerPool=A; TATravelInfo=V2*AY.2019*AM.2*AD.10*DY.2019*DM.2*DD.11*A.2*MG.-1*HP.2*FL.3*DSM.1548731398056*RS.1; _gat_UA-79743238-4=1; VRMCID=%1%V1*id.16631*llp.%2F-m16631-a_ttcampaign%5C.MTYpc-a_ttgroup%5C.title*e.1549336282886; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C5%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CCCUVOwnPers%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPartPers%2C%2C-1%7CRestPremRPers%2C%2C-1%7CCCUVOwnSess%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7C; TAReturnTo=%1%%2FAttraction_Review-g294212-d325811-Reviews-Mutianyu_Great_Wall-Beijing.html; roybatty=TNI1625!ANG6fwAEw4MiYShLuTZ9N9WPeY6fUh4dRd78w9OaSBkvQxj%2F60hlYf6y0oPtxKiK3BS1eW2%2FOjsVDQO0MRIVGMNgdm214FfrygtGMgt1eh6uLbPio2a1wOeAgDDbGaFbpZWzO1gHlhqRrmTZtTIbmGKmi81WnuJvqgNNp%2Fu3wlRa%2C1; TASession=%1%V2ID.09B9CACFFB2F6B5B99B3E1309F5F2BE0*SQ.76*MC.16631*LR.https%3A%2F%2Fsp0%5C.baidu%5C.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc%5C.php%3Fssl_s%3D1%26ssl_c%3Dssl1_1689740e32a%26h_search_ext%3D%257B%2522count%2522%253A4%252C%2522list%2522%253A%255B%257B%2522txt%2522%253A%2522%255Cu59dc%255Cu6210%255Cu52cb%255Cu88ab%255Cu7206%255Cu8d2a%255Cu6c61%2522%252C%2522cid%2522%253A%252246606222%2522%252C%2522sellv%2522%253A*LP.%2F-m16631-a_ttcampaign%5C.MTYpc-a_ttgroup%5C.title*LS.DemandLoadAjax*GR.41*TCPAR.97*TBR.65*EXEX.10*ABTR.89*PHTB.11*FS.48*CPU.4*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.ALL*FA.1*DF.0*MS.-1*RMS.-1*FLO.293920*TRA.false*LD.325811; TAUD=LA-1548682670471-1*RDD-1-2019_01_28*HC-48657123*HDD-48727532-2019_02_10.2019_02_11*LD-48857965-2019.2.10.2019.2.11*LG-48857967-2.1.F.',
        'Host': 'www.tripadvisor.cn',
        'Origin': 'https://www.tripadvisor.cn',
        'Referer': 'https://www.tripadvisor.cn/Attraction_Review-g294212-d325811-Reviews-Mutianyu_Great_Wall-Beijing.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'X-Puid': 'Xkw3EMCoASgABHnJHdQAAAAp',
        'X-Requested-With': 'XMLHttpRequest',
    }

    resp = requests.post(url=url, data=data, headers=headers)
    status_code = resp.status_code
    if str(status_code) != '200':
        print('请求响应异常，请检查相关参数')
    else:
        html = resp.text
        #print(html)
        soup = BeautifulSoup(html, 'lxml')
        report_alls = soup.find_all('p', attrs={"class": "partial_entry"})
        for report_all in report_alls:
            report_text = report_all.get_text()
            print(report_text)


if __name__ == "__main__":
    get_reports()