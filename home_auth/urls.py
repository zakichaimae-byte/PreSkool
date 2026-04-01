from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='signup'), 
    path('forgot-password/', views.login_view, name='forgot-password'),
    
    # STUDENT SPACE
    path('my-courses/', views.student_subjects_view, name='my_courses_list'),
    path('my-timetable/', views.student_timetable_view, name='student_timetable_full'),
    path('my-exams/', views.student_exams_view, name='student_exams_list'),
    path('notifications/', views.notifications_view, name='notifications'),
]