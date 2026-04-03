from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .models import Grade, Attendance
from academic.models import TimeTable, Exam
from student.models import Student
from subjects.models import Subject
from teachers.models import Teacher
from django.contrib import messages
from .services import TeacherDashboardService

@login_required
def my_classes_view(request):
    if not hasattr(request.user, 'teacher_profile'):
        messages.error(request, "Votre compte n'est pas lié à un profil enseignant.")
        return redirect('dashboard')
    teacher = request.user.teacher_profile
        
    timetables = TimeTable.objects.filter(subject__teacher=teacher).order_by('day_of_week', 'start_time')
    return render(request, 'teacher_space/my_classes.html', {'timetables': timetables})

@login_required
def grade_entry_view(request):
    if not hasattr(request.user, 'teacher_profile'):
        messages.error(request, "Votre compte n'est pas lié à un profil enseignant.")
        return redirect('dashboard')
    teacher = request.user.teacher_profile
        
    students = Student.objects.all()
    subjects = Subject.objects.all()
    exams = Exam.objects.all()
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        exam_id = request.POST.get('exam')
        score = request.POST.get('score')
        comments = request.POST.get('comments')
        
        student = get_object_or_404(Student, pk=student_id)
        subject = get_object_or_404(Subject, pk=subject_id)
        # Optional exam
        exam = get_object_or_404(Exam, pk=exam_id) if exam_id else None
        
        Grade.objects.create(
            student=student,
            subject=subject,
            exam=exam,
            teacher=teacher,
            score=score,
            comments=comments
        )
        messages.success(request, "Note enregistrée avec succès.")
        return redirect('grade_entry')
        
    return render(request, 'teacher_space/grade_entry.html', {
        'students': students,
        'subjects': subjects,
        'exams': exams
    })

@login_required
def attendance_view(request):
    if not hasattr(request.user, 'teacher_profile'):
        messages.error(request, "Votre compte n'est pas lié à un profil enseignant.")
        return redirect('dashboard')
    teacher = request.user.teacher_profile
        
    students = Student.objects.all()
    
    if request.method == 'POST':
        date = request.POST.get('date')
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'status': status, 'teacher': teacher}
                )
        messages.success(request, "Présences enregistrées.")
        return redirect('attendance')
        
    return render(request, 'teacher_space/attendance.html', {'students': students})

from academic.models import Quiz, Question, Choice, CourseSessionLog, HomeworkSubmission, Appointment
from teachers.models import Teacher, TeacherAvailability
from teachers.forms import TeacherAvailabilityForm
from academic.forms import QuizForm, QuestionForm, ChoiceForm, CourseSessionLogForm
from home_auth.models import Notification

@login_required
def create_quiz_view(request):
    if not hasattr(request.user, 'teacher_profile') and not request.user.is_superuser:
        messages.error(request, "Votre compte n'est pas lié à un profil enseignant.")
        return redirect('dashboard')
    
    teacher = getattr(request.user, 'teacher_profile', None)
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.teacher = teacher
            quiz.save()
            messages.success(request, "Quiz créé avec succès. Vous pouvez maintenant ajouter des questions.")
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuizForm()
    
    return render(request, 'teacher_space/create_quiz.html', {'form': form})

@login_required
def add_question_view(request, quiz_id):
    if request.user.is_superuser:
        quiz = get_object_or_404(Quiz, id=quiz_id)
    else:
        quiz = get_object_or_404(Quiz, id=quiz_id, teacher=request.user.teacher_profile)
    
    if request.method == 'POST':
        q_form = QuestionForm(request.POST)
        if q_form.is_valid():
            question = q_form.save(commit=False)
            question.quiz = quiz
            question.save()
            
            # Add 4 choices (simple implementation)
            for i in range(1, 5):
                choice_text = request.POST.get(f'choice_{i}')
                is_correct = request.POST.get(f'correct') == str(i)
                if choice_text:
                    Choice.objects.create(question=question, text=choice_text, is_correct=is_correct)
            
            messages.success(request, "Question ajoutée.")
            if 'save_and_add' in request.POST:
                return redirect('add_question', quiz_id=quiz.id)
            return redirect('quiz_list_teacher')
    else:
        q_form = QuestionForm()
    
    return render(request, 'teacher_space/add_question.html', {
        'quiz': quiz,
        'q_form': q_form,
    })

