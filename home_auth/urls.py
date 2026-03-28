from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='signup'), 
    path('forgot-password/', views.login_view, name='forgot-password'),
]