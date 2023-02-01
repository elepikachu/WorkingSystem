from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import escape_uri_path
from django.core.paginator import Paginator
from .models import Project, ProjectLog
from django.shortcuts import render
from io import BytesIO

import pandas as pd
import datetime
import json


VERSION = '项目管理系统 1.0.0'


# -------------------------------------------------------------
# 函数名： get_ip
# 功能： 获取电脑主机ip
# -------------------------------------------------------------
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# -------------------------------------------------------------
# 函数名： project_view
# 功能： 项目管理系统首页
# -------------------------------------------------------------
def project_view(request):
    dic = {'ver': VERSION}
    return render(request, 'project/project.html', dic)


# -------------------------------------------------------------
# 函数名： submit_view
# 功能： 提交模式
# -------------------------------------------------------------
def submit_view(request):
    if request.method == 'GET':
        date = datetime.date.today()
        datee = date + datetime.timedelta(weeks=1)
        date1 = date.strftime('%Y-%m-%d')
        date2 = datee.strftime('%Y-%m-%d')
        if request.COOKIES.get('person', '') != '':
            psn = request.COOKIES.get('person', '')
            psn = json.loads(psn)
            grp = request.COOKIES.get('group', '')
            grp = json.loads(grp)
        else:
            psn = ''
            grp = ''
        dic = {'ver': VERSION, 'date1': date1, 'date2': date2, 'psn': psn, 'grp': grp}
        return render(request, 'project/projectsubmit.html', dic)
    elif request.method == 'POST':
        if 'sub' in request.POST:
            name = request.POST['name']
            person = request.POST['person']
            group = request.POST['group']
            date = request.POST['date']
            enddate = request.POST['enddate']
            detail = request.POST['detail']
            classification = request.POST['classification']
            if Project.objects.exists():
                id = Project.objects.latest('id').id + 1
            else:
                id = 1
            Project.objects.create(id=id, name=name, person=person, group=group, date=date, enddate=enddate,
                                   detail=detail, classification=classification, finish=0)
            if ProjectLog.objects.exists():
                idx = ProjectLog.objects.latest('id').id
            else:
                idx = 0
            ProjectLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='insert',
                                      other='%s-%s-%s-%s%%' % (person, name, detail, '0'))
            res = HttpResponseRedirect('/project/manage?page=1')
            person = json.dumps(person)
            group = json.dumps(group)
            res.set_cookie(key='person', value=person, max_age=3600 * 24 * 30)
            res.set_cookie(key='group', value=group, max_age=3600 * 24 * 30)
            return res


# -------------------------------------------------------------
# 函数名： manage_view
# 功能： 管理模式
# -------------------------------------------------------------
def manage_view(request):
    if request.method == 'GET':
        if 'st' in request.GET:
            if request.GET['grp'] == "全部":
                all_data = Project.objects.filter(date__gte=request.GET['st'], date__lte=request.GET['et'])
            else:
                all_data = Project.objects.filter(date__gte=request.GET['st'], date__lte=request.GET['et'], group__exact=request.GET['grp'])
        else:
            all_data = Project.objects.all()
            all_data = all_data[::-1]
        page_num = request.GET.get('page', 1)
        paginator = Paginator(all_data, 30)
        c_page = paginator.page(int(page_num))
        ver = VERSION
        date = datetime.date.today()
        datee = date - datetime.timedelta(weeks=1)
        date1 = datee.strftime('%Y-%m-%d')
        date2 = date.strftime('%Y-%m-%d')
        groupbox = ['全部']
        for item in all_data:
            if item.group not in groupbox:
                groupbox.append(item.group)
        return render(request, 'project/projectmanage.html', locals())
    elif request.method == 'POST':
        if 'del' in request.POST:
            return HttpResponseRedirect('/project/batch')
        if 'self' in request.POST:
            return HttpResponseRedirect('/project/personal')
        if 'pri' in request.POST:
            if request.POST['grp'] == "全部":
                all_data = Project.objects.filter(date__gte=request.POST['date1'], date__lte=request.POST['date2'])
                name = f'项目完成情况.xlsx'
            else:
                all_data = Project.objects.filter(date__gte=request.POST['date1'], date__lte=request.POST['date2'],
                                                  group__exact=request.POST['grp'])
                name = f'%s项目完成情况.xlsx' % request.POST['grp']
            #all_data = all_data[::-1]
            data_list = all_data.values_list()
            response = create_excel(data_list, name)
            return response
        if 'unfit' in request.POST:
            return HttpResponseRedirect('/project/manage?page=1')
        if 'fit' in request.POST:
            st = request.POST['date1']
            et = request.POST['date2']
            grp = request.POST['grp']
            return HttpResponseRedirect('/project/manage?page=1&st=%s&et=%s&grp=%s' % (st, et, grp))


# -------------------------------------------------------------
# 函数名： update_project
# 功能： 数据行更新
# -------------------------------------------------------------
def update_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)

    except Exception as e:
        print('--update error is %s' % e)
        return HttpResponse('--The project is not existed!!--')
    if request.method == 'GET':
        date1 = project.date.strftime('%Y-%m-%d')
        date2 = project.enddate.strftime('%Y-%m-%d')
        ver = VERSION
        return render(request, 'project/projectupdate.html', locals())
    elif request.method == 'POST':
        if "upd" in request.POST:
            name = request.POST['name']
            person = request.POST['person']
            group = request.POST['group']
            date = request.POST['date']
            enddate = request.POST['enddate']
            detail = request.POST['detail']
            classification = request.POST['classification']
            finish = request.POST['finish']
            project.name = name
            project.person = person
            project.group = group
            project.date = date
            project.enddate = enddate
            project.detail = detail
            project.classification = classification
            project.finish = finish
            project.save()
            if ProjectLog.objects.exists():
                idx = ProjectLog.objects.latest('id').id
            else:
                idx = 0
            ProjectLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='update',
                                      other='%s-%s-%s-%s%%' % (person, name, detail, finish))
            return HttpResponseRedirect('/project/manage?page=1')
        elif "back" in request.POST:
            return HttpResponseRedirect('/project/manage?page=1')


