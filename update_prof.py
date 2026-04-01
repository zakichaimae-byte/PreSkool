import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

from django.contrib.auth.models import User
from teachers.models import Teacher

# Update prof_test user and teacher profile
prof_user = User.objects.filter(username='prof_test').first()
if prof_user:
    prof_user.first_name = 'Chaimae'
    prof_user.last_name = 'Zaki'
    prof_user.email = 'chaimae.zaki@prof.preskool.com'
    prof_user.save()
    print("Teacher User updated.")

prof_teacher = Teacher.objects.filter(user__username='prof_test').first()
if prof_teacher:
    prof_teacher.first_name = 'Chaimae'
    prof_teacher.last_name = 'Zaki'
    prof_teacher.save()
    print("Teacher profile updated.")
