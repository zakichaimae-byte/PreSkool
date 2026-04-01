from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject
from teachers.models import Teacher
from django.contrib import messages

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/list.html', {'subjects': subjects})

def subject_add(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        class_name = request.POST.get('class_name')
        teacher_id = request.POST.get('teacher')
        
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        
        Subject.objects.create(
            name=name,
            class_name=class_name,
            teacher=teacher
        )
        messages.success(request, "Matière ajoutée avec succès.")
        return redirect('subject_list')
    return render(request, 'subjects/add.html', {'teachers': teachers})

def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        subject.name = request.POST.get('name')
        subject.class_name = request.POST.get('class_name')
        teacher_id = request.POST.get('teacher')
        
        subject.teacher = get_object_or_404(Teacher, pk=teacher_id)
        subject.save()
        messages.success(request, "Matière mise à jour.")
        return redirect('subject_list')
    return render(request, 'subjects/edit.html', {'subject': subject, 'teachers': teachers})

def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, "Matière supprimée.")
        return redirect('subject_list')
    return render(request, 'subjects/delete.html', {'subject': subject})
