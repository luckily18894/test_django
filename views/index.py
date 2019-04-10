# -*- coding=utf-8 -*-

from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {'qyt_title': '强化班作业title',
                                          'qyt_body': '强化班作业body'})

