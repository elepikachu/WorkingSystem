from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.checal_view),
    path('steam', views.steam_view),
    path('minical', views.calculator_view),
    path('carbon', views.carbon_view),
    path('mass', views.mass_view),
    path('volume', views.volume_view),
    path('massup', views.mass_upload_view),
    path('volumeup', views.volume_upload_view)
    ]