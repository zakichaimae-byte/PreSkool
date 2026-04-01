from django.db import models

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('Soutenance', 'Soutenance'),
        ('TP/Atelier', 'TP / Atelier'),
        ('Conférence', 'Conférence'),
        ('Fête', 'Fête scolaire'),
        ('Autre', 'Autre'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    responsible = models.CharField(max_length=200, blank=True, null=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default='Autre')

    def __str__(self):
        return self.title
