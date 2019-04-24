# -*- coding=utf-8 -*-

from django.shortcuts import render
from testdjangodb.forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


def loginweb(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return HttpResponseRedirect(next_url)

        else:
            return render(request, 'registration/login.html', {'form': form, 'error': '用户名或密码错误'})
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        else:
            form = UserForm()
            return render(request, 'registration/login.html', {'form': form})


def logoutweb(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')

