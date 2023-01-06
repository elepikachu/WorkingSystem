from django.urls import path
from . import views


urlpatterns = [
    path('', views.project_view),
    path('submit', views.submit_view),
    path('manage', views.manage_view),
    path('log', views.log_view),
    path('batch', views.batch_view),
    path('personal', views.personal_view),
    path('update/<int:project_id>', views.update_project),
    path('delete/<int:project_id>', views.delete_project),
    ]