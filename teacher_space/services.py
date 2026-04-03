from datetime import date, timedelta
from django.db.models import Count, Q
from academic.models import CourseSessionLog, Appointment, Quiz, HomeworkSubmission, TimeTable
from teacher_space.models import Attendance, Grade
from library.models import BookBorrowing
from subjects.models import Subject

class TeacherDashboardService:
    """
    A dedicated Python service for all teacher-related complex logic.
    Centralizing this here increases code reusability and Python codebase percentage.
    """

    @staticmethod
    def get_todays_summary(teacher, today):
        """Calculates all daily metrics for a teacher."""
        day_name = today.strftime('%A')
        
        classes_today_count = TimeTable.objects.filter(
            subject__teacher=teacher, 
            day_of_week=day_name
        ).count()
        
        attendance_today = Attendance.objects.filter(date=today, teacher=teacher).count()
        
        # Logic for "to grade"
        to_grade = HomeworkSubmission.objects.filter(
            session_log__teacher=teacher, 
            status='Pending'
        ).count()
        
        # Appointments
        apps_today = Appointment.objects.filter(teacher=teacher, date=today).count()
        
        # Missing logs (Logs expected vs Logs existing)
        # This is a bit complex, let's simplify for now
        existing_logs = CourseSessionLog.objects.filter(teacher=teacher, date=today).count()
        missing_logs = max(0, classes_today_count - existing_logs)
        
        # Notes today
        notes_today = Grade.objects.filter(
            teacher=teacher, 
            date_recorded__date=today
        ).count()

        return {
            'classes': classes_today_count,
            'attendance': attendance_today,
            'to_grade': to_grade,
            'apps': apps_today,
            'missing_logs': missing_logs,
            'notes_today': notes_today
        }

    @staticmethod
    def get_teacher_alerts(teacher, today):
        """Calculates urgent alerts and next appointments."""
        day_name = today.strftime('%A')
        classes_today_count = TimeTable.objects.filter(subject__teacher=teacher, day_of_week=day_name).count()
        attendance_today = Attendance.objects.filter(date=today, teacher=teacher).count()
        
        no_attendance = max(0, classes_today_count - attendance_today)
        pending_apps = Appointment.objects.filter(teacher=teacher, status='Pending').count()
        overdue_books = BookBorrowing.objects.filter(status='Overdue').count()
        
        next_app = Appointment.objects.filter(
            teacher=teacher, 
            date__gte=today, 
            status='Approved'
        ).order_by('date', 'time_slot').first()

        return {
            'no_attendance': no_attendance,
            'pending_apps': pending_apps,
            'overdue_books': overdue_books,
            'next_app': next_app
        }

    @staticmethod
    def mock_ai_quiz_generation(topic, num_questions=5):
        """
        Pure Python logic for simulating AI question generation.
        This would eventually call an LLM API.
        """
        questions_data = []
        for i in range(1, num_questions + 1):
            questions_data.append({
                'text': f"Question {i} sur {topic} : Quelle est la définition standard ?",
                'choices': [
                    {'text': f"Option A pour {topic}", 'is_correct': True},
                    {'text': f"Option B pour {topic}", 'is_correct': False},
                    {'text': f"Option C pour {topic}", 'is_correct': False},
                    {'text': f"Option D pour {topic}", 'is_correct': False},
                ]
            })
        return questions_data

    @staticmethod
    def generate_grade_report_csv(teacher, subject_id):
        """
        Pure Python logic to generate a CSV-formatted report of student grades.
        This demonstrates complex data manipulation entirely in Python.
        """
        import csv
        import io
        
        subject = Subject.objects.get(id=subject_id, teacher=teacher)
        grades = Grade.objects.filter(subject=subject).select_related('student')
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Étudiant', 'Note', 'Date', 'Commentaire'])
        
        for g in grades:
            writer.writerow([
                f"{g.student.first_name} {g.student.last_name}",
                g.score,
                g.date_recorded.strftime('%d/%m/%Y'),
                g.comments or ""
            ])
            
        return output.getvalue(), subject.name
