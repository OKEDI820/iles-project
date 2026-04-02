# Internship Logging & Evaluation System Backend

## Quick start
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations users placements logs evaluations
python manage.py migrate
python scripts/seed_data.py
python manage.py runserver
```

Login API: `POST /api/auth/login/`

Demo accounts:
- coordinator@example.com / Pass1234!
- supervisor@example.com / Pass1234!
- student@example.com / Pass1234!
