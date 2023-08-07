from django.shortcuts import render
from .calculation import CalculationFunc, calculate_mass, calculate_volume
from .upload import excel_generate

# Create your views here.
VERSION = '化工计算器'
DIC_PRS = {'Pa': 1, 'kPa': 1000, 'MPa': 1000000, 'atm': 101325}
DIC_TMP = {'K': 0, 'C': 273.15}


# -------------------------------------------------------------
# 函数名： steam_view
# 功能： 蒸汽计算器
# -------------------------------------------------------------
def steam_view(request):
    if request.method == 'GET':
        dic = {'ver': VERSION, 'res': False}
        return render(request, 'checal/steam.html', dic)
    elif request.method == 'POST':
        if 'cal' in request.POST:
            prs = request.POST['prs']
            prs2 = float(prs) * float(DIC_PRS[request.POST['uprs']])
            tmp = request.POST['tmp']
            tmp2 = float(tmp) + float(DIC_TMP[request.POST['utmp']])
            stm = request.POST['stm']
            res = CalculationFunc().water_steam_cal(prs2, tmp2, stm)
            dic = {'ver': VERSION, 'res': True}
            dic.update(res)
            print(dic)
            return render(request, 'checal/steam.html', dic)


# -------------------------------------------------------------
# 函数名： carbon_view
# 功能： 碳缺省值计算器
# -------------------------------------------------------------
def carbon_view(request):
    if request.method == 'GET':
        dic = {'ver': VERSION, 'res': False}
        return render(request, 'checal/carb.html', dic)
    elif request.method == 'POST':
        if 'cal' in request.POST:
            NCVi_q = request.POST['prs']
            EFi_q = request.POST['tmp']
            res = CalculationFunc().carbon_content_cal(NCVi_q, EFi_q)
            dic = {'ver': VERSION, 'res': True, 'z': res}
            return render(request, 'checal/carb.html', dic)


# -------------------------------------------------------------
# 函数名： calculator_view
# 功能： 迷你计算器
# -------------------------------------------------------------
def calculator_view(request):
    dic = {'ver': VERSION}
    return render(request, 'checal/cal.html', dic)


# -------------------------------------------------------------
# 函数名： steam_view
# 功能： 首页
# -------------------------------------------------------------
def checal_view(request):
    dic = {'ver': VERSION}
    return render(request, 'checal/checalmain.html', dic)


# -------------------------------------------------------------
# 函数名： mass_view
# 功能： 质量分数计算
# -------------------------------------------------------------
def mass_view(request):
    if request.method == 'GET':
        dic = {'ver': VERSION}
        return render(request, 'checal/mass.html', dic)
    if request.method == 'POST':
        if 'btn' in request.POST:
            entries1 = []
            entries2 = []
            entries3 = []
            entries4 = []
            entries5 = []
            entries6 = []
            entries7 = []
            entries8 = []
            entries9 = []
            entries10 = []
            entries11 = []
            entries12 = []
            entries13 = []
            entries14 = []
            entries15 = []
            entries16 = []
            entries17 = []
            entries18 = []

            num = request.POST['num']
            for i in range(int(num)):
                entries2.append(float(request.POST['c11' + str(i)]))
                entries3.append(float(request.POST['c21' + str(i)]))
                entries4.append(float(request.POST['c22' + str(i)]))
                entries5.append(float(request.POST['c23' + str(i)]))
                entries6.append(float(request.POST['c31' + str(i)]))
                entries7.append(float(request.POST['c32' + str(i)]))
                entries8.append(float(request.POST['ic4' + str(i)]))
                entries9.append(float(request.POST['nc4' + str(i)]))
                entries10.append(float(request.POST['c42' + str(i)]))
                entries11.append(float(request.POST['c51' + str(i)]))
                entries12.append(float(request.POST['c52' + str(i)]))
                entries13.append(float(request.POST['h2' + str(i)]))
                entries14.append(float(request.POST['h2o' + str(i)]))
                entries15.append(float(request.POST['h2s' + str(i)]))
                entries16.append(float(request.POST['n2' + str(i)]))
                entries17.append(float(request.POST['co1' + str(i)]))
                entries18.append(float(request.POST['co2' + str(i)]))
                sum_all = float(request.POST['c11' + str(i)]) + float(request.POST['c21' + str(i)]) + float(request.POST['c22' + str(i)]) + float(request.POST['c23' + str(i)]) + float(request.POST['c31' + str(i)]) + float(request.POST['c32' + str(i)]) + float(request.POST['ic4' + str(i)]) + float(request.POST['nc4' + str(i)]) + float(request.POST['c42' + str(i)]) + float(request.POST['c51' + str(i)]) + float(request.POST['c52' + str(i)]) + float(request.POST['h2' + str(i)]) + float(request.POST['h2o' + str(i)]) + float(request.POST['h2s' + str(i)]) + float(request.POST['n2' + str(i)]) + float(request.POST['co1' + str(i)]) + float(request.POST['co2' + str(i)])
                entries1.append(sum_all)

            response = calculate_mass(entries1, entries2, entries3, entries4, entries5, entries6, entries7, entries8, entries9, entries10,
                    entries11, entries12, entries13, entries14, entries15, entries16, entries17, entries18)
            return response


