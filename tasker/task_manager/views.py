from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Dashboard, TodoList, Task, Comment
from .forms import DashboardCreateForm, TodoListCreateForm, TaskCreateForm, CommentCreateForm, AddMemberForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User



# Міксина до дошки
class DashboardAccessMixin:
    def get_queryset(self):
        return Dashboard.objects.filter(
            Q(created_by=self.request.user) | Q(members=self.request.user)
        ).distinct()


# Міксина до списків завдань
class TodoListAccessMixin(DashboardAccessMixin):
    def get_queryset(self):
        return TodoList.objects.filter(
            dashboard__in=DashboardAccessMixin.get_queryset(self)
        ).distinct()


# Міксина до завдань
class TaskAccessMixin(TodoListAccessMixin):
    def get_queryset(self):
        return Task.objects.filter(
            todolist__in=TodoListAccessMixin.get_queryset(self)
        ).distinct()


# Міксина до коментарів
class CommentAccessMixin(TaskAccessMixin):
    def get_queryset(self):
        return Comment.objects.filter(
            task__in=TaskAccessMixin.get_queryset(self)
        ).distinct()
    
"""Логін, регестрація та вихід"""


# Логін
class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True  
    next_page = reverse_lazy("main") 


# Вихід
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("main") 


# Реєстрація
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)  
        return response

"""СПИСКИ"""


#Список Дошок
class DashboardListView(LoginRequiredMixin, DashboardAccessMixin, ListView):
    model = Dashboard
    template_name = 'dashboard/dashboard_list.html'
    context_object_name = 'dashboards'

# Список коментарів конкретного завдання
class CommentListView(LoginRequiredMixin, CommentAccessMixin, ListView):
    model = Comment
    template_name = 'comment/comment_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        qs = super().get_queryset() 
        dashboard_pk = self.kwargs.get("dashboard_pk")
        todolist_pk = self.kwargs.get("todolist_pk")
        task_pk = self.kwargs.get("task_pk")

        if dashboard_pk:
            qs = qs.filter(task__todolist__dashboard_id=dashboard_pk)
        if todolist_pk:
            qs = qs.filter(task__todolist_id=todolist_pk)
        if task_pk:
            qs = qs.filter(task_id=task_pk)

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboards_qs = DashboardAccessMixin.get_queryset(self)
        context["dashboard"] = get_object_or_404(dashboards_qs, pk=self.kwargs["dashboard_pk"])
        context["todolist"] = get_object_or_404(TodoListAccessMixin.get_queryset(self), pk=self.kwargs["todolist_pk"])
        context["task"] = get_object_or_404(TaskAccessMixin.get_queryset(self), pk=self.kwargs["task_pk"])
        return context


"""ДЕТАЛЬНА СТОРІНКА"""



# Детальна сторінка дошки
class DashboardDetailView(LoginRequiredMixin, DashboardAccessMixin, DetailView):
    model = Dashboard
    template_name = 'dashboard/dashboard_detail.html'
    context_object_name = 'dashboard'
    pk_url_kwarg = "dashboard_pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard = self.get_object()
        context["todolists"] = dashboard.todolists.all()
        return context


# Детальна сторінка списку завдань
class TodoListDetailView(LoginRequiredMixin, TodoListAccessMixin, DetailView):
    model = TodoList
    template_name = 'todolist/todolist_detail.html'
    context_object_name = 'todolist'
    pk_url_kwarg = "todolist_pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todolist = self.get_object()
        context['dashboard'] = todolist.dashboard
        context["tasks"] = todolist.tasks.all()
        return context


