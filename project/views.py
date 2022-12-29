from django.shortcuts import render

# Create your views here.

VERSION = '项目管理系统 1.0.0'


def project_view(request):
    dic = {'ver': VERSION}
    return render(request, 'project.html', dic)


def submit_view(request):
    pass


def manage_view(request):
    pass


def log_view(request):
    pass
