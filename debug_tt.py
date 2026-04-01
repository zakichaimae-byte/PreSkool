import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from student.models import Student
from academic.models import Exam, TimeTable
from subjects.models import Subject

print("\n--- TimeTable ---")
for tt in TimeTable.objects.all():
    print(f"Class: {tt.class_name}, Subject: {tt.subject.name}, Day: {tt.day_of_week}")
