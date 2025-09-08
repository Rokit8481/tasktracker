from django import forms 
from .models import Dashboard, TodoList, Task, Comment

class DashboardCreateForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ("title", "description")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Назва"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Опис",
                "rows": 3
            }),
        }
        

class TodoListCreateForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ("title", "description", "important")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Назва"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Опис",
                "rows": 3
            }),


        }

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "content", "status", "priority", "deadline")
        widgets = {
            "title": forms.TextInput(attrs = {
                "class": "form-control",
                "placeholder": "Напишіть заголовок вашого завдання",
            }),
            "content": forms.Textarea(attrs = {
                "class": "form-control",
                "placeholder": "Напишіть текст вашого завдання",
                "rows": 4,
            }),
            "status": forms.Select(attrs = {
                "class": "form-control",
            }),
            "priority": forms.Select(attrs = {
                "class": "form-control",
            }),
            "deadline": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            }
        
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs = {
                "class": "form-control",
                "placeholder": "Напишіть текст вашого коментаря",
                "rows": 4,
            }),
            }

