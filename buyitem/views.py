import requests
from bs4 import BeautifulSoup
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
        if 'good' in request.GET:
            god = request.GET['good']
            no = request.GET['no']
            shp = request.GET['shop']
        else:
            god = ''
            no = ''
            shp = ''
        dic = {'ver': VERSION, 'psn': psn, 'grp': grp, 'tel': tel, 'num': num, 'god': god, 'no': no, 'shp': shp}
        return render(request, 'buyitem/buysubmit.html', dic)
    elif request.method == 'POST':
        if 'sub' in request.POST:
            name = request.POST['name']
            group = request.POST['group']
            tel = request.POST['phone']
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
            Item.objects.create(id=id, name=name, phone=tel, group=group, num=num, unit=unit, date=datetime.datetime.today(),
                                detail=detail, quantity=quantity, brand=brand, info=info, finish=0, good=good)
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
        elif 'spd' in request.POST:
            if request.POST['good'] == '':
                return HttpResponse('商品为空')
            res = parse_page(request.POST['good'], 1)
            dic = {'ver': VERSION, 'res':res, 'good':request.POST['good']}
            return render(request, 'buyitem/buyspider.html', dic)


# -------------------------------------------------------------
# 函数名： manage_view
# 功能： 管理模式
# -------------------------------------------------------------
def manage_view(request):
    if request.method == 'GET':
        if 'grp' in request.GET:
            if request.GET['grp'] is "全部" and request.GET['fin'] is 2 or '2':
                all_data = Item.objects.filter(date__gte=request.GET['st'], date__lte=request.GET['et'])
            elif request.GET['fin'] is 2 or '2':
                all_data = Item.objects.filter(date__gte=request.GET['st'], date__lte=request.GET['et'], group__exact=request.GET['grp'])
            elif request.GET['grp'] is "全部":
                all_data = Item.objects.filter(date__gte=request.GET['st'], date__lte=request.GET['et'], finish__exact=request.GET['fin'])
            else:
                all_data = Item.objects.filter(date__gte=request.GET['st'], date__lte=request.GET['et'], finish__exact=request.GET['fin'], group__exact=request.GET['grp'])
            if request.GET['fin'] == 0:
                slo = "未完成"
            elif request.GET['fin'] == 1:
                slo = "已完成"
            else:
                slo = ""
        else:
            all_data = Item.objects.filter(finish__exact=False)
            all_data = all_data[::-1]
            slo = "未完成"
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
            if request.POST['grp'] == "全部" and request.POST['fin'] == "全部":
                all_data = Item.objects.filter(date__gte=request.POST['date1'], date__lte=request.POST['date2'])
                name = f'物资采购情况.xlsx'
            elif request.POST['fin'] == "全部":
                all_data = Item.objects.filter(date__gte=request.POST['date1'], date__lte=request.POST['date2'],
                                                  group__exact=request.POST['grp'])
                name = f'%s物资采购情况.xlsx' % request.POST['grp']
            elif request.POST['grp'] == "全部":
                if request.POST['fin'] == "未完成":
                    fin = 0
                elif request.POST['fin'] == "已完成":
                    fin = 1
                all_data = Item.objects.filter(date__gte=request.POST['date1'], date__lte=request.POST['date2'],
                                               finish__exact=fin)
                name = f'%s物资采购情况.xlsx' % request.POST['fin']
            else:
                if request.POST['fin'] == "未完成":
                    fin = 0
                elif request.POST['fin'] == "已完成":
                    fin = 1
                all_data = Item.objects.filter(date__gte=request.POST['date1'], date__lte=request.POST['date2'],
                                               finish__exact=fin, group__exact=request.POST['grp'])
                name = f'%s%s物资采购情况.xlsx' % (request.POST['grp'], request.POST['fin'])
            data_list = all_data.values_list()
            response = create_excel(data_list, name)
            return response
        if 'unfit' in request.POST:
            return HttpResponseRedirect('/buyitem/manage?page=1')
        if 'fit' in request.POST:
            st = request.POST['date1']
            et = request.POST['date2']
            grp = request.POST['grp']
            if request.POST['fin'] == "全部":
                fin = 2
            elif request.POST['fin'] == "未完成":
                fin = 0
            elif request.POST['fin'] == "已完成":
                fin = 1
            return HttpResponseRedirect('/buyitem/manage?page=1&st=%s&et=%s&grp=%s&fin=%d' % (st, et, grp, fin))


# -------------------------------------------------------------
# 函数名： update_buy
# 功能： 数据行更新
# -------------------------------------------------------------
def update_buy(request, item_id):
    try:
        item = Item.objects.get(id=item_id)

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
            tel = request.POST['phone']
            num = request.POST['num']
            good = request.POST['good']
            brand = request.POST['brand']
            quantity = request.POST['quantity']
            unit = request.POST['unit']
            info = request.POST['info']
            detail = request.POST['detail']
            #finish = request.POST['finish']
            item.name = name
            item.tel = tel
            item.group = group
            item.num = num
            item.good = good
            item.detail = detail
            item.brand = brand
            item.quantity = quantity
            item.unit = unit
            item.info = info
            #item.finish = finish
            item.save()
            if ItemLog.objects.exists():
                idx = ItemLog.objects.latest('id').id
            else:
                idx = 0
            ItemLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='update',
                                   other='%s-%s-%s-%s' % (name, good, num, item.finish))
            return HttpResponseRedirect('/buyitem/manage?page=1')
        elif "back" in request.POST:
            return HttpResponseRedirect('/buyitem/manage?page=1')


