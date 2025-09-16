from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    student_number = models.CharField('Numero de aluno', max_length=10, unique=True)

    def __str__(self):
        return f"{self.username} ({self.student_number})"