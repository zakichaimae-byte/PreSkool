from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='exams')
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    coefficient = models.IntegerField(default=1)
    duration = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} - {self.subject.name}"

class TimeTable(models.Model):
    class_name = models.CharField(max_length=200)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.CharField(max_length=20, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_name} - {self.subject.name} ({self.day_of_week})"
