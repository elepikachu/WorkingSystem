from django.urls import path, include
from project import views

from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.project_view),
    path('submit', views.submit_view),
    path('manage', views.manage_view),
    path('log', views.log_view),
    ]