from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from students.models import Student
from teachers.models import Teacher
from departments.models import Department

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
   
    if request.user.is_superuser or request.user.groups.filter(name='Enseignant').exists():
        context = {
            'student_count': Student.objects.count(),
            'teacher_count': Teacher.objects.count(),
            'department_count': Department.objects.count(),
            'male_students': Student.objects.filter(gender='M').count(),
            'female_students': Student.objects.filter(gender='F').count(),
        }
        return render(request, 'dashboard.html', context)

    else:
        return render(request, 'student-dashboard.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('login')