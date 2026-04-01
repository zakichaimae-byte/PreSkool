import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from fees.models import Fee
from student.models import Student

# Data from screenshot
fees_data = [
    ('Sara', 'Bennis', 1200, date(2026, 4, 1), 'Paid', 'Frais mensuels'),
    ('Youssef', 'El Amrani', 1200, date(2026, 4, 2), 'Paid', 'Frais mensuels'),
    ('Imane', 'Lahlou', 1200, date(2026, 4, 3), 'Pending', 'Frais mensuels'),
    ('Mehdi', 'Chraibi', 1500, date(2026, 4, 1), 'Paid', 'Frais + transport'),
    ('Salma', 'Tazi', 1300, date(2026, 4, 4), 'Paid', 'Frais mensuels'),
    ('Othmane', 'Kabbaj', 1200, date(2026, 4, 5), 'Pending', 'Frais mensuels'),
    ('Amina', 'Idrissi', 1400, date(2026, 4, 2), 'Paid', 'Frais + activités'),
    ('Karim', 'Berrada', 1200, date(2026, 4, 6), 'Pending', 'Frais mensuels'),
]

print("Populating Fees...")
for first, last, amount, p_date, status, desc in fees_data:
    try:
        student = Student.objects.get(first_name=first, last_name=last)
        Fee.objects.create(
            student=student,
            amount=amount,
            payment_date=p_date,
            status=status,
            description=desc
        )
        print(f"Added fee for {first} {last}")
    except Student.DoesNotExist:
        print(f"Student {first} {last} not found!")

print("Done!")
