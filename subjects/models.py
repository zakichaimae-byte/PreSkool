from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=200)
    class_name = models.CharField(max_length=200)
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name
