from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from django.contrib import messages

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

def student_add(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        section = request.POST.get('section')
        admission_number = request.POST.get('admission_number')
        mobile_number = request.POST.get('mobile_number')
        # student_image handling can be added later if needed
        
        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            student_class=student_class,
            section=section,
            admission_number=admission_number,
            mobile_number=mobile_number
        )
        messages.success(request, "Étudiant ajouté avec succès.")
        return redirect('student_list')
    return render(request, 'students/add.html')

def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student_id = request.POST.get('student_id')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.student_class = request.POST.get('student_class')
        student.section = request.POST.get('section')
        student.admission_number = request.POST.get('admission_number')
        student.mobile_number = request.POST.get('mobile_number')
        student.save()
        messages.success(request, "Étudiant mis à jour.")
        return redirect('student_list')
    return render(request, 'students/edit.html', {'student': student})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Étudiant supprimé.")
        return redirect('student_list')
    return render(request, 'students/delete.html', {'student': student})
