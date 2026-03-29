from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    established_date = models.DateField()

    def __str__(self):
        return self.name
