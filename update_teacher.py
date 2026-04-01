import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

from teachers.models import Teacher
from django.contrib.auth.models import User

# Check if admin has a teacher profile and update it
teacher = Teacher.objects.filter(user__username='admin').first()
if teacher:
    teacher.first_name = 'Jaaouani'
    teacher.last_name = 'Alae'
    teacher.save()
    print("Admin Teacher profile updated.")
else:
    print("Admin Teacher profile not found.")
