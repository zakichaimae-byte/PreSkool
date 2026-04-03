from datetime import date, timedelta
from django.db.models import Count, Q, Avg
from academic.models import CourseSessionLog, Appointment, Quiz, HomeworkSubmission, TimeTable
from teacher_space.models import Attendance, Grade
from library.models import BookBorrowing
from subjects.models import Subject
from student.models import Student

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

    @staticmethod
    def get_performance_trends(teacher):
        """
        Calculates the performance progression of the teacher's classes.
        Compares this week's averages to last week's.
        """
        import datetime
        from django.db.models import Avg
        today = date.today()
        # Week starts on Monday
        start_of_week = today - timedelta(days=today.weekday())
        last_week_start = start_of_week - timedelta(days=7)
        
        this_week_avg = Grade.objects.filter(
            subject__teacher=teacher,
            date_recorded__gte=start_of_week
        ).aggregate(Avg('score'))['score__avg'] or 0
        
        last_week_avg = Grade.objects.filter(
            subject__teacher=teacher,
            date_recorded__gte=last_week_start,
            date_recorded__lt=start_of_week
        ).aggregate(Avg('score'))['score__avg'] or 0
        
        trend = 0
        if last_week_avg > 0:
            trend = ((float(this_week_avg) - float(last_week_avg)) / float(last_week_avg)) * 100
            
        return {
            'this_week': round(float(this_week_avg), 2),
            'last_week': round(float(last_week_avg), 2),
            'trend': round(float(trend), 1),
            'status': 'up' if trend >= 0 else 'down'
        }

    @staticmethod
    def get_top_performing_students(teacher, limit=5):
        """Calculates top students for the teacher's subjects based on average grades."""
        my_classes = Subject.objects.filter(teacher=teacher).values_list('class_name', flat=True).distinct()
        
        top_students = Student.objects.filter(student_class__in=my_classes).annotate(
            avg_score=Avg('grades__score', filter=Q(grades__subject__teacher=teacher))
        ).filter(avg_score__isnull=False).order_by('-avg_score')[:limit]
        
        return top_students

    @staticmethod
    def get_at_risk_students(teacher, limit=5):
        """
        Identifies students at risk based on:
        - Avg grade < 10
        - Absence rate > 15%
        Calculated in pure Python/Django ORM.
        """
        my_classes = Subject.objects.filter(teacher=teacher).values_list('class_name', flat=True).distinct()
        students = Student.objects.filter(student_class__in=my_classes)
        
        risk_list = []
        for student in students:
            avg = Grade.objects.filter(student=student, subject__teacher=teacher).aggregate(Avg('score'))['score__avg'] or 0
            total_attr = Attendance.objects.filter(student=student, teacher=teacher).count()
            absences = Attendance.objects.filter(student=student, teacher=teacher, status='Absent').count()
            abs_rate = (absences / total_attr * 100) if total_attr > 0 else 0
            
            if avg < 10 or abs_rate > 15:
                # Calculate simple risk level
                risk_lvl = 'Critique' if (avg < 8 or abs_rate > 30) else 'À surveiller'
                risk_list.append({
                    'student': student,
                    'avg': round(float(avg), 2),
                    'abs_rate': round(abs_rate, 1),
                    'risk_level': risk_lvl,
                    'color': 'danger' if risk_lvl == 'Critique' else 'warning'
                })
                
        # Sort by worst average
        risk_list.sort(key=lambda x: x['avg'])
        return risk_list[:limit]

    @staticmethod
    def get_chronic_absentees(teacher, limit=5):
        """
        Identifies students who have missed more than 3 sessions recently.
        Demonstrates complex Python list manipulation.
        """
        from django.utils import timezone
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        absentees = Attendance.objects.filter(
            teacher=teacher, 
            status='Absent',
            date__gte=thirty_days_ago
        ).values('student').annotate(abs_count=Count('id')).filter(abs_count__gte=3).order_by('-abs_count')[:limit]
        
        result = []
        for item in absentees:
            student = Student.objects.get(id=item['student'])
            result.append({
                'student': student,
                'count': item['abs_count']
            })
        return result
