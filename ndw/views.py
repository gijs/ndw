from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

def hello(request):
    return HttpResponse('Hello world!')