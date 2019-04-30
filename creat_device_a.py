# -*- coding=utf-8 -*-

import requests
from bs4 import BeautifulSoup

login_url = 'http://192.168.1.4:8000/accounts/login/'

# 会话对象让你能够跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie，
# 期间使用 urllib3 的 connection pooling 功能。所以如果你向同一主机发送多个请求，底层的 TCP 连接将会被重用，
# 从而带来显著的性能提升。
# http://docs.python-requests.org/zh_CN/latest/user/advanced.html
client = requests.session()

# 使用BS4分析页面
soup = BeautifulSoup(client.get(login_url).content, 'lxml')

# 找到页面中'csrfmiddlewaretoken'的值
csrftoken = soup.find('input', attrs={"type": "hidden", "name": "csrfmiddlewaretoken"}).get("value")

# 把用户名,密码,'csrfmiddlewaretoken'的值,通过POST的数据传输给登录页面
login_data = dict(username='test_user', password='luCKi1y18894', csrfmiddlewaretoken=csrftoken)
client.post(login_url, data=login_data)


add_device_url = 'http://www.qytang.com/add_device'
add_device_soup = BeautifulSoup(client.get(add_device_url).content, 'lxml')
add_device_csrftoken = add_device_soup.find('input', attrs={"type": "hidden", "name": "csrfmiddlewaretoken"}).get("value")

device_to_add = [{'name': 'device1',
                  'ip_address': '4.3.2.1',
                  'ro_community': '1232323',

                  'username': 'qwer',
                  'password': 'rewq',

                  'device_type': 'firewall'},
                 {'name': 'device2',
                  'ip_address': '4.3.2.2',
                  'ro_community': '123321',

                  'username': 'asdf',
                  'password': 'fdsa',

                  'device_type': 'firewall'},
                 ]

for device in device_to_add:
    device.update({'csrfmiddlewaretoken': add_device_csrftoken})
    r = client.post(add_device_url, data=device)
    print(r.status_code)

