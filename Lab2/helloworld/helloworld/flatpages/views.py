#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

#def home(request):
#    return HttpResponse('Привет, Мир!')


def home(request):
    return render(request, 'index.html', {})
#    return render(request, 'static_handler.html', {'STATIC_URL':'./static/'})