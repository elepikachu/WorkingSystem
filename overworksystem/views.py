from django.shortcuts import render


VERSION = '小皮的工具库 1.0.0'


def main_view(request):
    dic = {'ver': VERSION}
    return render(request, 'main.html', dic)


def update_view(request):
    dic = {'ver': VERSION}
    return render(request, 'update.html', dic)


def info_view(request):
    dic = {'ver': VERSION}
    return render(request, 'info.html', dic)


def food_view(request):
    dic = {'ver': VERSION}
    return render(request, 'food.html', dic)
