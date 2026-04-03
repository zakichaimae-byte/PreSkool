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

class TeacherAvailability(models.Model):
    DAYS = [
        ('1', 'Lundi'),
        ('2', 'Mardi'),
        ('3', 'Mercredi'),
        ('4', 'Jeudi'),
        ('5', 'Vendredi'),
        ('6', 'Samedi'),
        ('7', 'Dimanche'),
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.CharField(max_length=1, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.teacher} - {self.get_day_of_week_display()} ({self.start_time}-{self.end_time})"
