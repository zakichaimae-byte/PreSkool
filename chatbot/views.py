from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
import json
import datetime

# Import models for search and stats
from student.models import Student
from teachers.models import Teacher
from departments.models import Department
from subjects.models import Subject
from academic.models import Exam, Holiday, TimeTable, Quiz, Appointment
from fees.models import Fee
from events.models import Event
from library.models import Book, BookBorrowing

def chat_respond(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            msg = data.get('message', '').lower()
            user = request.user
            
            # Détection du rôle
            is_admin = user.is_superuser
            is_teacher = user.groups.filter(name='Enseignant').exists()
            is_student = hasattr(user, 'student_profile')
            
            response = "Je ne suis pas sûr de comprendre votre demande. Je suis là pour vous aider avec la gestion de l'école (étudiants, profs, cours, etc.). Que souhaitez-vous savoir ?"
            
            # --- INTELLIGENT SEARCH (Tous rôles) ---
            if any(k in msg for k in ["cherche", "trouve", "qui est", "où est", "recherche"]):
                query = msg.replace("cherche", "").replace("trouve", "").replace("qui est", "").replace("où est", "").replace("recherche", "").replace("l'étudiant", "").replace("l'etudiant", "").replace("l'enseignant", "").replace("le prof", "").replace("le département", "").replace("le departement", "").replace("la matière", "").replace("la matiere", "").strip()
                
                if query:
                    students = Student.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
                    if students.exists():
                        s = students.first()
                        url = reverse('student_details', args=[s.student_id])
                        response = "L'étudiant(e) <strong>{} {}</strong> a été trouvé(e). <strong>Classe : {}</strong>. <br><br>👉 <a href='{}' class='chat-link'>Afficher sa fiche complète</a>".format(s.first_name, s.last_name, s.student_class, url)
                    else:
                        teachers = Teacher.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
                        if teachers.exists():
                            t = teachers.first()
                            url = reverse('teacher_list')
                            response = "L'enseignant(e) <strong>{} {}</strong> a été trouvé(e). <br><br>👉 <a href='{}' class='chat-link'>Gérer les Enseignants</a>".format(t.first_name, t.last_name, url)
                        else:
                            response = "Désolé, je n'ai trouvé aucun résultat pour '<strong>{}</strong>'.".format(query)

            # --- LOGIQUE ÉTUDIANT ---
            elif is_student:
                # A. Mes Cours
                if any(k in msg for k in ["mes cours", "voir mes cours"]):
                    url = reverse('my_courses_list')
                    response = "Vous pouvez consulter vos cours et contenus pédagogiques dans la section <strong>Mes Cours</strong>. <br><br>📚 <a href='{}' class='chat-link'>Voir mes cours</a>".format(url)
                elif "détail" in msg and "cours" in msg:
                    url = reverse('my_courses_list')
                    response = "Accédez à <strong>Mes Cours</strong> et sélectionnez la matière souhaitée pour voir ses documents détaillés. <br><br>🔍 <a href='{}' class='chat-link'>Accéder à mes cours</a>".format(url)
                
                # B. Emploi du temps
                elif any(k in msg for k in ["emploi du temps", "mon planning", "cours d'aujourd'hui"]):
                    url = reverse('student_timetable_full')
                    response = "Votre emploi du temps affiche toutes les séances, y compris celles d'aujourd'hui et de demain. <br><br>📅 <a href='{}' class='chat-link'>Consulter mon emploi du temps</a>".format(url)
                
                # C. Mes Examens
                elif any(k in msg for k in ["mes examens", "prochain examen"]):
                    url = reverse('student_exams_list')
                    response = "La section <strong>Mes Examens</strong> vous permet de voir toutes les épreuves programmées avec leurs dates et lieux. <br><br>📝 <a href='{}' class='chat-link'>Mes Examens</a>".format(url)
                
                # D. Mes Quiz
                elif any(k in msg for k in ["passer un quiz", "mes quiz", "résultat d'un quiz"]):
                    url = reverse('student_quiz_list')
                    response = "Passer vos évaluations en ligne ou consultez vos résultats dans la section <strong>Mes Quiz</strong>. <br><br>💡 <a href='{}' class='chat-link'>Accéder aux Quiz</a>".format(url)
                
                # E. Cahier de Texte
                elif any(k in msg for k in ["cahier de texte", "voir les devoirs", "cours réalisés"]):
                    url = reverse('student_session_logs')
                    response = "Consultez le <strong>Cahier de Texte</strong> pour voir les séances passées et les devoirs donnés par vos enseignants. <br><br>📖 <a href='{}' class='chat-link'>Voir le Cahier de Texte</a>".format(url)
                
                # Autres
                elif any(k in msg for k in ["rendez-vous", "rdv"]):
                    url = reverse('student_appointments')
                    response = "Prenez ou gérez vos rendez-vous avec vos enseignants ici : <br><br>🤝 <a href='{}' class='chat-link'>Mes Rendez-vous</a>".format(url)
                elif any(k in msg for k in ["performance", "notes"]):
                    url = reverse('student_performance')
                    response = "Suivez vos performances académiques et vos notes globales ici : <br><br>🏆 <a href='{}' class='chat-link'>Mes Performances</a>".format(url)

            # --- LOGIQUE ENSEIGNANT ---
            elif is_teacher:
                # Mes Classes
                if any(k in msg for k in ["mes classes", "voir mes classes"]):
                    url = reverse('my_classes')
                    response = "Vos classes attribuées sont disponibles dans la section <strong>Mes Classes</strong>. <br><br>📋 <a href='{}' class='chat-link'>Voir mes classes</a>".format(url)
                # Notes
                elif any(k in msg for k in ["saisir les notes", "entrer les notes"]):
                    url = reverse('grade_entry')
                    response = "Rendez-vous dans <strong>Saisir les Notes</strong> pour enregistrer les évaluations. <br><br>📝 <a href='{}' class='chat-link'>Saisir les Notes</a>".format(url)
                # Présences
                elif any(k in msg for k in ["présences", "faire l'appel"]):
                    url = reverse('attendance')
                    response = "Gérez les absences et retards dans la section <strong>Présences</strong>. <br><br>✅ <a href='{}' class='chat-link'>Enregistrer les Présences</a>".format(url)
                # Quiz
                elif "quiz" in msg:
                    url = reverse('quiz_list_teacher')
                    response = "Créez et gérez vos quiz pédagogiques ici : <br><br>📂 <a href='{}' class='chat-link'>Mes Quiz</a>".format(url)
                # Cahier de Texte
                elif "cahier de texte" in msg or "remplir le cahier" in msg:
                    url = reverse('log_session')
                    response = "Remplissez le journal de vos séances de cours ici : <br><br>📖 <a href='{}' class='chat-link'>Cahier de Texte</a>".format(url)

            # --- LOGIQUE ADMINISTRATEUR ---
            elif is_admin:
                if any(k in msg for k in ["status", "statut", "bilan", "résumé"]):
                    s_count = Student.objects.count()
                    t_count = Teacher.objects.count()
                    d_count = Department.objects.count()
                    response = "📊 <strong>Bilan :</strong> {} Étudiants, {} Profs, {} Départements.".format(s_count, t_count, d_count)
                elif "ajouter" in msg and any(k in msg for k in ["étudiant", "élève"]):
                    url = reverse('add_student')
                    response = "Ajout d'élève : <a href='{}' class='chat-link'>➕ Inscription</a>".format(url)
                elif "ajouter" in msg and "prof" in msg:
                    url = reverse('teacher_add')
                    response = "Ajout d'enseignant : <a href='{}' class='chat-link'>👨‍🏫 Nouveau Profil</a>".format(url)

            # --- RÉPONSES GÉNÉRIQUES ---
            elif any(k in msg for k in ["bonjour", "salut", "hello"]):
                response = "Bonjour ! Je suis votre assistant PreSkool. Comment puis-je vous aider ?"

            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'response': "Erreur : {}".format(str(e))}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
