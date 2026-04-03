from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from home_auth import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('teachers/', include('teachers.urls')),
    path('departments/', include('departments.urls')),
    path('subjects/', include('subjects.urls')),
    path('academic/', include('academic.urls')),
    path('fees/', include('fees.urls')),
    path('events/', include('events.urls')),
    path('library/', include('library.urls')),
    path('teacher-space/', include('teacher_space.urls')),
    path('student/', include('student.urls')),
    path('faculty/', include('faculty.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('analytics/', include('analytics.urls')),
    path('', include('home_auth.urls')),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
