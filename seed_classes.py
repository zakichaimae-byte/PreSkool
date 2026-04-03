import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from academic.models import ClassLevel

classes = [
    ('Tronc Commun Lettres 1', 'Tronc Commun'),
    ('Tronc Commun Sciences 1', 'Tronc Commun'),
    ('Tronc Commun Sciences 2', 'Tronc Commun'),
    ('1ere Année Bac Lettres', '1 Bac'),
    ('1ere Année Bac Sciences Expérimentales', '1 Bac'),
    ('1ere Année Bac Sciences Maths', '1 Bac'),
    ('2eme Année Bac Lettres', '2 Bac'),
    ('2eme Année Bac Sciences de la Vie et de la Terre (SVT)', '2 Bac'),
    ('2eme Année Bac Sciences Physiques (PC)', '2 Bac'),
    ('2eme Année Bac Sciences Maths (SM)', '2 Bac'),
]

for name, level in classes:
    ClassLevel.objects.get_or_create(name=name, level=level)

print(f"{ClassLevel.objects.count()} classes sont maintenant dans la base de données.")
