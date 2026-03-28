from django.urls import path
from . import views

urlpatterns = [
    path('my-classes/', views.my_classes_view, name='my_classes'),
    path('grades/', views.grade_entry_view, name='grade_entry'),
    path('attendance/', views.attendance_view, name='attendance'),
]
