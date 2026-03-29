from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Grade, Attendance
from academic.models import TimeTable, Exam
from students.models import Student
from subjects.models import Subject
from teachers.models import Teacher
from django.contrib import messages

@login_required
def my_classes_view(request):
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "Votre compte n'est pas lié à un profil enseignant.")
        return redirect('dashboard')
        
    timetables = TimeTable.objects.filter(teacher=teacher).order_by('day_of_week', 'start_time')
    return render(request, 'teacher_space/my_classes.html', {'timetables': timetables})

@login_required
def grade_entry_view(request):
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "Votre compte n'est pas lié à un profil enseignant.")
        return redirect('dashboard')
        
    students = Student.objects.all()
    subjects = Subject.objects.all()
    exams = Exam.objects.all()
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        exam_id = request.POST.get('exam')
        score = request.POST.get('score')
        comments = request.POST.get('comments')
        
        student = get_object_or_404(Student, pk=student_id)
        subject = get_object_or_404(Subject, pk=subject_id)
        # Optional exam
        exam = get_object_or_404(Exam, pk=exam_id) if exam_id else None
        
        Grade.objects.create(
            student=student,
            subject=subject,
            exam=exam,
            teacher=teacher,
            score=score,
            comments=comments
        )
        messages.success(request, "Note enregistrée avec succès.")
        return redirect('grade_entry')
        
    return render(request, 'teacher_space/grade_entry.html', {
        'students': students,
        'subjects': subjects,
        'exams': exams
    })

@login_required
def attendance_view(request):
    try:
        teacher = request.user.teacher_profile
    except Teacher.DoesNotExist:
        messages.error(request, "Votre compte n'est pas lié à un profil enseignant.")
        return redirect('dashboard')
        
    students = Student.objects.all()
    
    if request.method == 'POST':
        date = request.POST.get('date')
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'status': status, 'teacher': teacher}
                )
        messages.success(request, "Présences enregistrées.")
        return redirect('attendance')
        
    return render(request, 'teacher_space/attendance.html', {'students': students})
