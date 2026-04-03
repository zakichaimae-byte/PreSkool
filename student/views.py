from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Student , Parent
from teacher_space.models import Grade, Attendance
from academic.models import CourseSessionLog, Quiz, Question, Choice, StudentQuizAttempt, HomeworkSubmission, Appointment
from academic.forms import HomeworkSubmissionForm, AppointmentForm
from academic.models import ClassLevel
from home_auth.models import Notification

@login_required
def book_appointment_view(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Accès réservé aux parents/étudiants.")
        return redirect('dashboard')
        
    parent = request.user.student_profile.parent
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.parent = parent
            appointment.save()
            
            # --- Notification for Teacher ---
            Notification.objects.create(
                user=appointment.teacher.user,
                title="Nouveau Rendez-vous",
                message=f"Le parent de {request.user.student_profile.first_name} a demandé un RDV le {appointment.date}.",
                category='contact',
                link='/teacher/appointments/'
            )
            
            messages.success(request, "Demande de rendez-vous envoyée avec succès !")
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    
    return render(request, 'students/book_appointment.html', {'form': form})

@login_required
def student_appointments_view(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Accès réservé aux parents/étudiants.")
        return redirect('dashboard')
        
    parent = request.user.student_profile.parent
    appointments = Appointment.objects.filter(parent=parent).order_by('-date', 'time_slot')
    return render(request, 'students/appointments_list.html', {'appointments': appointments})

@login_required
def student_performance_view(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard')
        
    student = request.user.student_profile
    
    # 1. Moyennes par Matière
    grades_by_subject = Grade.objects.filter(student=student).values('subject__name').annotate(average=Avg('score'))
    
    # 2. Taux d'Assiduité
    total_attendance = Attendance.objects.filter(student=student).count()
    present_count = Attendance.objects.filter(student=student, status='Present').count()
    attendance_rate = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    # 3. Historique des Quiz
    quiz_history = StudentQuizAttempt.objects.filter(student=student).order_by('-completed_at')[:10]
    
    # 4. Devoirs soumis / total devoirs
    total_homeworks = CourseSessionLog.objects.exclude(homework='').count() # Estimation simple
    submitted_homeworks = HomeworkSubmission.objects.filter(student=student).count()
    homework_rate = (submitted_homeworks / total_homeworks * 100) if total_homeworks > 0 else 0
    
    context = {
        'student': student,
        'grades_by_subject': grades_by_subject,
        'attendance_rate': attendance_rate,
        'present_count': present_count,
        'absent_count': total_attendance - present_count,
        'quiz_history': quiz_history,
        'homework_rate': homework_rate,
    }
    
    return render(request, 'students/performance.html', context)

def add_student(request):
    if request.method == 'POST':
        # --- TOUT CE BLOC EST MAINTENANT CORRECTEMENT INDENTÉ ---
            
            # Récupérer les données de l'étudiant
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            student_id = request.POST.get('student_id')
            gender = request.POST.get('gender')
            date_of_birth = request.POST.get('date_of_birth')
            student_class = request.POST.get('student_class')
            joining_date = request.POST.get('joining_date')
            mobile_number = request.POST.get('mobile_number')
            admission_number = request.POST.get('admission_number')
            section = request.POST.get('section')
            # On utilise request.FILES pour les images/fichiers
            student_image = request.FILES.get('student_image') 

            # Récupérer les données du parent
            father_name = request.POST.get('father_name')
            father_occupation = request.POST.get('father_occupation')
            father_mobile = request.POST.get('father_mobile')
            father_email = request.POST.get('father_email')
            mother_name = request.POST.get('mother_name')
            mother_occupation = request.POST.get('mother_occupation')
            mother_mobile = request.POST.get('mother_mobile')
            mother_email = request.POST.get('mother_email')
            present_address = request.POST.get('present_address')
            permanent_address = request.POST.get('permanent_address')

            # 1. Création du parent en premier
            parent = Parent.objects.create(
                father_name=father_name or '',
                father_occupation=father_occupation or '',
                father_mobile=father_mobile or '',
                father_email=father_email or '',
                mother_name=mother_name or '',
                mother_occupation=mother_occupation or '',
                mother_mobile=mother_mobile or '',
                mother_email=mother_email or '',
                present_address=present_address or '',
                permanent_address=permanent_address or ''
            )

            # 2. Création de l'étudiant (maintenant le 'parent' existe !)
            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                gender=gender,
                date_of_birth=date_of_birth,
                student_class=student_class,
                joining_date=joining_date or None, # Will trigger error if None, but we need to handle it
                mobile_number=mobile_number or '',
                admission_number=admission_number or '',
                section=section or '',
                student_image=student_image,
                parent=parent  # On lie l'étudiant au parent qu'on vient de créer
            )

            # Message de succès et redirection
            messages.success(request, 'Student added Successfully')
            return redirect('student_list')
            
    else:
        class_levels = ClassLevel.objects.all().order_by('level', 'name')
        return render(request, 'students/add.html', {'class_levels': class_levels})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

def student_details(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'students/list.html', {'student': student}) # Placeholder for details

def edit_student(request, student_id):
    # 1. On récupère l'étudiant et son parent
    student = get_object_or_404(Student, student_id=student_id)
    parent = student.parent # On récupère le parent lié à cet étudiant

    # 2. Si l'utilisateur a cliqué sur "Submit" (méthode POST)
    if request.method == 'POST':
        # On met à jour les infos de l'étudiant
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        # Attention: il vaut mieux éviter de modifier l'ID, mais on le laisse si c'est nécessaire.
        student.student_id = request.POST.get('student_id')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.student_class = request.POST.get('student_class')
        
        # On ne met à jour la date d'adhésion que si elle est fournie
        joining_date = request.POST.get('joining_date')
        if joining_date:
            student.joining_date = joining_date
            
        student.mobile_number = request.POST.get('mobile_number') or ''
        student.admission_number = request.POST.get('admission_number') or ''
        student.section = request.POST.get('section') or ''

        # Gestion de la nouvelle image (s'il en a uploadé une nouvelle)
        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')

        student.save() # On sauvegarde l'étudiant

        # On met à jour les infos du parent (uniquement si présentes dans POST)
        if request.POST.get('father_name'): parent.father_name = request.POST.get('father_name')
        if request.POST.get('father_occupation'): parent.father_occupation = request.POST.get('father_occupation')
        if request.POST.get('father_mobile'): parent.father_mobile = request.POST.get('father_mobile')
        if request.POST.get('father_email'): parent.father_email = request.POST.get('father_email')
        
        if request.POST.get('mother_name'): parent.mother_name = request.POST.get('mother_name')
        if request.POST.get('mother_occupation'): parent.mother_occupation = request.POST.get('mother_occupation')
        if request.POST.get('mother_mobile'): parent.mother_mobile = request.POST.get('mother_mobile')
        if request.POST.get('mother_email'): parent.mother_email = request.POST.get('mother_email')
        
        if request.POST.get('present_address'): parent.present_address = request.POST.get('present_address')
        if request.POST.get('permanent_address'): parent.permanent_address = request.POST.get('permanent_address')

        parent.save() # On sauvegarde le parent

        # Message de succès et redirection vers la liste
        messages.success(request, 'Student updated successfully!')
        return redirect('student_list')

    # 3. Si on charge juste la page (méthode GET), on envoie les données pour pré-remplir
    # Remarque comment on envoie 'student' ET 'parent' à ton fichier HTML !
    class_levels = ClassLevel.objects.all().order_by('level', 'name')
    return render(request, 'students/edit.html', {'student': student, 'parent': parent, 'class_levels': class_levels})

def delete_student(request, student_id):
    # 1. On cherche l'étudiant avec cet ID spécifique
    student = get_object_or_404(Student, student_id=student_id)
    
    # (Optionnel mais recommandé) Si tu veux aussi supprimer le Parent lié à l'étudiant :
    if student.parent:
        student.parent.delete()
        
    # 2. On supprime l'étudiant de la base de données
    student.delete()
    
    # 3. On affiche un petit message de succès
    messages.success(request, 'Student deleted successfully')
    
    # 4. On redirige vers la liste des étudiants
    return redirect('student_list')

def student_session_logs_view(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard')
    
    student = request.user.student_profile
    # Filter logs by the student's class
    logs = CourseSessionLog.objects.filter(class_name=student.student_class).order_by('-date')
    return render(request, 'students/session_logs.html', {'logs': logs})

def student_quiz_list_view(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard')
    
    student = request.user.student_profile
    quizzes = Quiz.objects.all()
    
    # Enrichir les quiz avec l'état de tentative de l'étudiant
    for quiz in quizzes:
        attempt = StudentQuizAttempt.objects.filter(student=student, quiz=quiz).first()
        quiz.my_attempt = attempt
        
    return render(request, 'students/quiz_list.html', {'quizzes': quizzes})

def take_quiz_view(request, quiz_id):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard')
    
    student = request.user.student_profile
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Vérifier si déjà passé
    previous_attempt = StudentQuizAttempt.objects.filter(student=student, quiz=quiz).first()
    
    if request.method == 'POST':
        if previous_attempt:
             messages.info(request, f"Vous avez déjà passé ce quiz. Votre score est de {previous_attempt.score:.2f}/20")
             return redirect('student_quiz_list')

        score = 0
        total_questions = quiz.questions.count()
        questions_with_results = []
        for question in quiz.questions.all():
            selected_choice_id = request.POST.get(f'question_{question.id}')
            correct_choice = question.choices.filter(is_correct=True).first()
            
            is_right = False
            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                if selected_choice.is_correct:
                    score += 1
                    is_right = True
            
            # Attacher les résultats directement à l'objet question pour le template
            question.selected_id = int(selected_choice_id) if selected_choice_id else None
            question.is_right = is_right
            questions_with_results.append(question)
        
        final_score = (score / total_questions) * 20 if total_questions > 0 else 0
        attempt = StudentQuizAttempt.objects.create(student=student, quiz=quiz, score=final_score)
        
        context = {
            'quiz': quiz,
            'questions': questions_with_results, # Passer les questions annotées
            'final_score': final_score,
            'is_result': True
        }
        messages.success(request, f"Quiz terminé ! Score : {final_score:.2f}/20")
        return render(request, 'students/take_quiz.html', context)
    
    # Si déjà passé et qu'on accède via GET, on pourrait aussi afficher les résultats ou bloquer
    if previous_attempt:
        # On ne peut pas "re-calculer" les résultats exacts car on ne stocke pas les choix individuels dans la DB (V2)
        # Mais pour cette session, on dira juste qu'il est terminé.
        # Si on voulait vraiment voir les résultats, il faudrait un modèle StudentAnswer.
        # Pour l'instant, disons qu'on affiche la note.
        messages.info(request, f"Ce quiz est déjà terminé. Note : {previous_attempt.score:.2f}/20")
        return redirect('student_quiz_list')

    return render(request, 'students/take_quiz.html', {'quiz': quiz})

@login_required
def submit_homework_view(request, log_id):
    session_log = get_object_or_404(CourseSessionLog, id=log_id)
    # Check if student profile exists
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('dashboard')
        
    student = request.user.student_profile
    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = student
            submission.session_log = session_log
            submission.save()
            messages.success(request, "Travail soumis avec succès !")
            return redirect('student_session_logs')
    else:
        form = HomeworkSubmissionForm()
    
    return render(request, 'students/submit_homework.html', {
        'form': form,
        'session_log': session_log
    })