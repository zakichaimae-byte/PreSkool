from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='teacher_profile')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
