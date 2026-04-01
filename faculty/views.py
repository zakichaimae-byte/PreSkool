from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # On utilise index.html car c'est lui qui "extends" base.html
    return render(request, 'index.html')