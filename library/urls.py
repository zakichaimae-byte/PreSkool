from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_add, name='book_add'),
    path('borrow/<int:book_id>/', views.borrow_book_view, name='borrow_book'),
    path('return/<int:borrowing_id>/', views.return_book_view, name='return_book'),
    path('my-loans/', views.my_borrowings_view, name='my_borrowings'),
    path('manage-loans/', views.manage_borrowings_view, name='manage_borrowings'),
]
