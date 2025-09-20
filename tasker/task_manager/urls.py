from django.urls import path
from .views import *

urlpatterns = [
    #Основні
    path("main/", MainPageView.as_view(), name="main"),
    path("dashboard/<int:dashboard_pk>/members/", DashboardMembersView.as_view(), name="dashboard_members"),
    path("dashboard/<int:dashboard_pk>/members/<int:user_pk>/delete/", DashboardMemberDeleteView.as_view(), name="dashboard_member_delete" ),
    path("task/update-status/", TaskStatusUpdateView.as_view(), name="task_update_status"),

    # Авторизація
    path("", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),

    # Спиcок
    path('dashboards/', DashboardListView.as_view(), name = 'dashboard_list'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/comments/', CommentListView.as_view(), name = 'comment_list'),
 
    # Деталі
    path('dashboard/<int:dashboard_pk>/', DashboardDetailView.as_view(), name = 'dashboard_detail'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/', TodoListDetailView.as_view(), name = 'todolist_detail'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/', TaskDetailView.as_view(), name = 'task_detail'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/comment/<int:comment_pk>/', CommentDetailView.as_view(), name = 'comment_detail'),

    # Створення
    path('dashboard/create/', DashboardCreateView.as_view(), name = 'dashboard_create'),
    path('dashboard/<int:dashboard_pk>/todolist/create/', TodoListCreateView.as_view(), name = 'todolist_create'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/create/', TaskCreateView.as_view(), name = 'task_create'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/comment/create/', CommentCreateView.as_view(), name = 'comment_create'),

    # Оновлення
    path('dashboard/<int:dashboard_pk>/edit/', DashboardUpdateView.as_view(), name = 'dashboard_edit'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/edit/', TodoListUpdateView.as_view(), name = 'todolist_edit'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/edit/', TaskUpdateView.as_view(), name = 'task_edit'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/comment/<int:comment_pk>/edit/', CommentUpdateView.as_view(), name = 'comment_edit'),

    # Видалення
    path('dashboard/<int:dashboard_pk>/delete/', DashboardDeleteView.as_view(), name = 'dashboard_delete'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/delete/', TodoListDeleteView.as_view(), name = 'todolist_delete'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/delete/', TaskDeleteView.as_view(), name = 'task_delete'),
    path('dashboard/<int:dashboard_pk>/todolist/<int:todolist_pk>/task/<int:task_pk>/comment/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name = 'comment_delete'),
]
