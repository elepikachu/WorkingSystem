from django.http import HttpResponse
from django.shortcuts import render
from .models import SOFCTest

import numpy as np
from matplotlib import pyplot as plt
import time


VERSION = "化工计算器"


def main_view(request):
    dic = {'ver': VERSION}
    return render(request, 'cheapp/cheapp.html', dic)


def test_view(request):
    all_data = SOFCTest.objects.all()
    dic = {'ver': VERSION, 'data': all_data}
    return render(request, 'cheapp/test.html', dic)


def test_view_add(request):
    dic = {'ver': VERSION}
    return render(request, 'cheapp/test.html', dic)


def test_view_del(request, index):
    dic = {'ver': VERSION}
    return render(request, 'cheapp/test.html', dic)


def test_view_upd(request, index):
    dic = {'ver': VERSION}
    return render(request, 'cheapp/test.html', dic)


def test_view_det(request, index):
    dic = {'ver': VERSION}
    return render(request, 'cheapp/test.html', dic)