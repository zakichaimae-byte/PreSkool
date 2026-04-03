from django.urls import path
from . import views

urlpatterns = [
    path('dropout-risk/', views.dropout_prediction_view, name='dropout_risk'),
]
