from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher
from departments.models import Department
from django.contrib import messages

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/list.html', {'teachers': teachers})

def teacher_add(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department_id = request.POST.get('department')
        
        department = get_object_or_404(Department, pk=department_id)
        
        Teacher.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            department=department
        )
        messages.success(request, "Enseignant ajouté avec succès.")
        return redirect('teacher_list')
    return render(request, 'teachers/add.html', {'departments': departments})

def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    departments = Department.objects.all()
    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.email = request.POST.get('email')
        teacher.phone = request.POST.get('phone')
        department_id = request.POST.get('department')
        
        teacher.department = get_object_or_404(Department, pk=department_id)
        teacher.save()
        messages.success(request, "Enseignant mis à jour.")
        return redirect('teacher_list')
    return render(request, 'teachers/edit.html', {'teacher': teacher, 'departments': departments})

def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, "Enseignant supprimé.")
        return redirect('teacher_list')
    return render(request, 'teachers/delete.html', {'teacher': teacher})
