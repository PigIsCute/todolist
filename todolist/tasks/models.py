from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('undo', 'undo'),
        ('done', 'done'),
    ]

    content = models.CharField(max_length=50, null=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='undo'
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content}, {self.status}"