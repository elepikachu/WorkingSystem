from django.urls import path, include
from project import views

from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.fuelcell_view),
    ]