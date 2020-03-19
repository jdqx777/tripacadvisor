#coding=utf-8
import json

dict = {'SearchId': None, 'TotalCompanyCardCount': 0, 'Total': 0, 'Took': 0, 'DbTook': 0, 'Hits': [], 'GroupKey': None, 'GroupHits': [], 'Aggregations': [], 'HighlightFilters': [], 'TitleHighlights': [], 'ContentHighlights': [], 'IpoItems': [], 'Message': None, 'NickName': None, 'PaymentStatus': '0', 'SubscriptionLimit': '3', 'CanPay': True, 'ExpireTime': '2020-03-14', 'ResponseCode': 888, 'ResponseMessage': 'success', 'Token': 'y64Wol%2bu4NHIoj1YpW%2bMzwDJSW9F5k3sCVXFUyKF1VgR4LvmTfRisvnT2GLRq7k4cckH1IlfqbFuNUUwoeT7HcmA7qMKHVnMqDcCGsA2LlimzJzdl3qO4D6EI6KLRod9%2fz6RS8CfctGRlai8Vu%2fdkA%3d%3d', 'CommonSession': None}

for k,v in dict.items():
    print(k,'   ',v)

