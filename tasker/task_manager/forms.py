from django import forms 
from .models import Dashboard, TodoList, Task, Comment

class DashboardCreateForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ("title", "description")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control-custom",
                "placeholder": "Назва"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control-custom",
                "placeholder": "Опис",
                "rows": 3
            }),
        }
        

class TodoListCreateForm(forms.ModelForm):
    important = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input-custom",
            "style": "width:auto; display:inline-block; margin:0;"
        })
    )

    class Meta:
        model = TodoList
        fields = ("title", "description", "important")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control-custom",
                "placeholder": "Назва"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control-custom",
                "placeholder": "Опис",
                "rows": 3
            }),
        }


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "content", "status", "priority", "deadline")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control-custom",
                "placeholder": "Напишіть заголовок вашого завдання",
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control-custom",
                "placeholder": "Напишіть текст вашого завдання",
                "rows": 4,
            }),
            "status": forms.Select(attrs={
                "class": "form-control-custom",
            }),
            "priority": forms.Select(attrs={
                "class": "form-control-custom",
            }),
            "deadline": forms.DateInput(attrs={
                "class": "form-control-custom",
                "type": "date"
            }),
        }
        

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control-custom",
                "placeholder": "Напишіть текст вашого коментаря",
                "rows": 4,
            }),
        }
