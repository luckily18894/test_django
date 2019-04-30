# -*- coding=utf-8 -*-

from ldap3 import Server, Connection, AUTO_BIND_NO_TLS, ALL, MODIFY_REPLACE
from datetime import timezone, timedelta, datetime, date
from dateutil import parser
import pinyin
from random import randint, choice
import string


username = 'luckily18894'
password = 'luCKi1y18894'

tzutc_8 = timezone(timedelta(hours=8))

group_dn = 'CN=Domain Users,OU=QYT,DC=luckily18894,DC=com'


def random_password():  # 产生随机 固定格式的密码
    length = randint(3, 4)
    first1 = str(choice(string.digits))
    first2 = choice(string.ascii_letters).upper()
    first3 = choice(string.ascii_letters).lower()
    first4 = choice('.-')
    lastpassword = ''.join(choice(string.ascii_letters + string.digits) for i in range(length))
    return first1 + first2 + first3 + first4 + lastpassword


server = Server('ldap://192.168.1.15', get_info=ALL, use_ssl=True)


def get_user_group(username, password):
    # 返回用户属于的组与用户名
    try:
        # 连接服务器
        c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=True, check_names=True, user="luckily18894\\"+username, password=password)
        # 提取域qytang.com, 用户的memberOf,sn和department信息
        c.search(search_base='dc=luckily18894,dc=com', search_filter='(&(samAccountName=' + username + '))', attributes=['memberOf', 'sn', 'department'], paged_size=5)
        # 返回获取的memberOf,sn和department信息
        return c.response[0]['dn'], c.response[0]['attributes']['memberOf'], c.response[0]['attributes']['sn'], c.response[0]['attributes']['department']
        # return c.response
    except Exception as e:
        print(e)
        return None


def get_group_users(user_dn):
    # 返回属于组的用户
    users_list = []
    try:
        # 连接服务器
        c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=True, check_names=True, user="qytang\\"+username, password=password)
        c.search(search_base=user_dn,
                 search_filter='(|(objectCategory=group)(objectCategory=user))',
                 search_scope='SUBTREE',
                 attributes=['member', 'objectClass', 'userAccountControl', 'sAMAccountName'],
                 size_limit=0)
        # print(c.entries[0])
        for user in c.entries[0].member:
            users_list.append(user)
        return users_list

    except Exception:
        return None


def disable_user(user_dn):
    # 禁用用户
    try:
        c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=False, check_names=True, user="qytang\\"+username, password=password)
        c.modify(user_dn,
                 {'userAccountControl': [(MODIFY_REPLACE, [514])]})

    except Exception as e:
        print(e)
        return None


def enable_user(user_dn):
    # 激活用户
    try:
        c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=False, check_names=True, user="qytang\\"+username, password=password)
        c.modify(user_dn,
                 {'userAccountControl': [(MODIFY_REPLACE, [512])]})

    except Exception as e:
        print(e)
        return None


def get_user_attributes(cn):
    # 512 = Enabled
    # 514 = Disabled
    # 66048 = Enabled, password never expires
    # 66050 = Disabled, password never expires

    # 返回用户属性
    try:
        # 连接服务器
        c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=True, check_names=True, user="qytang\\"+username, password=password)
        c.search(search_base=cn,
                 search_filter='(objectCategory=user)',
                 attributes=['sAMAccountName', 'createTimeStamp', 'accountExpires', 'userAccountControl', 'memberOf', 'objectClass', 'pwdLastSet'],
                 size_limit=1)
        # print(c.entries[0].createTimeStamp)
        return c.entries[0]

    except Exception as e:
        print(e)
        return None


def if_user_expire_and_active(cn):
    # 判断用户是否过期
    cn_result = get_user_attributes(cn)
    userAccountControl = cn_result.userAccountControl
    createTimeStamp = cn_result.createTimeStamp
    delta_date = datetime.now().replace(tzinfo=tzutc_8) - createTimeStamp.value
    if (delta_date.days > 365*1.5 and userAccountControl == 512) or (delta_date.days > 365*1.5 and userAccountControl == 66048):
        return cn
    else:
        return None