# -------------------------------------------------------------
# 函数名： delete_project
# 功能： 数据行删除
# -------------------------------------------------------------
def delete_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        name = project.name
        person = project.person
        project.delete()
        if ProjectLog.objects.exists():
            idx = ProjectLog.objects.latest('id').id
        else:
            idx = 0
        ProjectLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='delete',
                                  other='%s-%s' % (name, person))
        return HttpResponseRedirect('/project/manage?page=1')
    except Exception as e:
        print('--delete error is %s' % e)
        return HttpResponse('--Delete failed!!--')


# -------------------------------------------------------------
# 函数名： batch_view
# 功能： 批量删除
# -------------------------------------------------------------
def batch_view(request):
    if request.method == 'GET':
        date = datetime.date.today()
        datee = date + datetime.timedelta(weeks=1)
        date1 = date.strftime('%Y-%m-%d')
        date2 = datee.strftime('%Y-%m-%d')
        ver = VERSION
        return render(request, 'project/projectdelete.html', locals())
    elif request.method == 'POST':
        if 'delall' in request.POST:
            all_data = Project.objects.all()
            all_data.delete()
            if ProjectLog.objects.exists():
                idx = ProjectLog.objects.latest('id').id
            else:
                idx = 0
            ProjectLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='delete',
                                      other='ALL')
            return HttpResponseRedirect('/project/manage?page=1')
        elif 'deldate' in request.POST:
            date1 = request.POST['date1']
            date2 = request.POST['date2']
            all_data = Project.objects.filter(date__gte=date1, date__lte=date2)
            all_data.delete()
            if ProjectLog.objects.exists():
                idx = ProjectLog.objects.latest('id').id
            else:
                idx = 0
            ProjectLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='delete',
                                      other='all in %s-%s' % (date1, date2))
            return HttpResponseRedirect('/project/manage?page=1')
        elif 'delend' in request.POST:
            date1 = request.POST['date1']
            date2 = request.POST['date2']
            all_data = Project.objects.filter(enddate__gte=date1, enddate__lte=date2)
            all_data.delete()
            if ProjectLog.objects.exists():
                idx = ProjectLog.objects.latest('id').id
            else:
                idx = 0
            ProjectLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='delete',
                                      other='all in %s-%s' % (date1, date2))
            return HttpResponseRedirect('/project/manage?page=1')


# -------------------------------------------------------------
# 函数名： personal_view
# 功能： 个人数据操作
# -------------------------------------------------------------
def personal_view(request):
    if request.method == 'GET':
        ver = VERSION
        if request.COOKIES.get('person', '') != '':
            psn = request.COOKIES.get('person', '')
            psn = json.loads(psn)
            unfinished = Project.objects.filter(person__exact=psn).exclude(finish__exact=100)
            unfinished = unfinished[::-1]
            length = len(unfinished)
            finished = Project.objects.filter(person__exact=psn, finish__exact=100)
            finished = finished[::-1]
            return render(request, 'project/projectself.html', locals())
        else:
            namebox = []
            all_data = Project.objects.all()
            for item in all_data:
                if item.person not in namebox:
                    namebox.append(item.person)
            return render(request, 'project/projectperson.html', locals())
    if request.method == 'POST':
        if 'ret' in request.POST:
            res = HttpResponseRedirect('/project/personal')
            res.delete_cookie('person')
            return res
        if 'nm' in request.POST:
            res = HttpResponseRedirect('/project/personal')
            person = json.dumps(request.POST['nam'])
            res.set_cookie(key='person', value=person, max_age=3600 * 24 * 30)
            return res
        if 'prt' in request.POST:
            psn = request.COOKIES.get('person', '')
            psn = json.loads(psn)
            all_data = Project.objects.filter(person__exact=psn)
            data_list = all_data.values_list()
            name = f'项目完成情况-%s.xlsx' % psn
            response = create_excel(data_list, name)
            return response


# -------------------------------------------------------------
# 函数名： create_excel
# 功能： 打印excel
# -------------------------------------------------------------
def create_excel(data_list, name):
    data = pd.DataFrame(data_list)
    data.columns = ['id', '项目名', '项目开始时间', '预计完成时间', '项目组', '完成人', '分类', '备注', '进展(%)']
    output = BytesIO()  # 转二进制流
    data.to_excel(output, index=False)
    output.seek(0)  # 重新定位到开始
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = "attachment;filename=%s" % escape_uri_path(name)
    response.write(output.getvalue())
    output.close()
    return response


# -------------------------------------------------------------
# 函数名： log_view
# 功能： 日志界面
# -------------------------------------------------------------
def log_view(request):
    if request.method == 'GET':
        all_log = ProjectLog.objects.all()
        all_log = all_log[::-1]
        dic = {'ver': VERSION, 'data': all_log}
        return render(request, 'project/projectlog.html', dic)
