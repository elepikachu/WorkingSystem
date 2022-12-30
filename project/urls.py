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
    path('update_project/<int:project_id>', views.update_project),
path('delete_project/<int:project_id>', views.delete_project),
    ]