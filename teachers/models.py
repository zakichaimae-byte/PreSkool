from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