# -------------------------------------------------------------
# 函数名： mass_upload_view
# 功能： 质量分数表格上传
# -------------------------------------------------------------
def mass_upload_view(request):
    if request.method == 'GET':
        dic = {'ver': VERSION}
        return render(request, 'checal/mass up.html', dic)
    if request.method == 'POST':
        if 'cal' in request.POST and request.FILES['upl']:
            f = request.FILES['upl']
            response = excel_generate(f, 'M')
            return response


# -------------------------------------------------------------
# 函数名： volume_upload_view
# 功能： 体积分数表格上传
# -------------------------------------------------------------
def volume_upload_view(request):
    if request.method == 'GET':
        dic = {'ver': VERSION}
        return render(request, 'checal/volume up.html', dic)
    if request.method == 'POST':
        if 'cal' in request.POST and request.FILES['upl']:
            f = request.FILES['upl']
            rep = excel_generate(f, 'V')
            return rep


# -------------------------------------------------------------
# 函数名： volume_view
# 功能： 体积分数计算
# -------------------------------------------------------------
def volume_view(request):
    if request.method == 'GET':
        dic = {'ver': VERSION}
        return render(request, 'checal/volume.html', dic)
    if request.method == 'POST':
        if 'btn' in request.POST:
            entries1 = []
            entries2 = []
            entries3 = []
            entries4 = []
            entries5 = []
            entries6 = []
            entries7 = []
            entries8 = []
            entries9 = []
            entries10 = []
            entries11 = []
            entries12 = []
            entries13 = []
            entries14 = []
            entries15 = []
            entries16 = []
            entries17 = []
            entries18 = []

            num = request.POST['num']
            for i in range(int(num)):
                entries2.append(int(request.POST['c11' + str(i)]))
                entries3.append(int(request.POST['c21' + str(i)]))
                entries4.append(int(request.POST['c22' + str(i)]))
                entries5.append(int(request.POST['c23' + str(i)]))
                entries6.append(int(request.POST['c31' + str(i)]))
                entries7.append(int(request.POST['c32' + str(i)]))
                entries8.append(int(request.POST['ic4' + str(i)]))
                entries9.append(int(request.POST['nc4' + str(i)]))
                entries10.append(int(request.POST['c42' + str(i)]))
                entries11.append(int(request.POST['c51' + str(i)]))
                entries12.append(int(request.POST['c52' + str(i)]))
                entries13.append(int(request.POST['h2' + str(i)]))
                entries14.append(int(request.POST['h2o' + str(i)]))
                entries15.append(int(request.POST['h2s' + str(i)]))
                entries16.append(int(request.POST['n2' + str(i)]))
                entries17.append(int(request.POST['co1' + str(i)]))
                entries18.append(int(request.POST['co2' + str(i)]))
                sum_all = int(request.POST['c11' + str(i)]) + int(request.POST['c21' + str(i)]) + int(request.POST['c22' + str(i)]) + int(request.POST['c23' + str(i)]) + int(request.POST['c31' + str(i)]) + int(request.POST['c32' + str(i)]) + int(request.POST['ic4' + str(i)]) + int(request.POST['nc4' + str(i)]) + int(request.POST['c42' + str(i)]) + int(request.POST['c51' + str(i)]) + int(request.POST['c52' + str(i)]) + int(request.POST['h2' + str(i)]) + int(request.POST['h2o' + str(i)]) + int(request.POST['h2s' + str(i)]) + int(request.POST['n2' + str(i)]) + int(request.POST['co1' + str(i)]) + int(request.POST['co2' + str(i)])
                entries1.append(sum_all)

            response = calculate_volume(entries1, entries2, entries3, entries4, entries5, entries6, entries7, entries8, entries9, entries10,
                    entries11, entries12, entries13, entries14, entries15, entries16, entries17, entries18)
            return response