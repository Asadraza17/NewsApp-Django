# Create your models here.
from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @classmethod
    def delete_all(cls):
        cls.objects.all().delete()