# 添加域账号
def add_ad_user(xingming, phone, qq, mail, start_time, type='sec_ccie'):
    # 转换汉字到拼音
    hanzi = xingming
    try:
        xingming = pinyin.get(xingming, format='strip')
    except Exception:
        pass
    # 根据类型找到组
    if type == 'sec_ccie' or type == 'sec_ccnp' or type == 'sec_ccnp1111':
        group_dn = 'CN=npsecremotelab, OU=NPSEC_RemoteLab, OU=Security, OU=QYT, DC=qytang,DC=com'
        display_name = 'rsec-' + xingming

    user_cn = 'cn=' + display_name + ',' + ','.join(group_dn.split(',')[1:])
    # 判断是否重名, 如果重名就产生新的用户名
    while True:
        try:
            display_name = get_user_attributes(user_cn).sAMAccountName
            name_randint = str(randint(1, 100))
            display_name = display_name.value + name_randint
            user_cn = 'cn=' + display_name + ',' + ','.join(group_dn.split(',')[1:])
        except Exception:
            break
    try:
        # 连接服务器
        c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=False, check_names=True, user="qytang\\"+username, password=password)
        if type == 'sec_ccie' or type == 'sec_ccnp':
            end_time = parser.parse(start_time) + timedelta(days=365*1.5)
        elif type == 'sec_ccnp1111':
            end_time = parser.parse(start_time) + timedelta(days=180)
        c.add(user_cn, attributes={'objectClass':  ['top', 'person', 'organizationalPerson', 'user'],
                                   # 用户名
                                   'sAMAccountName': display_name,
                                   # 用户名
                                   'userPrincipalName': display_name,
                                   # 有效期一年半
                                   'accountExpires': end_time,
                                   # 姓为中文的汉字
                                   'sn': hanzi,
                                   # 显示名为用户名
                                   'displayName': display_name,
                                   # 电话
                                   "telephoneNumber": phone,
                                   # 邮件
                                   "Mail": mail,
                                   # QQ
                                   "description": hanzi + qq
                                   })
        # 添加用户到组
        c.extend.microsoft.add_members_to_groups(user_cn, group_dn)
        # 产生随机密码
        rand_pass = random_password()
        # 创建用户初始密码
        c.extend.microsoft.modify_password(user_cn, new_password=rand_pass)
        # 激活用户
        c.modify(user_cn, {'userAccountControl': [(MODIFY_REPLACE, [544])]})
        # 发送通知客户邮件

        return display_name, rand_pass

    except Exception:
        return None


def disable_expired_users_by_group(group):
    # 根据组禁用过期账号
    users_list = get_group_users(group)
    need_disable_users_list = []
    for user in users_list:
        if if_user_expire_and_active(user):
            need_disable_users_list.append(user)
            disable_user(user)
    print(need_disable_users_list)


# 从用户组用删除用户
def remove_user_from_group(user_dn, group_dn):
    c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=False, check_names=True,user="qytang\\" + username, password=password)
    c.extend.microsoft.remove_members_from_groups(user_dn, group_dn)


# 添加用户到用户组
def add_user_to_group(user_dn, group_dn):
    c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=False, check_names=True,user="qytang\\" + username, password=password)
    c.extend.microsoft.add_members_to_groups(user_dn, group_dn)


# 修改用户密码
def change_user_password(user_dn, newpass=''):
    c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=False, check_names=True,user="qytang\\" + username, password=password)
    if newpass == '':
        newpass = random_password()

    c.extend.microsoft.modify_password(user_dn, newpass)
    return newpass


def overtime_user_accountexpires(user_dn, days=180):
    # 修改有效期
    try:
        c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=False, check_names=True, user="qytang\\"+username, password=password)

        c.modify(user_dn,
                 {'accountExpires': [(MODIFY_REPLACE, [datetime.now() + timedelta(days=days)])]})

    except Exception as e:
        print(e)
        return None


def set_user_accountexpires(user_dn, datetimeobj):
    # 修改有效期
    try:
        c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=False, check_names=True, user="qytang\\"+username, password=password)

        c.modify(user_dn,
                 {'accountExpires': [(MODIFY_REPLACE, [datetimeobj])]})

    except Exception as e:
        print(e)
        return None


def get_user_accountexpires(user_cn):
    return get_user_attributes(user_cn).accountExpires.value


def delete_user(cn):
    try:
        # 连接服务器
        c = Connection(server, auto_bind=True, user="qytang\\"+username, password=password)

        c.delete(cn)

        return c.result

    except Exception:
        return None


def get_username_dn(samaccountname):
    for x in get_group_users('CN=npsecremotelab,OU=NPSEC_RemoteLab,OU=Security,OU=QYT,DC=qytang,DC=com'):
        try:
            if str(get_user_attributes(x).sAMAccountName) == samaccountname:
                return x
        except AttributeError:
            pass

    else:
        return None


def delete_ccnp_user_by_username(samaccountname):
    user_dn = get_username_dn(samaccountname)
    if not user_dn:
        print('用户未找到')
        return
    delete_user(user_dn)


if __name__ == "__main__":
    # print(random_password())
    print(get_user_group('test_user', 'luCKi1y18894'))
