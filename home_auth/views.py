from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        email_user = request.POST.get('email')
        password_user = request.POST.get('password')

        
        try:
            user_obj = User.objects.get(email=email_user)
            
            username_to_auth = user_obj.username
        except User.DoesNotExist:
            
            username_to_auth = None

        
        user = authenticate(request, username=username_to_auth, password=password_user)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('dashboard') 
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
            
    return render(request, 'login.html')
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('login')