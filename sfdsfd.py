# -*- coding=utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
import json


# 3
header_dict = {}
header_txt = open('header.txt')
for header in header_txt.readlines():
    # print(header)
    key, val = header.strip().split(':')
    header_dict[key.strip()] = val.strip()
# print(header_dict)

r = requests.get('http://www.qytang.com/Public/home/images/logo.png', headers=header_dict)
i = r.content
File = open('qytang_logo.png', 'wb')
File.write(i)
File.close()


# 2
# res = requests.get('http://192.168.1.111/level/15/exec/-/show/ip/interface/brief/CR', auth=HTTPBasicAuth('admin', 'admin'))
# print(res.text)


# 1
# res = requests.get('http://192.168.1.103:8000/device_monitor/pie/3/')
# a = json.loads(res.text)
# print(a)
#
# for x in a:
#     print(x, ':', a[x])



