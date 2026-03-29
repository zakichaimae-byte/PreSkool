from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from django.contrib import messages

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/list.html', {'books': books})

def book_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        quantity = request.POST.get('quantity')
        
        Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            quantity=quantity,
            available_quantity=quantity
        )
        messages.success(request, "Livre ajouté.")
        return redirect('book_list')
    return render(request, 'library/add.html')
