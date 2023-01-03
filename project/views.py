from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Project, ProjectLog
import datetime
import json

# Create your views here.

VERSION = '项目管理系统 1.0.0'


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def project_view(request):
    dic = {'ver': VERSION}
    return render(request, 'project.html', dic)


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
        return render(request, 'projectsubmit.html', dic)
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
                                   detail=detail, classification=classification, finish=False)
            if ProjectLog.objects.exists():
                idx = ProjectLog.objects.latest('id').id
            else:
                idx = 0
            ProjectLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='insert',
                                      other='%s-%s-%s' % (name, person, detail))
            obj = HttpResponseRedirect('/project/manage')
            person = json.dumps(person)
            group = json.dumps(group)
            obj.set_cookie(key='person', value=person, max_age=3600 * 24 * 30)
            obj.set_cookie(key='group', value=group, max_age=3600 * 24 * 30)
            return obj


def manage_view(request):
    if request.method == 'GET':
        all_data = Project.objects.all()
        dic = {'ver': VERSION, 'data': all_data}
        return render(request, 'projectmanage.html', dic)


def update_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)

    except Exception as e:
        print('--update error is %s' % e)
        return HttpResponse('--The project is not existed!!--')
    if request.method == 'GET':
        date1 = project.date.strftime('%Y-%m-%d')
        date2 = project.enddate.strftime('%Y-%m-%d')
        return render(request, 'projectupdate.html', locals())
    elif request.method == 'POST':
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
                                  other='%s-%s-%s' % (name, person, detail))
        return HttpResponseRedirect('/project/manage')


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
        return HttpResponseRedirect('/project/manage')
    except Exception as e:
        print('--delete error is %s' % e)
        return HttpResponse('--Delete failed!!--')


def log_view(request):
    if request.method == 'GET':
        all_log = ProjectLog.objects.all()
        dic = {'ver': VERSION, 'data': all_log}
        return render(request, 'projectlog.html', dic)
