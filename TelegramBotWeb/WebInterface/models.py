from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField("Название отдела", max_length=255)

    def __str__(self):
        return self.name
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)


