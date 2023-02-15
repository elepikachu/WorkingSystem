from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view),
    path('test', views.test_view),
    path('test/<int:item_id>', views.test_view_det),
    path('test/add', views.test_view_add),
    path('test/update/<int:item_id>', views.test_view_upd),
    path('test/delete/<int:item_id>', views.test_view_del),
    ]