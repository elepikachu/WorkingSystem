from django.urls import path
from . import views


urlpatterns = [
    path('', views.buy_view),
    path('submit', views.submit_view),
    path('manage', views.manage_view),
    path('log', views.log_view),
    path('batch', views.batch_view),
    path('personal', views.personal_view),
    path('update/<int:item_id>', views.update_buy),
    path('delete/<int:item_id>', views.delete_buy),
    path('finish/<int:item_id>', views.finish_buy),
    ]