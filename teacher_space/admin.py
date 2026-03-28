from django.contrib import admin
from .models import Grade, Attendance

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'teacher', 'date_recorded')
    list_filter = ('subject', 'teacher', 'exam')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'teacher')
    list_filter = ('status', 'date', 'teacher')
    search_fields = ('student__first_name', 'student__last_name')