# -------------------------------------------------------------
# 函数名： finish_buy
# 功能： 数据行完成
# -------------------------------------------------------------
def finish_buy(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        if item.finish == True:
            return HttpResponse('--操作失败，该条购买已经完成啦!!--')
        item.finish = True
        item.save()
        name = item.name
        good = item.good
        if ItemLog.objects.exists():
            idx = ItemLog.objects.latest('id').id
        else:
            idx = 0
        ItemLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='finish',
                               other='%s-%s' % (name, good))
        return HttpResponseRedirect('/buyitem/manage?page=1')
    except Exception as e:
        print('--delete error is %s' % e)
        return HttpResponse('--更新失败，请稍后再试!!--')


# -------------------------------------------------------------
# 函数名： delete_buy
# 功能： 数据行删除
# -------------------------------------------------------------
def delete_buy(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        name = item.name
        good = item.good
        item.delete()
        if ItemLog.objects.exists():
            idx = ItemLog.objects.latest('id').id
        else:
            idx = 0
        ItemLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='delete',
                               other='%s-%s' % (name, good))
        return HttpResponseRedirect('/buyitem/manage?page=1')
    except Exception as e:
        print('--delete error is %s' % e)
        return HttpResponse('--删除失败，请稍后再试!!--')


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
        groupbox = []
        all_data = Item.objects.all()
        for item in all_data:
            if item.group not in groupbox:
                groupbox.append(item.group)
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
        elif 'deldate' in request.POST:
            date1 = request.POST['date1']
            date2 = request.POST['date2']
            all_data = Item.objects.filter(date__gte=date1, date__lte=date2)
            all_data.delete()
            if ItemLog.objects.exists():
                idx = ItemLog.objects.latest('id').id
            else:
                idx = 0
            ItemLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='delete',
                                      other='all in %s-%s' % (date1, date2))
            return HttpResponseRedirect('/buyitem/manage?page=1')
        elif 'delgrp' in request.POST:
            grp = request.POST['grp']
            all_data = Item.objects.filter(group__exact=grp)
            all_data.delete()
            if ItemLog.objects.exists():
                idx = ItemLog.objects.latest('id').id
            else:
                idx = 0
            ItemLog.objects.create(id=idx + 1, ip=get_ip(request), date=datetime.datetime.today(), cmd='delete',
                                other='all for %s' % grp)
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
            res.set_cookie(key='name', value=person, max_age=3600 * 24 * 30)
            return res
        if 'prt' in request.POST:
            psn = request.COOKIES.get('name', '')
            psn = json.loads(psn)
            all_data = Item.objects.filter(name__exact=psn)
            data_list = all_data.values_list()
            name = f'物资采购情况-%s.xlsx' % psn
            response = create_excel(data_list, name)
            return response


# -------------------------------------------------------------
# 函数名： create_excel
# 功能： 打印excel
# -------------------------------------------------------------
def create_excel(data_list, name):
    data = pd.DataFrame(data_list)
    data.columns = ['id', '商品名', '品牌型号', '单位', '数量', '姓名', '电话', '课题编号', '采购说明', '商品编号', '单位全称', '提交日期', '完成情况']
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


# -------------------------------------------------------------
# 函数名： get_page
# 功能： 爬取页面
# -------------------------------------------------------------
def get_page(url, page):
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    try:
        html = requests.request("GET", url, headers=headers, timeout=10)
        html.encoding = "utf-8"
        #print(html.text[:1000])
        return html.text
    except:
        print('爬取失败')
        return "爬取失败"


# -------------------------------------------------------------
# 函数名： parse_page
# 功能： 解析爬取页面
# -------------------------------------------------------------
def parse_page(item, page):
    url = "https://search.jd.com/Search?keyword=%s" % item
    html = get_page(url, page)
    html = str(html)
    if html is not None:
        soup = BeautifulSoup(html, 'html.parser')
        li_all = soup.select('#J_goodsList ul li')
        res_list = []
        for li in li_all:
            name = [i.get_text() for i in li.select('.p-name em')][0]
            price = [i.get_text() for i in li.select('.p-price i')][0]
            if li.select('.p-shop a'):
                shop = [i.get_text() for i in li.select('.p-shop a')][0]
            elif li.select('.p-shopnum a'):
                shop = [i.get_text() for i in li.select('.p-shopnum a')][0]
            else:
                print(li)
                shop = "自营"
            number = li['data-sku']
            href = "item.jd.com/%s.html" % number
            if(len(name) !=0 and len(price) !=0 and len(shop) !=0 and len(number) !=0):
                info = {'name': name, 'price': price, 'shop': shop, 'number': number, 'href': href}
                res_list.append(info)
        return res_list
    else:
        print('error')
        return None