# Детальна сторінка завдання
class TaskDetailView(LoginRequiredMixin, TaskAccessMixin, DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'
    pk_url_kwarg = "task_pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['todolist'] = task.todolist
        context['dashboard'] = task.todolist.dashboard
        return context
    
#Детальна сторінка коментаря
class CommentDetailView(LoginRequiredMixin, CommentAccessMixin, DetailView):
    model = Comment
    template_name = 'comment/comment_detail.html'
    context_object_name = 'comment'
    pk_url_kwarg = "comment_pk"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = self.get_object()
        context['task'] = comment.task
        context['todolist'] = comment.task.todolist
        context['dashboard'] = comment.task.todolist.dashboard
        return context


"""CТОРІНКА СТВОРЕННЯ"""


#Сторінка створення дошки
class DashboardCreateView(LoginRequiredMixin, CreateView):
    model = Dashboard
    form_class = DashboardCreateForm
    template_name = "dashboard/dashboard_create.html"
    success_url = reverse_lazy("dashboard_list")

    def form_valid(self, form):
        dashboard = form.save(commit = False)
        dashboard.created_by = self.request.user
        dashboard.save()
        return super().form_valid(form)

#Сторінка створення списку завдань
class TodoListCreateView(LoginRequiredMixin, CreateView):
    model = TodoList
    form_class = TodoListCreateForm
    template_name = "todolist/todolist_create.html"
    
    def get_success_url(self):
        return reverse_lazy("dashboard_detail", kwargs = {"dashboard_pk": self.kwargs["dashboard_pk"]})

    def form_valid(self, form):
        todolist = form.save(commit = False)
        todolist.created_by = self.request.user
        todolist.dashboard = get_object_or_404(Dashboard, pk = self.kwargs["dashboard_pk"] )
        todolist.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        return context

#Сторінка створення завдання
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task/task_create.html"

    def get_success_url(self):
        return reverse_lazy("todolist_detail", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"]
            })

    def form_valid(self, form):
        task = form.save(commit = False)
        task.created_by = self.request.user
        task.todolist = TodoList.objects.get(pk = self.kwargs["todolist_pk"] )
        task.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        context["todolist"] = get_object_or_404(TodoList, pk=self.kwargs["todolist_pk"])
        return context
    
#Сторінка створення коментаря
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment 
    form_class = CommentCreateForm
    template_name = "comment/comment_create.html"

    def get_success_url(self):
        return reverse_lazy("comment_list", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"],
            "task_pk": self.kwargs["task_pk"]
            })

    def form_valid(self, form):
        comment = form.save(commit = False)
        comment.created_by = self.request.user
        comment.task = Task.objects.get(pk = self.kwargs["task_pk"])
        comment.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        context["todolist"] = get_object_or_404(TodoList, pk=self.kwargs["todolist_pk"])
        context["task"] = get_object_or_404(Task, pk=self.kwargs["task_pk"])
        return context


"""СТОРІНКА РЕДАГУВАННЯ"""



# Редагування дошки
class DashboardUpdateView(LoginRequiredMixin, DashboardAccessMixin, UpdateView):
    model = Dashboard
    form_class = DashboardCreateForm
    template_name = 'dashboard/dashboard_edit.html'
    pk_url_kwarg = "dashboard_pk"

    def get_success_url(self):
        return reverse_lazy("dashboard_detail", kwargs={"dashboard_pk": self.kwargs["dashboard_pk"]})


