from django.db import models

class Note(models.Model):
    title = models.CharField(max_length = 200, verbose_name = "Назва") 
    content = models.TextField(verbose_name = "Контент")

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = "Нотатка"
        verbose_name_plural = "Нотатки"