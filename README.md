# Django LMS - Learning Management System

A full-featured Learning Management System built with **Django** and **Bootstrap 5**. It supports role-based access for students and teachers, course and lesson management, enrollment, progress tracking, and quizzes with automatic grading.

![Preview](docs/preview.png)

## Features

**Students**
- Register, log in, and manage their profile (bio, picture)
- Browse and search courses, filter by category
- Enroll in courses and view lessons (video link, text, attachments)
- Mark lessons as complete and track progress with a progress bar
- Take quizzes with instant score and pass/fail result
- View all quiz results in one place

**Teachers**
- Dashboard with all their courses, status, and student count
- Create, edit, and delete courses (thumbnail, category, level, price, publish/draft)
- Add modules and lessons from the website
- Create quizzes with multiple-choice questions
- View enrolled students and their progress

**General**
- Role-based access control (students cannot open teacher pages and vice versa)
- Only enrolled students can open lessons and quizzes
- Django admin panel for all models
- Custom 404 and 500 pages
- Secrets and settings kept in a `.env` file

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 5.2 |
| Frontend | Django Templates, Bootstrap 5 |
| Forms | django-crispy-forms, crispy-bootstrap5 |
| Database | SQLite (development), PostgreSQL ready |
| Config | python-decouple (`.env`) |
| Media | Pillow (image uploads) |

## Architecture

![Architecture](docs/architecture.png)

## Database Schema

![Database Schema](docs/database_schema.png)

## Project Structure

```
LMS/
├── manage.py
├── requirements.txt
├── .env                # not uploaded to GitHub
├── config/             # project settings and main urls
├── accounts/           # custom User, register, login, profile
├── courses/            # Category, Course, Module, Lesson
├── enrollments/        # Enrollment, LessonProgress, My Courses
├── quizzes/            # Quiz, Question, Choice, Result
├── core/               # home page, teacher dashboard
├── templates/          # all HTML templates
├── static/
└── media/              # uploaded files
```

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Create a `.env` file** in the project root (next to `manage.py`)

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Generate a key with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

**5. Run migrations and create an admin user**

```bash
python manage.py makemigrations accounts
python manage.py makemigrations courses enrollments quizzes
python manage.py migrate
python manage.py createsuperuser
```

**6. Start the server**

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. The admin panel is at `/admin/`.

## Main URLs

| URL | Description |
|---|---|
| `/` | Home page |
| `/courses/` | Course list and search |
| `/courses/<slug>/` | Course detail |
| `/accounts/register/` | Register (student or teacher) |
| `/enrollments/my-courses/` | Student's enrolled courses |
| `/quizzes/my-results/` | Student's quiz results |
| `/teacher/dashboard/` | Teacher dashboard |
| `/admin/` | Admin panel |

## Future Improvements

- Limit the number of quiz attempts
- Course reviews and ratings
- Email notifications
- Payment integration for paid courses
- REST API with Django REST Framework

## License

This project is for learning and portfolio purposes.
