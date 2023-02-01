from django.http import HttpResponse
from django.shortcuts import render
from win32com import client

import numpy as np
import pythoncom
import time


VERSION = "化工计算器"


def main_view(request):
    dic = {'ver': VERSION}
    return render(request, 'cheapp/cheapp.html', dic)


def doc_inf():
    pythoncom.CoInitialize()
    app = client.Dispatch('Word.Application')
    doc = app.Documents.Add()
    app.Visible = 1
    sel = app.selection
    sel.Text = 'Helloworld'
    res = sel()
    pythoncom.CoUninitialize()
    time.sleep(1)
    return res


def aspen_inf():
    pythoncom.CoInitialize()
    file_bkp = 'D:\\工作\\Aspen\\学习\\sofc_simple.bkp'
    Aspen = client.Dispatch('Apwn.Document.37.0')
    Aspen.InitFromArchive2(file_bkp)
    # 设置用户界面可见性
    Aspen.Visible = 0
    # 压制对话框弹出
    Aspen.SuppressDialogs = 1
    # 运行初始化
    Aspen.Reinit()
    # 运行模拟
    Aspen.Engine.Run2(1)
    # 每两秒检查是否运行
    while Aspen.Engine.IsRunning == 1:
        time.sleep(2)
    # 检查报错
    IsError = Aspen.Tree.FindNode('\Data\Results Summary\Run-Status\Output\PER_ERROR').value
    Aspen.Close()
    pythoncom.CoUninitialize()
    return


def test_view(request):
    result = test_func()
    return HttpResponse(result)


def test_func():
    res = aspen_inf()
    return res
