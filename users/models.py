from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length= 100)
    surname = models.CharField(max_length=100)
    employee_number = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} Profile'
