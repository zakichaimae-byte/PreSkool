from django.urls import path
from . import views

urlpatterns = [
    path('', views.subject_list, name='subject_list'),
    path('add/', views.subject_add, name='subject_add'),
    path('edit/<int:pk>/', views.subject_edit, name='subject_edit'),
    path('delete/<int:pk>/', views.subject_delete, name='subject_delete'),
]