@login_required
def generate_quiz_ai_view(request):
    if not hasattr(request.user, 'teacher_profile') and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('dashboard')
    
    teacher = getattr(request.user, 'teacher_profile', None)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'generate':
            topic = request.POST.get('topic', '')
            count = int(request.POST.get('count', 3))
            subject_id = request.POST.get('subject')
            
            # --- Python Service Layer for AI Generation ---
            service = TeacherDashboardService()
            questions_data = service.mock_ai_quiz_generation(topic, count)
            
            request.session['temp_quiz_data'] = {
                'title': f"Quiz sur {topic}",
                'subject_id': subject_id,
                'questions': questions_data
            }
            
            return render(request, 'teacher_space/generate_quiz_ai.html', {
                'topic': topic,
                'subject_id': subject_id,
                'questions': questions_data,
                'preview': True
            })
            
        elif action == 'save':
            topic = request.POST.get('topic')
            subject_id = request.POST.get('subject_id')
            subject = Subject.objects.filter(id=subject_id).first() if subject_id else Subject.objects.first()
            # Create Quiz
            quiz = Quiz.objects.create(
                title=f"Quiz IA : {topic}",
                teacher=teacher,
                subject=subject,
                due_date=date.today() + timedelta(days=7)
            )
            
            # Create Questions & Choices from submitted data
            q_count = int(request.POST.get('q_count', 0))
            for i in range(q_count):
                q_text = request.POST.get(f'q_{i}_text')
                if q_text:
                    question = Question.objects.create(quiz=quiz, text=q_text)
                    for j in range(4):
                        c_text = request.POST.get(f'q_{i}_c_{j}')
                        is_correct = request.POST.get(f'q_{i}_correct') == str(j)
                        if c_text:
                            Choice.objects.create(question=question, text=c_text, is_correct=is_correct)
            
            messages.success(request, f"Le quiz '{quiz.title}' a été généré et publié avec succès !")
            return redirect('quiz_list_teacher')
            
    subjects = Subject.objects.filter(teacher=teacher) if teacher else Subject.objects.all()
    return render(request, 'teacher_space/generate_quiz_ai.html', {'preview': False, 'subjects': subjects})

@login_required
def quiz_list_teacher_view(request):
    if request.user.is_superuser:
        quizzes = Quiz.objects.all()
    else:
        teacher = request.user.teacher_profile
        quizzes = Quiz.objects.filter(teacher=teacher)
    return render(request, 'teacher_space/quiz_list.html', {'quizzes': quizzes})

@login_required
def delete_quiz_view(request, quiz_id):
    if request.user.is_superuser:
        quiz = get_object_or_404(Quiz, id=quiz_id)
    else:
        quiz = get_object_or_404(Quiz, id=quiz_id, teacher=request.user.teacher_profile)
    
    quiz_title = quiz.title
    quiz.delete()
    messages.success(request, f"Le quiz '{quiz_title}' a été supprimé avec succès.")
    return redirect('quiz_list_teacher')

@login_required
def log_session_view(request):
    if not hasattr(request.user, 'teacher_profile') and not request.user.is_superuser:
        messages.error(request, "Votre compte n'est pas lié à un profil enseignant.")
        return redirect('dashboard')
    
    teacher = getattr(request.user, 'teacher_profile', None)
    if request.method == 'POST':
        form = CourseSessionLogForm(request.POST, request.FILES)
        if form.is_valid():
            log = form.save(commit=False)
            log.teacher = teacher
            log.save()
            messages.success(request, "Séance de cours enregistrée dans le cahier de texte.")
            return redirect('session_logs_list')
    else:
        form = CourseSessionLogForm()
    
    return render(request, 'teacher_space/log_session.html', {'form': form})

