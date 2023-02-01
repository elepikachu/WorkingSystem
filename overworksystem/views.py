from django.shortcuts import render
from django.views.decorators.http import require_GET


VERSION = '小皮的工具库 1.0.0'


# -------------------------------------------------------------
# 函数名： main_view
# 功能： 网站首页
# -------------------------------------------------------------
def main_view(request):
    dic = {'ver': VERSION}
    return render(request, 'main.html', dic)


# -------------------------------------------------------------
# 函数名： update_view
# 功能： 更新日志
# -------------------------------------------------------------
def update_view(request):
    dic = {'ver': VERSION}
    return render(request, 'update.html', dic)


# -------------------------------------------------------------
# 函数名： info_view
# 功能： 网站说明
# -------------------------------------------------------------
def info_view(request):
    dic = {'ver': VERSION}
    return render(request, 'info.html', dic)


# -------------------------------------------------------------
# 函数名： food_view
# 功能： 随机选择器
# -------------------------------------------------------------
def food_view(request):
    dic = {'ver': VERSION}
    return render(request, 'food.html', dic)


# -------------------------------------------------------------
# 函数名： robots_txt
# 功能： robots.txt
# -------------------------------------------------------------
@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: *",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")