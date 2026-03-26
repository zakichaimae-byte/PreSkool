from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        email_user = request.POST.get('email')
        password_user = request.POST.get('password')

        # 1. On cherche d'abord l'utilisateur par son email
        try:
            user_obj = User.objects.get(email=email_user)
            # On récupère le vrai username (dans ton cas : 'admin')
            username_to_auth = user_obj.username
        except User.DoesNotExist:
            # Si l'email n'existe pas, on met une valeur qui échouera à l'auth
            username_to_auth = None

        # 2. On tente l'authentification avec le vrai username trouvé
        user = authenticate(request, username=username_to_auth, password=password_user)

        if user is not None:
            login(request, user)
            # Une fois connecté, on redirige (on peut mettre 'login' en attendant le dashboard)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('dashboard') 
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
            
    return render(request, 'login.html')
def dashboard_view(request):
    return render(request, 'dashboard.html')