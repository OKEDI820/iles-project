from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))
from datetime import date, timedelta
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.users.models import User
from apps.placements.models import InternshipPlacement
from apps.logs.models import WeeklyLog
from apps.evaluations.models import EvaluationCriteria, Evaluation
from apps.evaluations.scoring import calculate_total_score

coordinator, _ = User.objects.get_or_create(email='coordinator@example.com', defaults={'username': 'coordinator', 'role': 'coordinator', 'full_name': 'Course Coordinator'})
coordinator.set_password('Pass1234!')
coordinator.save()

supervisor, _ = User.objects.get_or_create(email='supervisor@example.com', defaults={'username': 'supervisor', 'role': 'supervisor', 'full_name': 'Industry Supervisor'})
supervisor.set_password('Pass1234!')
supervisor.save()

student, _ = User.objects.get_or_create(email='student@example.com', defaults={'username': 'student', 'role': 'student', 'full_name': 'Demo Student'})
student.set_password('Pass1234!')
student.save()

placement, _ = InternshipPlacement.objects.get_or_create(
    student=student,
    defaults={
        'company_name': 'Tech Hub Uganda',
        'company_address': 'Kampala',
        'supervisor_name': 'Industry Supervisor',
        'supervisor_email': 'supervisor@example.com',
        'start_date': date.today() - timedelta(days=21),
        'end_date': date.today() + timedelta(days=35),
    }
)

for name, weight in [('Technical Skills', 50), ('Communication', 20), ('Professionalism', 30)]:
    EvaluationCriteria.objects.get_or_create(name=name, defaults={'weight': weight, 'max_score': 100})

log, _ = WeeklyLog.objects.get_or_create(
    student=student,
    week_number=1,
    defaults={
        'placement': placement,
        'title': 'Week 1 Activities',
        'activities': 'Setup development environment, attended orientation, and fixed initial bugs.',
        'challenges': 'Adjusting to company workflow.',
        'lessons_learned': 'Team communication and Git workflow.',
        'date_from': date.today() - timedelta(days=7),
        'date_to': date.today() - timedelta(days=1),
        'submission_deadline': date.today() + timedelta(days=2),
        'status': 'reviewed',
        'feedback': 'Good start. Add more detail next time.',
    }
)

Evaluation.objects.get_or_create(
    weekly_log=log,
    defaults={
        'evaluator': supervisor,
        'technical_skills': 80,
        'communication': 75,
        'professionalism': 90,
        'total_score': calculate_total_score(80, 75, 90),
        'remarks': 'Solid week one performance.'
    }
)

print('Seed data created.')
print('coordinator@example.com / Pass1234!')
print('supervisor@example.com / Pass1234!')
print('student@example.com / Pass1234!')
