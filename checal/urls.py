from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.checal_view),
    path('steam', views.steam_view),
    path('minical', views.calculator_view),
    path('carbon', views.carbon_view),
    ]