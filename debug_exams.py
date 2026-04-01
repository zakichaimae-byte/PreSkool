import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from student.models import Student
from academic.models import Exam
from subjects.models import Subject

print("--- Students ---")
for s in Student.objects.all():
    print(f"User: {s.user.username if s.user else 'N/A'}, Class: {s.student_class}")

print("\n--- Subjects ---")
for sub in Subject.objects.all():
    print(f"Name: {sub.name}, Class: {sub.class_name}")

print("\n--- Exams ---")
for e in Exam.objects.all():
    print(f"Examen: {e.name}, Subject: {e.subject.name}, SubClass: {e.subject.class_name}")
