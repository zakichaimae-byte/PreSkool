from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student.models import Student
from teacher_space.models import Grade, Attendance
from django.db.models import Avg, Count, Q

@login_required
def dropout_prediction_view(request):
    """
    Vue pour analyser le risque de décrochage scolaire des élèves.
    Logique heuristique simulant un modèle prédictif.
    """
    students = Student.objects.all()
    analysis_results = []

    for student in students:
        # 1. Moyenne des notes
        avg_grade = Grade.objects.filter(student=student).aggregate(Avg('score'))['score__avg'] or 0
        
        # 2. Taux d'absence
        total_attendance = Attendance.objects.filter(student=student).count()
        absences = Attendance.objects.filter(student=student, status='Absent').count()
        absence_rate = (absences / total_attendance * 100) if total_attendance > 0 else 0
        
        # 3. Calcul du score de risque (Heuristique)
        # Base risk: 0%
        risk_score = 0
        
        # Grade impact
        if avg_grade < 8: risk_score += 60
        elif avg_grade < 10: risk_score += 40
        elif avg_grade < 12: risk_score += 20
        
        # Absence impact
        if absence_rate > 30: risk_score += 40
        elif absence_rate > 15: risk_score += 25
        elif absence_rate > 5: risk_score += 10
        
        # Cap risk score at 100
        risk_score = min(risk_score, 100)
        
        # Determine Status
        if risk_score >= 70:
            status = 'Critique'
            color = 'danger'
        elif risk_score >= 40:
            status = 'À surveiller'
            color = 'warning'
        else:
            status = 'Faible'
            color = 'success'
            
        analysis_results.append({
            'student': student,
            'avg_grade': round(float(avg_grade), 2),
            'absence_rate': round(absence_rate, 2),
            'risk_score': risk_score,
            'status': status,
            'color': color
        })
        
    # Sort by risk score descending
    analysis_results.sort(key=lambda x: x['risk_score'], reverse=True)
    
    return render(request, 'analytics/dropout_risk.html', {'results': analysis_results})
