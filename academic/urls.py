from django.urls import path
from . import views

urlpatterns = [
    path('holidays/', views.holiday_list, name='holiday_list'),
    path('holidays/add/', views.holiday_add, name='holiday_add'),
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/add/', views.exam_add, name='exam_add'),
    path('timetable/', views.timetable_list, name='timetable_list'),
    path('timetable/add/', views.timetable_add, name='timetable_add'),
]
