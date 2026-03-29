from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    student_class = models.CharField(max_length=100)
    section = models.CharField(max_length=50, blank=True, null=True)
    admission_number = models.CharField(max_length=50, blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    joining_date = models.DateField(auto_now_add=True)
    student_image = models.ImageField(upload_to='students/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
