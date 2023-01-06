from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import escape_uri_path
from .models import Item, ItemLog
import datetime
import json
import pandas as pd
from io import BytesIO

# Create your views here.

VERSION = '物资采购系统 1.0.0'


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
def buy_view(request):
    dic = {'ver': VERSION}
    return render(request, 'buyitem/buy.html', dic)


# -------------------------------------------------------------
# 函数名： submit_view
# 功能： 提交模式
# -------------------------------------------------------------
def submit_view(request):
    if request.method == 'GET':
        if request.COOKIES.get('name', '') != '':
            psn = request.COOKIES.get('name', '')
            psn = json.loads(psn)
            grp = request.COOKIES.get('group', '')
            grp = json.loads(grp)
            tel = request.COOKIES.get('tel', '')
            tel = json.loads(tel)
            num = request.COOKIES.get('num', '')
            num = json.loads(num)
        else:
            psn = ''
            grp = ''
            tel = ''
            num = ''
        dic = {'ver': VERSION, 'psn': psn, 'grp': grp, 'tel':tel, 'num':num}
        return render(request, 'buyitem/buysubmit.html', dic)
    elif request.method == 'POST':
        if 'sub' in request.POST:
            name = request.POST['name']
            group = request.POST['group']
            tel = request.POST['tel']
            num = request.POST['num']
            good = request.POST['good']
            brand = request.POST['brand']
            quantity = request.POST['quantity']
            unit = request.POST['unit']
            info = request.POST['info']
            detail = request.POST['detail']
            if Item.objects.exists():
                id = Item.objects.latest('id').id + 1
            else:
                id = 1
            Item.objects.create(id=id, name=name, tel=tel, group=group, num=num, unit=unit,
                                detail=detail, quantity=quantity, brand=brand, info=info, finish=0)
            if ItemLog.objects.exists():
                idx = ItemLog.objects.latest('id').id
            else:
                idx = 0
            ItemLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='insert',
                                   other='%s-%s-%s-%s' % (name, good, num, 'false'))
            res = HttpResponseRedirect('/buyitem/manage?page=1')
            name = json.dumps(name)
            group = json.dumps(group)
            tel = json.dumps(tel)
            num = json.dumps(num)

            res.set_cookie(key='name', value=name, max_age=3600 * 24 * 30)
            res.set_cookie(key='group', value=group, max_age=3600 * 24 * 30)
            res.set_cookie(key='tel', value=tel, max_age=3600 * 24 * 30)
            res.set_cookie(key='num', value=num, max_age=3600 * 24 * 30)
            return res


# -------------------------------------------------------------
# 函数名： manage_view
# 功能： 管理模式
# -------------------------------------------------------------
def manage_view(request):
    if request.method == 'GET':
        if 'num' in request.GET:
            if request.GET['grp'] == "全部":
                all_data = Item.objects.filter(num__exact=request.GET['num'])
            else:
                all_data = Item.objects.filter(num__exact=request.GET['num'], group__exact=request.GET['grp'])
        else:
            all_data = Item.objects.all()
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
        return render(request, 'buyitem/buymanage.html', locals())
    elif request.method == 'POST':
        if 'del' in request.POST:
            return HttpResponseRedirect('/buyitem/batch')
        if 'self' in request.POST:
            return HttpResponseRedirect('/buyitem/personal')
        if 'pri' in request.POST:
            if request.POST['grp'] == "全部":
                all_data = Item.objects.filter(num__exact=request.GET['num'])
                name = f'项目完成情况.xlsx'
            else:
                all_data = Item.objects.filter(num__exact=request.GET['num'], group__exact=request.GET['grp'])
                name = f'%s项目完成情况.xlsx' % request.POST['grp']
            #all_data = all_data[::-1]
            data_list = all_data.values_list()
            response = create_excel(data_list, name)
            return response
        if 'unfit' in request.POST:
            return HttpResponseRedirect('/buyitem/manage?page=1')
        if 'fit' in request.POST:
            num = request.POST['num']
            grp = request.POST['grp']
            return HttpResponseRedirect('/buyitem/manage?page=1&num=%s&grp=%s' % (num, grp))


