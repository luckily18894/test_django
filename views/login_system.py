# -*- coding=utf-8 -*-

from django.shortcuts import render
from testdjangodb.forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from views.ldap_login import get_user_group


# def loginweb(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = authenticate(username=username, password=password)
#         if user is not None and user.is_active:
#             login(request, user)
#             next_url = request.GET.get('next', '/')
#             return HttpResponseRedirect(next_url)
#
#         else:
#             return render(request, 'registration/login.html', {'form': form, 'error': '用户名或密码错误'})
#     else:
#         if request.user.is_authenticated:
#             return HttpResponseRedirect('/')
#
#         else:
#             form = UserForm()
#             return render(request, 'registration/login.html', {'form': form})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip.strip()


# 此处应该用数据库来找到映射关系
department_map = {'CN=qytanggroup,OU=QYT,DC=qytang,DC=com': 'qytanggroup'}


def loginweb(request):
    if request.method == 'POST':
        # 获取客户提交的Form内容
        form = UserForm(request.POST)
        # 提取用户名和密码
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        clientip = get_client_ip(request)
        # 如果客户没有输入用户名或者密码, 就提示客户错误信息
        if not username or not password:
            return render(request, 'registration/login.html', {'form': form, 'error': '用户名或密码不能为空!'})
        else:
            ldap_result = get_user_group(username, password)
            if not ldap_result:
                # 返回'用户名或者密码错误！'的信息给客户
                return render(request, 'registration/login.html', {'form': form, 'error': '用户名或者密码错误！'})
            else:
                # 会话变量
                # department = department_map.get(ldap_result[1][-1])
                # department = ldap_result[1][-1]
                request.session['username'] = username
                request.session['department'] = ldap_result[-1]
                request.session['user_sn'] = ldap_result[2]
                request.session['login_status'] = True
                request.session['ip'] = clientip
                next_url = request.GET.get('next', '/')
                return HttpResponseRedirect(next_url)

    else:  # 如果客户使用GET访问,并且客户已经认证,重定向他到主页
        if request.session.get('login_status', ''):
            return HttpResponseRedirect('/')

        else:  # 如果客户使用GET访问, 给他展示登录页面
            form = UserForm()
            return render(request, 'registration/login.html', {'form': form})


# def logoutweb(request):
#     logout(request)
#     return HttpResponseRedirect('/accounts/login')


# 登出操作,登出成功后,显示登录页面
def logoutweb(request):
    try:
        request.session.clear()  # 清除会话变量, 会话变量中保存有登录信息!
    except Exception:
        pass
    # 重定向登出客户到登录页面
    return HttpResponseRedirect('/accounts/login')

