from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Task
from .forms import TaskCreateForm
from django.urls import reverse_lazy

class TaskListView(ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "task/task_create.html"
    success_url = reverse_lazy("task_list")