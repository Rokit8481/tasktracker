from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Dashboard, TodoList, Task
from .forms import DashboardCreateForm, TodoListCreateForm, TaskCreateForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


""""Логін, регестрація та вихід"""


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
class DashboardListView(ListView):
    model = Dashboard
    template_name = 'dashboard/dashboard_list.html'
    context_object_name = 'dashboards'

# Список списків завдань
class TodoListView(ListView):
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
class TaskListView(ListView):
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


""""ДЕТАЛЬНА СТОРІНКА"""

#Детальна сторінка дошки
class DashboardDetailView(DetailView, LoginRequiredMixin):
    model = Dashboard
    template_name = 'dashboard/dashboard_detail.html'
    context_object_name = 'dashboard'
    pk_url_kwarg = "dashboard_pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todolists"] = TodoList.objects.filter(created_by=self.request.user, dashboard_id=self.kwargs["dashboard_pk"])  
        return context
    
#Детальна сторінка списку завдань
class TodoListDetailView(DetailView, LoginRequiredMixin):
    model = TodoList
    template_name = 'todolist/todolist_detail.html'
    context_object_name = 'todolist'

    def get_object(self, queryset=None):
        return get_object_or_404(
            TodoList,
            pk=self.kwargs["todolist_pk"],
            dashboard_id=self.kwargs["dashboard_pk"]
        )
#Детальна сторінка завдання
class TaskDetailView(DetailView, LoginRequiredMixin):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Task,
            pk=self.kwargs["task_pk"],
            todolist_id=self.kwargs["todolist_pk"]
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['todolist'] = task.todolist
        context['dashboard'] = task.todolist.dashboard
        return context


""""CТОРІНКА СТВОРЕННЯ"""


#Сторінка створення дошки
class DashboardCreateView(CreateView, LoginRequiredMixin):
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
class TodoListCreateView(CreateView, LoginRequiredMixin):
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
class TaskCreateView(CreateView, LoginRequiredMixin):
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


""""СТОРІНКА РЕДАГУВАННЯ"""


#Редагування дошки
class DashboardUpdateView(UpdateView, LoginRequiredMixin):
    model = Dashboard
    form_class = DashboardCreateForm
    template_name = 'dashboard/dashboard_edit.html'
    success_url = reverse_lazy("dashboard_list")
    pk_url_kwarg = "dashboard_pk"

    def get_queryset(self):
        return Dashboard.objects.filter(created_by=self.request.user)

#Редагування списка завдань
class TodoListUpdateView(UpdateView, LoginRequiredMixin):
    model = TodoList
    form_class = TodoListCreateForm
    template_name = 'todolist/todolist_edit.html'
    pk_url_kwarg = "todolist_pk"
    
    def get_success_url(self):
        return reverse_lazy("todolist_list", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            })
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        return context
    
    def get_queryset(self):
        return TodoList.objects.filter(dashboard__created_by=self.request.user)

    
#Редагування завдання
class TaskUpdateView(UpdateView, LoginRequiredMixin):
    model = Task
    form_class = TaskCreateForm
    template_name = 'task/task_edit.html'
    pk_url_kwarg = "task_pk"
    
    def get_success_url(self):
        return reverse_lazy("task_list", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"]
            })
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = get_object_or_404(Dashboard, pk=self.kwargs["dashboard_pk"])
        context["todolist"] = get_object_or_404(TodoList, pk=self.kwargs["todolist_pk"])
        return context

    def get_queryset(self):
        return Task.objects.filter(todolist__dashboard__created_by=self.request.user)
    

""""СТОРІНКА ВИДАЛЕННЯ"""


#Видалення дошки
class DashboardDeleteView(DeleteView, LoginRequiredMixin):
    model = Dashboard
    success_url = reverse_lazy("dashboard_list")
    pk_url_kwarg = "dashboard_pk"

    def get_queryset(self):
        return Dashboard.objects.filter(created_by=self.request.user)

#Видалення списка завдань
class TodoListDeleteView(DeleteView, LoginRequiredMixin):
    model = TodoList
    pk_url_kwarg = "todolist_pk"

    def get_success_url(self):
        return reverse_lazy("todolist_list", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            })
    
    def get_queryset(self):
        return TodoList.objects.filter(dashboard__created_by=self.request.user)

#Видалення завдання
class TaskDeleteView(DeleteView, LoginRequiredMixin):
    model = Task
    pk_url_kwarg = "task_pk"

    def get_success_url(self):
        return reverse_lazy("task_list", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"]
            })
    
    def get_queryset(self):
        return Task.objects.filter(todolist__dashboard__created_by=self.request.user)