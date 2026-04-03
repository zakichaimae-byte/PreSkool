from django.urls import path
from . import views

urlpatterns = [
    path('my-classes/', views.my_classes_view, name='my_classes'),
    path('grades/', views.grade_entry_view, name='grade_entry'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('quiz/create/', views.create_quiz_view, name='create_quiz'),
    path('quiz/add-question/<int:quiz_id>/', views.add_question_view, name='add_question'),
    path('quiz/delete/<int:quiz_id>/', views.delete_quiz_view, name='delete_quiz'),
    path('quizzes/', views.quiz_list_teacher_view, name='quiz_list_teacher'),
    path('generate-quiz-ai/', views.generate_quiz_ai_view, name='generate_quiz_ai'),
    path('log_session/', views.log_session_view, name='log_session'),
    path('session_logs/', views.session_logs_list_view, name='session_logs_list'),
    path('homework/submissions/<int:log_id>/', views.homework_submissions_view, name='homework_submissions'),
    path('homework/grade/<int:submission_id>/', views.grade_homework_view, name='grade_homework'),
    path('availability/', views.manage_availability_view, name='manage_availability'),
    path('appointments/', views.teacher_appointments_view, name='teacher_appointments'),
    path('appointments/update/<int:appt_id>/<str:status>/', views.update_appointment_status_view, name='update_appointment_status'),
    path('export-grades/<int:subject_id>/', views.export_grade_report_view, name='export_grade_report'),
]
