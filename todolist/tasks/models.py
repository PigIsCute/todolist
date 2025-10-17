from django.db import models

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

    def __str__(self):
        return f"{self.content}, {self.status}"