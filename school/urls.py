from django.contrib import admin
from django.urls import path, include 
from home_auth import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student.urls')),
    path('faculty/', include('faculty.urls')),
    path('', include('home_auth.urls')),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
