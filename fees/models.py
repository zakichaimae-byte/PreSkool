from django.db import models
from student.models import Student

class Fee(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Payé'),
        ('Pending', 'En attente'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Frais de {self.student.first_name} - {self.amount} ({self.status})"
