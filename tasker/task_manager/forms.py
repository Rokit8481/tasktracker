from django import forms 
from .models import Note

class NoteCreateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs = {
                "class": "form-control",
                "placeholder": "Напишіть заголовок вашої нотатки",
            }),
            "content": forms.Textarea(attrs = {
                "class": "form-control",
                "placeholder": "Напишіть текст вашої нотатки",
                "rows": 4,
            }),
            }
