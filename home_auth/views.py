from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 

@csrf_exempt 

def login_view(request):
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

@login_required(login_url='login')
def dashboard_view(request):
   
    if request.user.is_superuser or request.user.groups.filter(name='Enseignant').exists():
        return render(request, 'dashboard.html')

    else:
        return render(request, 'student-dashboard.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('login')