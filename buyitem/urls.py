from django.urls import path
from . import views


urlpatterns = [
    path('', views.buy_view),
    path('submit', views.submit_view),
    path('submit2', views.submit2_view),
    path('manage', views.manage_view),
    path('log', views.log_view),
    path('batch', views.batch_view),
    path('personal', views.personal_view),
    path('suggestion', views.suggest_view),
    path('spider', views.spider_view),
    path('info', views.info_view),
    path('update/<int:item_id>', views.update_buy),
    path('delete/<int:item_id>', views.delete_buy),
    path('finish/<int:item_id>', views.finish_buy),
    path('unfinish/<int:item_id>', views.unfinish_buy),
    ]