# Редагування списку завдань
class TodoListUpdateView(LoginRequiredMixin, TodoListAccessMixin, UpdateView):
    model = TodoList
    form_class = TodoListCreateForm
    template_name = 'todolist/todolist_edit.html'
    pk_url_kwarg = "todolist_pk"

    def get_success_url(self):
        return reverse_lazy("todolist_detail", kwargs={
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"]
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        return context

# Редагування завдання
class TaskUpdateView(LoginRequiredMixin, TaskAccessMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'task/task_edit.html'
    pk_url_kwarg = "task_pk"

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"],
            "task_pk": self.kwargs["task_pk"]
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        context["todolist"] = get_object_or_404(TodoList, pk=self.kwargs["todolist_pk"])
        return context

# Редагування коментаря
class CommentUpdateView(LoginRequiredMixin, CommentAccessMixin, UpdateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = 'comment/comment_edit.html'
    pk_url_kwarg = "comment_pk"

    def get_success_url(self):
        return reverse_lazy("comment_detail", kwargs={
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"],
            "task_pk": self.kwargs["task_pk"],
            "comment_pk": self.kwargs["comment_pk"],
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        context["todolist"] = get_object_or_404(TodoList, pk=self.kwargs["todolist_pk"])
        context["task"] = get_object_or_404(Task, pk=self.kwargs["task_pk"])
        return context
    
    
"""СТОРІНКА ВИДАЛЕННЯ"""


#Видалення дошки
class DashboardDeleteView(LoginRequiredMixin, DashboardAccessMixin, DeleteView):
    model = Dashboard
    success_url = reverse_lazy("dashboard_list")
    pk_url_kwarg = "dashboard_pk"

#Видалення списка завдань
class TodoListDeleteView(LoginRequiredMixin, TodoListAccessMixin, DeleteView):
    model = TodoList
    pk_url_kwarg = "todolist_pk"

    def get_success_url(self):
        return reverse_lazy("dashboard_detail", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            })
    
#Видалення завдання
class TaskDeleteView(LoginRequiredMixin, TaskAccessMixin, DeleteView):
    model = Task
    pk_url_kwarg = "task_pk"

    def get_success_url(self):
        return reverse_lazy("todolist_detail", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"]
            })

#Видалення завдання
class CommentDeleteView(LoginRequiredMixin, CommentAccessMixin, DeleteView):
    model = Comment
    pk_url_kwarg = "comment_pk"

    def get_success_url(self):
        return reverse_lazy("comment_list", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"],
            "task_pk": self.kwargs["task_pk"]
            })
    

"""ОСНОВНІ СТОРІНКИ САЙТУ"""

#Основна сторінка
class MainPageView(TaskAccessMixin ,LoginRequiredMixin, ListView):
    model = Task
    template_name = "main/main.html"
    context_object_name = "tasks"

    def get_queryset(self):
        qs = super().get_queryset()

        dashboard_pk = self.request.GET.get("dashboard")
        todolist_pk = self.request.GET.get("todolist")

        if dashboard_pk:
            qs = qs.filter(todolist__dashboard_id=dashboard_pk)
        if todolist_pk:
            qs = qs.filter(todolist_id=todolist_pk)

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dashboards_qs = Dashboard.objects.filter(
            Q(created_by=self.request.user) | Q(members=self.request.user)
        ).distinct()
        context["dashboards"] = dashboards_qs

        dashboard_pk = self.request.GET.get("dashboard")
        todolist_pk = self.request.GET.get("todolist")

        if dashboard_pk:
            dashboard = get_object_or_404(dashboards_qs, pk=dashboard_pk)
            context["selected_dashboard"] = dashboard
            context["todolists"] = dashboard.todolists.all()
        else:
            context["selected_dashboard"] = None
            context["todolists"] = []

        if todolist_pk:
            todolist = get_object_or_404(
                TodoList.objects.filter(dashboard__in=dashboards_qs),
                pk=todolist_pk
            )
            context["selected_todolist"] = todolist
        else:
            context["selected_todolist"] = None

        context["columns"] = {
            "draft": "Чернетка",
            "in_progress": "В процесі",
            "completed": "Завершено",
            "archived": "Архів"
        }

        return context

#Учасники дошки
class DashboardMembersView(LoginRequiredMixin, DashboardAccessMixin, SingleObjectMixin, FormView):
    model = Dashboard
    template_name = "dashboard/dashboard_members.html"
    context_object_name = "dashboard"
    pk_url_kwarg = "dashboard_pk"
    form_class = AddMemberForm

    def get_object(self, queryset=None):
        return super().get_object(queryset)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.cleaned_data["username"]
        if user != self.object.created_by:
            self.object.members.add(user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("dashboard_members", kwargs={"dashboard_pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = self.object
        context["members"] = self.object.members.all()
        return context

#Видалення учасника дошки
class DashboardMemberDeleteView(LoginRequiredMixin, DashboardAccessMixin, View):
    def post(self, request, *args, **kwargs):
        dashboard = get_object_or_404(Dashboard, pk=kwargs["dashboard_pk"])
        user = get_object_or_404(User, pk=kwargs["user_pk"])

        if user != dashboard.created_by:
            dashboard.members.remove(user)

        return redirect("dashboard_members", dashboard_pk=dashboard.pk)