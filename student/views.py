from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student , Parent

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
                father_name=father_name,
                father_occupation=father_occupation,
                father_mobile=father_mobile,
                father_email=father_email,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                mother_mobile=mother_mobile,
                mother_email=mother_email,
                present_address=present_address,
                permanent_address=permanent_address
            )

            # 2. Création de l'étudiant (maintenant le 'parent' existe !)
            student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                gender=gender,
                date_of_birth=date_of_birth,
                student_class=student_class,
                joining_date=joining_date,
                mobile_number=mobile_number,
                admission_number=admission_number,
                section=section,
                student_image=student_image,
                parent=parent  # On lie l'étudiant au parent qu'on vient de créer
            )

            # Message de succès et redirection
            messages.success(request, 'Student added Successfully')
            return redirect('student_list')
            
    else:
        return render(request, 'students/add.html')

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
        student.religion = request.POST.get('religion')
        student.joining_date = request.POST.get('joining_date')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')

        # Gestion de la nouvelle image (s'il en a uploadé une nouvelle)
        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')

        student.save() # On sauvegarde l'étudiant

        # On met à jour les infos du parent
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')

        parent.save() # On sauvegarde le parent

        # Message de succès et redirection vers la liste
        messages.success(request, 'Student updated successfully!')
        return redirect('student_list')

    # 3. Si on charge juste la page (méthode GET), on envoie les données pour pré-remplir
    # Remarque comment on envoie 'student' ET 'parent' à ton fichier HTML !
    return render(request, 'students/edit.html', {'student': student, 'parent': parent})

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