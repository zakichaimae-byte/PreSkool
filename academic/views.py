from django.shortcuts import render, get_object_or_404, redirect
from .models import Holiday, Exam, TimeTable
from subjects.models import Subject
from teachers.models import Teacher
from django.contrib import messages

# HOLIDAYS
def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'academic/holiday_list.html', {'holidays': holidays})

def holiday_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        Holiday.objects.create(name=name, start_date=start_date, end_date=end_date)
        messages.success(request, "Vacances ajoutées.")
        return redirect('holiday_list')
    return render(request, 'academic/holiday_add.html')

# EXAMS
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'academic/exam_list.html', {'exams': exams})

def exam_add(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        subject_id = request.POST.get('subject')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        
        subject = get_object_or_404(Subject, pk=subject_id)
        Exam.objects.create(name=name, subject=subject, date=date, start_time=start_time)
        messages.success(request, "Examen ajouté.")
        return redirect('exam_list')
    return render(request, 'academic/exam_add.html', {'subjects': subjects})

# TIMETABLE
def timetable_list(request):
    timetables = TimeTable.objects.all().order_by('day_of_week', 'start_time')
    return render(request, 'academic/timetable_list.html', {'timetables': timetables})

def timetable_add(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        subject_id = request.POST.get('subject')
        day_of_week = request.POST.get('day_of_week')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        subject = get_object_or_404(Subject, pk=subject_id)
        
        TimeTable.objects.create(
            class_name=class_name,
            subject=subject,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time
        )
        messages.success(request, "Créneau ajouté à l'emploi du temps.")
        return redirect('timetable_list')
    return render(request, 'academic/timetable_add.html', {'subjects': subjects})

def timetable_edit(request, pk):
    entry = get_object_or_404(TimeTable, pk=pk)
    subjects = Subject.objects.all()
    if request.method == 'POST':
        entry.class_name = request.POST.get('class_name')
        subject_id = request.POST.get('subject')
        entry.day_of_week = request.POST.get('day_of_week')
        entry.start_time = request.POST.get('start_time')
        entry.end_time = request.POST.get('end_time')
        
        entry.subject = get_object_or_404(Subject, pk=subject_id)
        entry.save()
        
        messages.success(request, "Emploi du temps mis à jour.")
        return redirect('timetable_list')
    return render(request, 'academic/timetable_edit.html', {'entry': entry, 'subjects': subjects})

def timetable_delete(request, pk):
    entry = get_object_or_404(TimeTable, pk=pk)
    entry.delete()
    messages.success(request, "Créneau supprimé.")
    return redirect('timetable_list')
