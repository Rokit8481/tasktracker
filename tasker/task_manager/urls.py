from django.urls import path
from .views import *

urlpatterns = [
    # Авторизація
    path("", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),

    # Список
    path('dashboards/', DashboardListView.as_view(), name = 'dashboard_list'),
    path('dashboard/<int:dashboard_pk>/todolists/', TodoListView.as_view(), name='todolist_list'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/tasks/', TaskListView.as_view(), name = 'task_list'),
 
    # Деталі
    path('dashboard/<int:dashboard_pk>/', DashboardDetailView.as_view(), name = 'dashboard_detail'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/', TodoListDetailView.as_view(), name = 'todolist_detail'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/', TaskDetailView.as_view(), name = 'task_detail'),

    # Створення
    path('dashboard/create/', DashboardCreateView.as_view(), name = 'dashboard_create'),
    path('dashboard/<int:dashboard_pk>/todolist/create/', TodoListCreateView.as_view(), name = 'todolist_create'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/create/', TaskCreateView.as_view(), name = 'task_create'),

    # Оновлення
    path('dashboard/<int:dashboard_pk>/edit/', DashboardUpdateView.as_view(), name = 'dashboard_edit'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/edit/', TodoListUpdateView.as_view(), name = 'todolist_edit'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/edit/', TaskUpdateView.as_view(), name = 'task_edit'),

    # Видалення
    path('dashboard/<int:dashboard_pk>/delete/', DashboardDeleteView.as_view(), name = 'dashboard_delete'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/delete/', TodoListDeleteView.as_view(), name = 'todolist_delete'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/delete/', TaskDeleteView.as_view(), name = 'task_delete'),


]
