import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

from django.contrib.auth.models import User
from student.models import Student

# Update User for admin
admin_user = User.objects.filter(username='admin').first()
if admin_user:
    admin_user.first_name = 'Alae'
    admin_user.last_name = 'Jaaouani'
    admin_user.save()
    print("Admin updated.")

# Update student User
student_user = User.objects.filter(username='sara_bennis').first()
if student_user:
    student_user.first_name = 'Chaymaa'
    student_user.last_name = 'Oualili'
    student_user.save()
    print("Student user updated.")

# Update Student profile
student_profile = Student.objects.filter(user__username='sara_bennis').first()
if student_profile:
    student_profile.first_name = 'Chaymaa'
    student_profile.last_name = 'Oualili'
    student_profile.save()
    print("Student profile updated.")
