import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

from django.contrib.auth.models import User

# Add emails if empty
admin_user = User.objects.filter(username='admin').first()
if admin_user:
    admin_user.email = 'alaa.jaaouani@preskool.com'
    admin_user.save()
    print("Admin email updated.")

student_user = User.objects.filter(username='chaymaa_oualili').first()
if student_user:
    student_user.email = 'chaymaa.oualili@student.preskool.com'
    student_user.save()
    print("Student email updated.")
