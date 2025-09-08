from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Dashboard, TodoList, Task, Comment
from .forms import DashboardCreateForm, TodoListCreateForm, TaskCreateForm, CommentCreateForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# Мінікс для доступу до дошки
class DashboardAccessMixin:
    def get_dashboard(self):
        queryset = Dashboard.objects.filter(
            Q(created_by=self.request.user) | Q(members=self.request.user)
        ).distinct()
        return get_object_or_404(queryset, pk=self.kwargs["dashboard_pk"])

    def dispatch(self, request, *args, **kwargs):
        self.dashboard = self.get_dashboard()
        return super().dispatch(request, *args, **kwargs)

# Мінікс для доступу до списку завдань
class TodoListAccessMixin(DashboardAccessMixin):
    def get_todolist(self):
        dashboard = self.get_dashboard()
        queryset = TodoList.objects.filter(dashboard=dashboard)
        return get_object_or_404(queryset, pk=self.kwargs["todolist_pk"])

    def dispatch(self, request, *args, **kwargs):
        self.todolist = self.get_todolist()
        return super().dispatch(request, *args, **kwargs)

# Мінікс для доступу до завдання
class TaskAccessMixin(TodoListAccessMixin):
    def get_task(self):
        todolist = self.get_todolist()
        queryset = Task.objects.filter(todolist=todolist)
        return get_object_or_404(queryset, pk=self.kwargs["task_pk"])

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_task()
        return super().dispatch(request, *args, **kwargs)

# Мінікс для доступу до коментаря
class CommentAccessMixin(TaskAccessMixin):
    def get_comment(self):
        task = self.get_task()
        queryset = Comment.objects.filter(task=task)
        return get_object_or_404(queryset, pk=self.kwargs["comment_pk"])

    def dispatch(self, request, *args, **kwargs):
        self.comment = self.get_comment()
        return super().dispatch(request, *args, **kwargs)

"""Логін, регестрація та вихід"""


# Логін
class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True  
    next_page = reverse_lazy("dashboard_list") 


# Вихід
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login") 


# Реєстрація
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("dashboard_list")

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

