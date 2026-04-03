from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='exams')
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    coefficient = models.IntegerField(default=1)
    duration = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} - {self.subject.name}"

class TimeTable(models.Model):
    class_name = models.CharField(max_length=200)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.CharField(max_length=20, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_name} - {self.subject.name} ({self.day_of_week})"

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='quizzes')
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class StudentQuizAttempt(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.quiz.title} ({self.score})"

class CourseSessionLog(models.Model):
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='session_logs', null=True, blank=True)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='session_logs')
    class_name = models.CharField(max_length=100)
    date = models.DateField()
    summary = models.TextField()
    homework = models.TextField(blank=True)
    attachment = models.FileField(upload_to='course_materials/', blank=True, null=True)

    def __str__(self):
        return f"{self.subject} - {self.class_name} ({self.date})"

class HomeworkSubmission(models.Model):
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='homework_submissions')
    session_log = models.ForeignKey(CourseSessionLog, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='homework_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    teacher_feedback = models.TextField(blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'En attente'), ('Graded', 'Corrigé')])

    def __str__(self):
        return f"{self.student} - {self.session_log.subject} ({self.submitted_at.date()})"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'En attente'),
        ('Approved', 'Confirmé'),
        ('Completed', 'Terminé'),
        ('Cancelled', 'Annulé'),
    ]
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='appointments')
    parent = models.ForeignKey('student.Parent', on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time_slot = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RDV: {self.teacher} - {self.parent} le {self.date}"

class ClassLevel(models.Model):
    name = models.CharField(max_length=200, help_text="Nom exact pour la base de données (ex: 'Tronc Commun Sciences 1')")
    level = models.CharField(max_length=50, blank=True, null=True, help_text="Niveau général (ex: 'Tronc Commun')")

    def __str__(self):
        return self.name
