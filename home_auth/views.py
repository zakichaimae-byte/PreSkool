from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from student.models import Student
from teachers.models import Teacher
from departments.models import Department
from academic.models import Exam, TimeTable
from subjects.models import Subject
from .models import Notification
from django.db.models import Count
import json
import datetime

@csrf_exempt 

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        email_user = request.POST.get('email')
        password_user = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email_user)
            username_to_auth = user_obj.username
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            username_to_auth = email_user 

        user = authenticate(request, username=username_to_auth, password=password_user)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Bienvenue {user.username} !")
                return redirect('dashboard')
            else:
                messages.error(request, "Ce compte est désactivé.")
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")
            
    return render(request, 'login.html')

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message:
            Notification.objects.create(
                title=f"Nouveau message de {name}",
                message=f"Email: {email}\n\nMessage: {message}",
                category='contact'
            )
            messages.success(request, "votre message a été envoyé avec succès à l'administration.")
            return redirect('home')

    return render(request, 'landing.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet e-mail est déjà utilisé.")
            return render(request, 'register.html')

        username = email.split('@')[0]
        if User.objects.filter(username=username).exists():
            username = email

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, "Compte créé avec succès ! Bienvenue.")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Erreur lors de la création du compte : {e}")
            return render(request, 'register.html')
        
    return render(request, 'register.html')

@login_required(login_url='login')
def dashboard_view(request):
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]
    
    if request.user.is_superuser or request.user.groups.filter(name='Enseignant').exists():
        # General Stats
        student_count = Student.objects.count()
        teacher_count = Teacher.objects.count()
        department_count = Department.objects.count()
        
        # Departments Chart Data
        departments_data = Department.objects.annotate(num_teachers=Count('teachers'))
        dep_names = json.dumps([dep.name for dep in departments_data])
        dep_counts = json.dumps([dep.num_teachers for dep in departments_data])
        
        # ── Attendance Stats (today) ──
        today = datetime.date.today()
        from teacher_space.models import Attendance, Grade
        present_today = Attendance.objects.filter(date=today, status='Present').count()
        absent_today  = Attendance.objects.filter(date=today, status='Absent').count()
        
        # ── 7-day evolution (last 7 days) ──
        from django.db.models import Q
        evolution_labels = []
        evolution_present = []
        evolution_absent  = []
        for i in range(6, -1, -1):
            d = today - datetime.timedelta(days=i)
            evolution_labels.append(d.strftime('%d/%m'))
            evolution_present.append(Attendance.objects.filter(date=d, status='Present').count())
            evolution_absent.append(Attendance.objects.filter(date=d, status='Absent').count())
        
        # ── Latest Grades (with optional class/date filters) ──
        selected_class = request.GET.get('filter_class', '')
        selected_date  = request.GET.get('filter_date', '')
        
        grades_qs = Grade.objects.select_related('student', 'subject').order_by('-date_recorded')
        if selected_class:
            grades_qs = grades_qs.filter(student__student_class=selected_class)
        if selected_date:
            try:
                filter_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
                grades_qs = grades_qs.filter(date_recorded__date=filter_date)
            except ValueError:
                pass
        latest_grades = grades_qs[:20]
        
        # Available classes for filter dropdown
        all_classes = Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class')
        
        context = {
            'student_count': student_count,
            'teacher_count': teacher_count,
            'department_count': department_count,
            'male_students': Student.objects.filter(gender='Male').count(),
            'female_students': Student.objects.filter(gender='Female').count(),
            'dep_names': dep_names,
            'dep_counts': dep_counts,
            'notifications': notifications,
            # Attendance
            'present_today': present_today,
            'absent_today':  absent_today,
            # Evolution chart
            'evolution_labels':  json.dumps(evolution_labels),
            'evolution_present': json.dumps(evolution_present),
            'evolution_absent':  json.dumps(evolution_absent),
            # Grades table
            'latest_grades': latest_grades,
            'all_classes':   all_classes,
            'selected_class': selected_class,
            'selected_date':  selected_date,
        }
        return render(request, 'dashboard.html', context)

    else:
        # Student Dashboard
        student_profile = getattr(request.user, 'student_profile', None)
        if student_profile:
            # Fetch subjects for this student's class
            subjects_count = Subject.objects.filter(class_name=student_profile.student_class).count()
            
            # Fetch today's timetable
            today = datetime.datetime.now().strftime('%A')
            timetables = TimeTable.objects.filter(
                class_name=student_profile.student_class,
                day_of_week=today
            ).order_by('start_time')
            
            context = {
                'student': student_profile,
                'subjects_count': subjects_count,
                'timetables': timetables,
                'today': today,
                'notifications': notifications,
            }
            return render(request, 'student-dashboard.html', context)
        
        return render(request, 'student-dashboard.html', {'notifications': notifications})

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('home')

@login_required(login_url='login')
def profile_view(request):
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]
    return render(request, 'profile.html', {'notifications': notifications})

@login_required(login_url='login')
def student_subjects_view(request):
    student_profile = getattr(request.user, 'student_profile', None)
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]
    if not student_profile:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard')
    
    subjects = Subject.objects.filter(class_name=student_profile.student_class)
    return render(request, 'student_subjects.html', {'subjects': subjects, 'notifications': notifications})

@login_required(login_url='login')
def student_timetable_view(request):
    student_profile = getattr(request.user, 'student_profile', None)
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]
    if not student_profile:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard')
    
    timetables = TimeTable.objects.filter(class_name=student_profile.student_class).order_by('day_of_week', 'start_time')
    return render(request, 'student_timetable.html', {'timetables': timetables, 'notifications': notifications})

@login_required(login_url='login')
def student_exams_view(request):
    student_profile = getattr(request.user, 'student_profile', None)
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]
    if not student_profile:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard')
    
    exams = Exam.objects.filter(subject__class_name=student_profile.student_class).order_by('date')
    return render(request, 'student_exams.html', {'exams': exams, 'notifications': notifications})

@login_required(login_url='login')
def notifications_view(request):
    Notification.objects.filter(is_read=False).update(is_read=True)
    all_notifications = Notification.objects.all().order_by('-created_at')
    # pass empty notifications to base.html since they are all read now
    unread_notifications = Notification.objects.filter(is_read=False)[:5]
    return render(request, 'notifications.html', {'all_notifications': all_notifications, 'notifications': unread_notifications})
