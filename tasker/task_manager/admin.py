from django.contrib import admin
from .models import Dashboard, TodoList, Task, Comment

admin.site.register(Dashboard)
admin.site.register(TodoList)
admin.site.register(Task)
admin.site.register(Comment)