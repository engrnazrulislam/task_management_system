from django.urls import path
from tasks.views import manager_dashboard, dashboard, employee_dashboard
from tasks.views import create_task, view_task, update_task, delete_task, task_details
urlpatterns = [
    # path('dashboard/',dashboard),
    path('manager_dashboard/',manager_dashboard, name='manager_dashboard'),
    path('user_dashboard/',employee_dashboard, name='user_dashboard'),
    path('create_task/',create_task, name='create_task'),
    path('view_task/', view_task, name='view_task'),
    path('task_details/<int:task_id>/details/', task_details, name='task_details'),
    path('update_task/<int:id>/', update_task, name='update_task'),
    path('delete_task/<int:id>/', delete_task, name='delete_task'),
    path('dashboard/',dashboard,name='dashboard')    

]
