from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.login_view, name='signup'), 
    path('forgot-password/', views.login_view, name='forgot-password'),
]