# Список списків завдань
class TodoListView(LoginRequiredMixin, TodoListAccessMixin, ListView):
    model = TodoList
    template_name = 'todolist/todolist_list.html'
    context_object_name = 'todolists'

    def get_queryset(self):
        return TodoList.objects.filter(dashboard_id=self.kwargs["dashboard_pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        context["dashboards"] = Dashboard.objects.filter(created_by=self.request.user)
        return context

#Список Завдань
class TaskListView(LoginRequiredMixin, TaskAccessMixin, ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        todolist_pk = self.kwargs["todolist_pk"]
        return Task.objects.filter(todolist_id=todolist_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        context["todolist"] = get_object_or_404(TodoList, pk=self.kwargs["todolist_pk"])
        context["dashboards"] = Dashboard.objects.filter(created_by=self.request.user)
        context["todolists"] = TodoList.objects.filter(created_by=self.request.user)  
        context["columns"] = {
        "draft": "Чернетка",
        "in_progress": "В роботі",
        "completed": "Завершено",
        "archived": "Архів",
        }
        return context

#Список Коментарів
class CommentListView(LoginRequiredMixin, CommentAccessMixin, ListView):
    model = Comment
    template_name = 'comment/comment_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        task_pk = self.kwargs["task_pk"]
        return Comment.objects.filter(task_id=task_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        context["todolist"] = get_object_or_404(TodoList, pk=self.kwargs["todolist_pk"])
        context["task"] = get_object_or_404(Task, pk=self.kwargs["task_pk"])
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
        context["todolists"] = TodoList.objects.filter(
            Q(dashboard=self.dashboard) & 
            (Q(created_by=self.request.user) | Q(dashboard__members=self.request.user))
        ).distinct()
        return context


# Детальна сторінка списку завдань
class TodoListDetailView(LoginRequiredMixin, TodoListAccessMixin, DetailView):
    model = TodoList
    template_name = 'todolist/todolist_detail.html'
    context_object_name = 'todolist'

    def get_object(self, queryset=None):
        return self.todolist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todolist = self.get_object()
        context['dashboard'] = todolist.dashboard
        context['tasks'] = Task.objects.filter(
            Q(todolist=todolist) &
            (Q(created_by=self.request.user) | Q(todolist__dashboard__members=self.request.user))
        ).distinct()
        return context


# Детальна сторінка завдання
class TaskDetailView(LoginRequiredMixin, TaskAccessMixin, DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        return self.task

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

    def get_object(self, queryset=None):
        return self.comment
    
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
        return reverse_lazy("todolist_list", kwargs = {"dashboard_pk": self.kwargs["dashboard_pk"]})

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
        return reverse_lazy("task_list", kwargs = {
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
    success_url = reverse_lazy("dashboard_list")
    pk_url_kwarg = "dashboard_pk"

    def get_queryset(self):
        return Dashboard.objects.filter(
            Q(created_by=self.request.user) | Q(members=self.request.user)
        ).distinct()

# Редагування списку завдань
class TodoListUpdateView(LoginRequiredMixin, TodoListAccessMixin, UpdateView):
    model = TodoList
    form_class = TodoListCreateForm
    template_name = 'todolist/todolist_edit.html'
    pk_url_kwarg = "todolist_pk"

    def get_success_url(self):
        return reverse_lazy("todolist_list", kwargs={"dashboard_pk": self.kwargs["dashboard_pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        return context

    def get_queryset(self):
        return TodoList.objects.filter(
            Q(dashboard__created_by=self.request.user) | Q(dashboard__members=self.request.user)
        ).distinct()

# Редагування завдання
class TaskUpdateView(LoginRequiredMixin, TaskAccessMixin, UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'task/task_edit.html'
    pk_url_kwarg = "task_pk"

    def get_success_url(self):
        return reverse_lazy("task_list", kwargs={
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"]
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        context["todolist"] = get_object_or_404(TodoList, pk=self.kwargs["todolist_pk"])
        return context

    def get_queryset(self):
        return Task.objects.filter(
            Q(todolist__dashboard__created_by=self.request.user) |
            Q(todolist__dashboard__members=self.request.user)
        ).distinct()

# Редагування коментаря
class CommentUpdateView(LoginRequiredMixin, CommentAccessMixin, UpdateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = 'comment/comment_edit.html'
    pk_url_kwarg = "comment_pk"

    def get_success_url(self):
        return reverse_lazy("comment_list", kwargs={
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"],
            "task_pk": self.kwargs["task_pk"]
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        context["todolist"] = get_object_or_404(TodoList, pk=self.kwargs["todolist_pk"])
        context["task"] = get_object_or_404(Task, pk=self.kwargs["task_pk"])
        return context

    def get_queryset(self):
        return Comment.objects.filter(
            Q(task__todolist__dashboard__created_by=self.request.user) |
            Q(task__todolist__dashboard__members=self.request.user)
        ).distinct()
    
    
"""СТОРІНКА ВИДАЛЕННЯ"""


#Видалення дошки
class DashboardDeleteView(LoginRequiredMixin, DashboardAccessMixin, DeleteView):
    model = Dashboard
    success_url = reverse_lazy("dashboard_list")
    pk_url_kwarg = "dashboard_pk"

    def get_queryset(self):
        return Dashboard.objects.filter(created_by=self.request.user)

#Видалення списка завдань
class TodoListDeleteView(LoginRequiredMixin, TodoListAccessMixin, DeleteView):
    model = TodoList
    pk_url_kwarg = "todolist_pk"

    def get_success_url(self):
        return reverse_lazy("todolist_list", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            })
    
    def get_queryset(self):
        return TodoList.objects.filter(dashboard__created_by=self.request.user)

#Видалення завдання
class TaskDeleteView(LoginRequiredMixin, TaskAccessMixin, DeleteView):
    model = Task
    pk_url_kwarg = "task_pk"

    def get_success_url(self):
        return reverse_lazy("task_list", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"]
            })
    
    def get_queryset(self):
        return Task.objects.filter(todolist__dashboard__created_by=self.request.user)
    
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
    
    def get_queryset(self):
        return Comment.objects.filter(task__todolist__dashboard__created_by=self.request.user)