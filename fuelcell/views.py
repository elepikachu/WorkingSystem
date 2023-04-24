from django.http import HttpResponse
from django.shortcuts import render
from .models import SOFCTest

import numpy as np
from matplotlib import pyplot as plt
import time


VERSION = "SOFC测试工具"


def main_view(request):
    dic = {'ver': VERSION}
    return render(request, 'fuelcell/fuelcell.html', dic)


def test_view(request):
    all_data = SOFCTest.objects.all()
    dic = {'ver': VERSION, 'data': all_data}
    return render(request, 'fuelcell/test.html', dic)


def test_view_add(request):
    dic = {'ver': VERSION}
    return render(request, 'fuelcell/test.html', dic)


def test_view_del(request, index):
    dic = {'ver': VERSION}
    return render(request, 'fuelcell/test.html', dic)


def test_view_upd(request, index):
    dic = {'ver': VERSION}
    return render(request, 'fuelcell/test.html', dic)


def test_view_det(request, index):
    dic = {'ver': VERSION}
    return render(request, 'fuelcell/test.html', dic)