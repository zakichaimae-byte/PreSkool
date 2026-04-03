from django.db import models
from django.contrib.auth.models import User
from student.models import Student

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('scientific', 'Scientifique'),
        ('literary', 'Littéraire'),
        ('historical', 'Historique'),
        ('artistic', 'Artistique'),
        ('other', 'Autre'),
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    isbn = models.CharField(max_length=20, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.author}"

class BookBorrowing(models.Model):
    STATUS_CHOICES = [
        ('Borrowed', 'Emprunté'),
        ('Returned', 'Rendu'),
        ('Overdue', 'En retard'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='book_loans')
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Borrowed')

    def __str__(self):
        return f"{self.student} -> {self.book} (Statut: {self.status})"