@login_required
def session_logs_list_view(request):
    if request.user.is_superuser:
        logs = CourseSessionLog.objects.all().order_by('-date')
    else:
        teacher = request.user.teacher_profile
        logs = CourseSessionLog.objects.filter(teacher=teacher).order_by('-date')
    return render(request, 'teacher_space/session_logs_list.html', {'logs': logs})

@login_required
def homework_submissions_view(request, log_id):
    session_log = get_object_or_404(CourseSessionLog, id=log_id)
    # Check permission
    if not request.user.is_superuser and session_log.teacher != request.user.teacher_profile:
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    submissions = session_log.submissions.all().order_by('-submitted_at')
    return render(request, 'teacher_space/homework_submissions.html', {
        'session_log': session_log,
        'submissions': submissions
    })

@login_required
def grade_homework_view(request, submission_id):
    submission = get_object_or_404(HomeworkSubmission, id=submission_id)
    # Check permission
    if not request.user.is_superuser and submission.session_log.teacher != request.user.teacher_profile:
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        submission.teacher_feedback = request.POST.get('feedback')
        submission.score = request.POST.get('score')
        submission.status = 'Graded'
        submission.save()
        
        # --- Notification ---
        Notification.objects.create(
            user=submission.student.user,
            title="Devoir Corrigé",
            message=f"Votre travail pour '{submission.session_log.subject}' a été corrigé. Note : {submission.score}/20.",
            category='system',
            link='/student/logbook/'
        )
        
        messages.success(request, "Note et feedback enregistrés.")
        return redirect('homework_submissions', log_id=submission.session_log.id)
    
    return render(request, 'teacher_space/grade_homework.html', {'submission': submission})

@login_required
def manage_availability_view(request):
    if not hasattr(request.user, 'teacher_profile') and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('dashboard')
    
    teacher = getattr(request.user, 'teacher_profile', None)
    if request.method == 'POST':
        form = TeacherAvailabilityForm(request.POST)
        if form.is_valid():
            avail = form.save(commit=False)
            avail.teacher = teacher
            avail.save()
            messages.success(request, "Disponibilité ajoutée.")
            return redirect('manage_availability')
    else:
        form = TeacherAvailabilityForm()
    
    # List current availabilities
    if teacher:
        availabilities = teacher.availabilities.all().order_by('day_of_week', 'start_time')
    else:
        availabilities = TeacherAvailability.objects.all().order_by('teacher', 'day_of_week')
        
    return render(request, 'teacher_space/manage_availability.html', {
        'form': form,
        'availabilities': availabilities
    })

@login_required
def teacher_appointments_view(request):
    if request.user.is_superuser:
        appointments = Appointment.objects.all().order_by('-date', 'time_slot')
    elif hasattr(request.user, 'teacher_profile'):
        appointments = Appointment.objects.filter(teacher=request.user.teacher_profile).order_by('-date', 'time_slot')
    else:
        return redirect('dashboard')
        
    return render(request, 'teacher_space/appointments_list.html', {'appointments': appointments})

@login_required
def update_appointment_status_view(request, appt_id, status):
    if request.user.is_superuser:
        appt = get_object_or_404(Appointment, id=appt_id)
    elif hasattr(request.user, 'teacher_profile'):
        appt = get_object_or_404(Appointment, id=appt_id, teacher=request.user.teacher_profile)
    else:
        return redirect('dashboard')
    
    if status in ['Approved', 'Cancelled']:
        appt.status = status
        appt.save()
        msg_type = "confirmé" if status == 'Approved' else "annulé"
        messages.success(request, f"Le rendez-vous avec {appt.parent} a été {msg_type}.")
    
    return redirect('teacher_appointments')

@login_required
def export_grade_report_view(request, subject_id):
    """View to download grade reports as CSV, powered by Python Service."""
    from django.http import HttpResponse
    from django.shortcuts import get_object_or_404
    teacher = getattr(request.user, 'teacher_profile', None)
    if not teacher and not request.user.is_superuser:
        return redirect('dashboard')
        
    service = TeacherDashboardService()
    csv_content, subject_name = service.generate_grade_report_csv(teacher, subject_id)
    
    response = HttpResponse(csv_content, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="notes_{subject_name}_{date.today()}.csv"'
    return response
