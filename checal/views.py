from django.shortcuts import render

# Create your views here.
VERSION = '燃料电池'


def checal_view(request):
    dic = {'ver': VERSION}
    return render(request, 'checal/checalmain.html', dic)