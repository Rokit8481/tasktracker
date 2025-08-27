from django.urls import path
from .views import NoteListView, NoteDetailView, NoteCreateView

urlpatterns = [
    path('', NoteListView.as_view(), name = 'note_list'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name = 'note_detail'),
    path('note/create/', NoteCreateView.as_view(), name = 'note_create')
]