# -------------------------------------------------------------
# 函数名： update_project
# 功能： 数据行更新
# -------------------------------------------------------------
def update_buy(request, item_id):
    try:
        project = Item.objects.get(id=item_id)

    except Exception as e:
        print('--update error is %s' % e)
        return HttpResponse('--The project is not existed!!--')
    if request.method == 'GET':
        ver = VERSION
        return render(request, 'buyitem/buyupdate.html', locals())
    elif request.method == 'POST':
        if "upd" in request.POST:
            name = request.POST['name']
            group = request.POST['group']
            tel = request.POST['tel']
            num = request.POST['num']
            good = request.POST['good']
            brand = request.POST['brand']
            quantity = request.POST['quantity']
            unit = request.POST['unit']
            info = request.POST['info']
            detail = request.POST['detail']
            finish = request.POST['finish']
            project.name = name
            project.tel = tel
            project.group = group
            project.num = num
            project.good = good
            project.detail = detail
            project.brand = brand
            project.quantity = quantity
            project.unit = unit
            project.info = info
            project.finish = finish
            project.save()
            if ItemLog.objects.exists():
                idx = ItemLog.objects.latest('id').id
            else:
                idx = 0
            ItemLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='update',
                                   other='%s-%s-%s-%s' % (name, good, num, finish))
            return HttpResponseRedirect('/buyitem/manage?page=1')
        elif "back" in request.POST:
            return HttpResponseRedirect('/buyitem/manage?page=1')


# -------------------------------------------------------------
# 函数名： delete_project
# 功能： 数据行删除
# -------------------------------------------------------------
def delete_buy(request, item_id):
    try:
        project = Item.objects.get(id=item_id)
        name = project.name
        good = project.good
        project.delete()
        if ItemLog.objects.exists():
            idx = ItemLog.objects.latest('id').id
        else:
            idx = 0
        ItemLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='delete',
                               other='%s-%s' % (name, good))
        return HttpResponseRedirect('/buyitem/manage?page=1')
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
        return render(request, 'buyitem/buydelete.html', locals())
    elif request.method == 'POST':
        if 'delall' in request.POST:
            all_data = Item.objects.all()
            all_data.delete()
            if ItemLog.objects.exists():
                idx = ItemLog.objects.latest('id').id
            else:
                idx = 0
            ItemLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='delete',
                                   other='all')
            return HttpResponseRedirect('/buyitem/manage?page=1')


# -------------------------------------------------------------
# 函数名： personal_view
# 功能： 个人数据操作
# -------------------------------------------------------------
def personal_view(request):
    if request.method == 'GET':
        ver = VERSION
        if request.COOKIES.get('name', '') != '':
            psn = request.COOKIES.get('name', '')
            psn = json.loads(psn)
            unfinished = Item.objects.filter(name__exact=psn).exclude(finish__exact=True)
            unfinished = unfinished[::-1]
            length = len(unfinished)
            finished = Item.objects.filter(name__exact=psn, finish__exact=True)
            finished = finished[::-1]
            return render(request, 'buyitem/buyself.html', locals())
        else:
            namebox = []
            all_data = Item.objects.all()
            for item in all_data:
                if item.name not in namebox:
                    namebox.append(item.name)
            return render(request, 'buyitem/buyperson.html', locals())
    if request.method == 'POST':
        if 'ret' in request.POST:
            res = HttpResponseRedirect('/buyitem/personal')
            res.delete_cookie('name')
            return res
        if 'nm' in request.POST:
            res = HttpResponseRedirect('/buyitem/personal')
            person = json.dumps(request.POST['nam'])
            res.set_cookie(key='person', value=person, max_age=3600 * 24 * 30)
            return res
        if 'prt' in request.POST:
            psn = request.COOKIES.get('name', '')
            psn = json.loads(psn)
            all_data = Item.objects.filter(name__exact=psn)
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
    data.columns = ['id', '姓名', '单位', '联系电话', '课题编号', '商品名', '商品型号', '数量', '单位', '采购说明', '商品编号']
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
        all_log = ItemLog.objects.all()
        all_log = all_log[::-1]
        dic = {'ver': VERSION, 'data': all_log}
        return render(request, 'buyitem/buylog.html', dic)
