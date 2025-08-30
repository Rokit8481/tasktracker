from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Dashboard, TodoList, Task
from .forms import DashboardCreateForm, TodoListCreateForm, TaskCreateForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.http import HttpRequest


""""Вхід, регестрація та вихід"""


#Логін
def login_view(request: HttpRequest):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard_list')
    return render(request, 'registration/login.html', {'form': form})

#Вихід
def logout_view(request: HttpRequest):
    logout(request)
    return redirect('/')

#Регестрація
def register(request: HttpRequest):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


"""СПИСКИ"""


#Список Дошок
class DashboardListView(ListView):
    model = Dashboard
    template_name = 'dashboard/dashboard_list.html'
    context_object_name = 'dashboards'

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
        context["dashboards"] = TodoList.objects.filter(created_by=self.request.user)  
        return context


""""ДЕТАЛЬНА СТОРІНКА"""

#Детальна сторінка завдання
class TaskDetailView(DetailView):
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
class DashboardCreateView(CreateView):
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
class TodoListCreateView(CreateView):
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
class TaskCreateView(CreateView):
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
class DashboardUpdateView(UpdateView):
    model = Dashboard
    form_class = DashboardCreateForm
    template_name = 'dashboard/dashboard_edit.html'
    success_url = reverse_lazy("dashboard_list")
    pk_url_kwarg = "dashboard_pk"

    def get_queryset(self):
        return Dashboard.objects.filter(created_by=self.request.user)

#Редагування списка завдань
class TodoListUpdateView(UpdateView):
    model = TodoList
    form_class = TodoListCreateForm
    template_name = 'todolist/todolist_edit.html'
    
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
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'task/task_edit.html'
    
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
class DashboardDeleteView(DeleteView):
    model = Dashboard
    success_url = reverse_lazy("dashboard_list")
    pk_url_kwarg = "dashboard_pk"

    def get_queryset(self):
        return Dashboard.objects.filter(created_by=self.request.user)

#Видалення списка завдань
class TodoListDeleteView(DeleteView):
    model = TodoList

    def get_success_url(self):
        return reverse_lazy("todolist_list", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            })
    
    def get_queryset(self):
        return TodoList.objects.filter(dashboard__created_by=self.request.user)

#Видалення завдання
class TaskDeleteView(DeleteView):
    model = Task

    def get_success_url(self):
        return reverse_lazy("task_list", kwargs = {
            "dashboard_pk": self.kwargs["dashboard_pk"],
            "todolist_pk": self.kwargs["todolist_pk"]
            })
    
    def get_queryset(self):
        return Task.objects.filter(todolist__dashboard__created_by=self.request.user)