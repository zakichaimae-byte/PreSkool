from django.contrib import admin
from django.urls import path, include 
from home_auth import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('faculty/', include('faculty.urls')),
    path('departments/', include('departments.urls')),
    path('teachers/', include('teachers.urls')),
    path('subjects/', include('subjects.urls')),
    path('academic/', include('academic.urls')),
    
    path('', include('home_auth.urls')),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
