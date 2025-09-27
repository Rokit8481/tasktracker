from django import forms 
from .models import Dashboard, TodoList, Task, Comment
from django.contrib.auth.models import User
from django.utils import timezone

class AddMemberForm(forms.Form):
    username = forms.CharField(
        label="Імʼя користувача",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control-custom",
            "placeholder": "Введіть імʼя користувача"
        })
    )

    def __init__(self, *args, **kwargs):
        self.dashboard = kwargs.pop("dashboard", None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Користувача з таким ім'ям не існує.")

        if self.dashboard and user in self.dashboard.members.all():
            raise forms.ValidationError("Цей користувач вже є учасником цієї дошки.")

        if self.dashboard and user == self.dashboard.created_by:
            raise forms.ValidationError("Цей користувач є власником дошки.")

        return user


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

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title or len(title.strip()) == 0:
            raise forms.ValidationError("Назва не може бути порожньою.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description or len(description.strip()) == 0:
            raise forms.ValidationError("Опис не може бути порожнім.")
        return description


class TodoListCreateForm(forms.ModelForm):
    important = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input-custom",
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

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title or len(title.strip()) == 0:
            raise forms.ValidationError("Назва не може бути порожньою.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description or len(description.strip()) == 0:
            raise forms.ValidationError("Опис не може бути порожнім.")
        return description


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

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title or len(title.strip()) == 0:
            raise forms.ValidationError("Заголовок не може бути порожнім.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content or len(content.strip()) == 0:
            raise forms.ValidationError("Текст завдання не може бути порожнім.")
        return content

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("Дедлайн не може бути в минулому.")
        return deadline


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

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content or len(content.strip()) == 0:
            raise forms.ValidationError("Коментар не може бути порожнім.")
        return content
