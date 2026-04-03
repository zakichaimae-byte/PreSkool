from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book, BookBorrowing
from django.contrib import messages
from datetime import date, timedelta
from student.models import Student

def book_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    books = Book.objects.all()
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
    if category:
        books = books.filter(category=category)
        
    return render(request, 'library/list.html', {'books': books, 'query': query, 'category_filter': category})

@login_required
def borrow_book_view(request, book_id):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Seuls les étudiants peuvent emprunter des livres.")
        return redirect('book_list')
        
    book = get_object_or_404(Book, id=book_id)
    student = request.user.student_profile
    
    if book.available_quantity <= 0:
        messages.error(request, "Ce livre n'est plus disponible actuellement.")
        return redirect('book_list')
        
    # Create borrowing record (14 days default)
    due_date = date.today() + timedelta(days=14)
    BookBorrowing.objects.create(
        book=book,
        student=student,
        due_date=due_date
    )
    
    # Update stock
    book.available_quantity -= 1
    book.save()
    
    messages.success(request, f"Vous avez emprunté '{book.title}'. À rendre avant le {due_date}.")
    return redirect('my_borrowings')

@login_required
def return_book_view(request, borrowing_id):
    # Only Admin or Teacher can validate returns for integrity
    if not request.user.is_superuser and request.user.groups.all().first().name != "Enseignant":
        messages.error(request, "Seul le bibliothécaire ou un enseignant peut valider un retour.")
        return redirect('dashboard')
        
    borrowing = get_object_or_404(BookBorrowing, id=borrowing_id)
    if borrowing.status == 'Returned':
        messages.info(request, "Ce livre a déjà été marqué comme rendu.")
        return redirect('manage_borrowings')
        
    borrowing.return_date = date.today()
    borrowing.status = 'Returned'
    borrowing.save()
    
    # Update stock
    borrowing.book.available_quantity += 1
    borrowing.book.save()
    
    messages.success(request, f"Le livre '{borrowing.book.title}' a été rendu avec succès.")
    return redirect('manage_borrowings')

@login_required
def my_borrowings_view(request):
    if not hasattr(request.user, 'student_profile'):
        return redirect('dashboard')
        
    loans = BookBorrowing.objects.filter(student=request.user.student_profile).order_by('-borrow_date')
    return render(request, 'library/my_borrowings.html', {'loans': loans})

@login_required
def manage_borrowings_view(request):
    # For Admin/Teachers
    all_loans = BookBorrowing.objects.all().order_by('-borrow_date')
    return render(request, 'library/manage_borrowings.html', {'loans': all_loans})

def book_add(request):
    # ... (keeping existing book_add logic)
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        category = request.POST.get('category')
        quantity = int(request.POST.get('quantity'))
        
        Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            quantity=quantity,
            available_quantity=quantity
        )
        messages.success(request, "Livre ajouté à la bibliothèque.")
        return redirect('book_list')
    return render(request, 'library/add.html')
