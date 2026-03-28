from django.shortcuts import render, get_object_or_404, redirect
from .models import Fee
from students.models import Student
from django.contrib import messages

def fee_list(request):
    fees = Fee.objects.all().select_related('student')
    return render(request, 'fees/list.html', {'fees': fees})

def fee_add(request):
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student')
        amount = request.POST.get('amount')
        status = request.POST.get('status')
        description = request.POST.get('description')
        
        student = get_object_or_404(Student, pk=student_id)
        Fee.objects.create(
            student=student,
            amount=amount,
            status=status,
            description=description
        )
        messages.success(request, "Frais ajoutés.")
        return redirect('fee_list')
    return render(request, 'fees/add.html', {'students': students})
