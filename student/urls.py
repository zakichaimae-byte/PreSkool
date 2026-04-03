from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_student, name='add_student'),
    path('list/', views.student_list, name='student_list'),
    path('details/<str:student_id>/', views.student_details, name='student_details'),
    path('edit/<str:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<str:student_id>/', views.delete_student, name='delete_student'),
    path('logbook/', views.student_session_logs_view, name='student_session_logs'),
    path('quiz_list/', views.student_quiz_list_view, name='student_quiz_list'),
    path('take_quiz/<int:quiz_id>/', views.take_quiz_view, name='take_quiz'),
    path('submit_homework/<int:log_id>/', views.submit_homework_view, name='submit_homework'),
    path('book_appointment/', views.book_appointment_view, name='book_appointment'),
    path('my_appointments/', views.student_appointments_view, name='student_appointments'),
    path('performance/', views.student_performance_view, name='student_performance'),
]