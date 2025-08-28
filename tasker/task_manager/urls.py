from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('', DashboardListView.as_view(), name = 'dashboard_list'),
    path('dashboard/<int:dashboard_pk>/', DashboardDetailView.as_view(), name = 'dashboard_detail'),
    path('dashboard/create/', DashboardCreateView.as_view(), name = 'dashboard_create'),
    path('dashboard/<int:dashboard_pk>/todolists', TodoListListView.as_view(), name = 'todolist_list'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/', TodoListDetailView.as_view(), name = 'todolist_detail'),
    path('dashboard/<int:dashboard_pk>/todolist/create', TodoListCreateView.as_view(), name = 'todolist_create'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/tasks/', TaskListView.as_view(), name = 'task_list'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/', TaskDetailView.as_view(), name = 'task_detail'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/create/', TaskCreateView.as_view(), name = 'task_create'),
]
