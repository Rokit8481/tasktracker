from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Note
from .forms import NoteCreateForm
from django.urls import reverse_lazy

class NoteListView(ListView):
    model = Note
    template_name = 'note/note_list.html'
    context_object_name = 'notes'

class NoteDetailView(DetailView):
    model = Note
    template_name = 'note/note_detail.html'
    context_object_name = 'note'

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteCreateForm
    template_name = "note/note_create.html"
    success_url = reverse_lazy("note_list")