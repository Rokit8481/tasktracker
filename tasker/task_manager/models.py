from django.db import models
from django.contrib.auth.models import User

class Dashboard(models.Model):
    title =  models.CharField(max_length = 200, verbose_name = "Назва") 
    description =  models.TextField(verbose_name = "Опис", blank = True) 
    created_at = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name='dashboards', verbose_name = "Користувач")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Дошка"
        verbose_name_plural = "Дошки"

class TodoList(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete = models.CASCADE, related_name= 'todolists', verbose_name = "Дошка")
    title =  models.CharField(max_length = 200, verbose_name = "Назва") 
    description =  models.TextField(verbose_name = "Опис", blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    important = models.BooleanField(default = False, verbose_name = "Важливість")
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name= 'todolists', verbose_name = "Користувач")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Список завдань"
        verbose_name_plural = "Списки завдань"


class Task(models.Model):
    todolist = models.ForeignKey(TodoList, on_delete = models.CASCADE, related_name= 'tasks', verbose_name = "Список завдань")
    title = models.CharField(max_length = 200, verbose_name = "Назва") 
    content = models.TextField(verbose_name = "Контент", blank = True)
    status = models.CharField(max_length = 20, verbose_name = "Статус", default = 'draft', choices = [
    ('draft', 'Чернетка'),
    ('in_progress', 'В процесі'),
    ('completed', 'Завершено'),
    ('archived', 'Архів')
    ])

    priority = models.CharField(max_length = 10, verbose_name = "Приорітет", default = 'low', choices = [
    ('low', 'Низький'),
    ('medium', 'Середній'),
    ('high', 'Високий'),
    ('urgent', 'Терміновий')
    ])

    deadline = models.DateField(null=True, blank=True, verbose_name = "Дедлайн")
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = "Створено в")
    updated_at = models.DateTimeField(auto_now = True, verbose_name = "Оновлено в")
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name= 'tasks', verbose_name = "Користувач")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"