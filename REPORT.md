---
title: "Django LMS - Project Report"
subtitle: "Learning Management System with Quizzes and Progress Tracking"
---

# 1. Abstract

This report describes the design and development of a web-based Learning Management System (LMS) built with Django. The system allows teachers to publish courses made of modules and lessons, and allows students to enroll, learn, track their progress, and take quizzes that are graded automatically. Access is controlled by user roles, so each user only sees the features that belong to them.

# 2. Objectives

- Provide a simple platform where teachers can create and manage online courses.
- Let students enroll in courses and learn at their own pace.
- Track each student's progress lesson by lesson.
- Assess learning through multiple-choice quizzes with instant results.
- Keep the system secure with role-based access control.

# 3. Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Framework | Django 5.2 |
| Frontend | Django Templates, Bootstrap 5 |
| Forms | django-crispy-forms, crispy-bootstrap5 |
| Database | SQLite (PostgreSQL ready) |
| Image handling | Pillow |
| Configuration | python-decouple (.env file) |

# 4. System Architecture

The project follows Django's MVT (Model, View, Template) pattern and is divided into five apps, each with a single responsibility.

![System architecture](docs/architecture.png)

| App | Responsibility |
|---|---|
| accounts | Custom user model, registration, login, logout, profile |
| courses | Categories, courses, modules, lessons, teacher course management |
| enrollments | Enrollment, lesson progress, My Courses page |
| quizzes | Quizzes, questions, choices, results, automatic grading |
| core | Home page, teacher dashboard, student list per course |

# 5. Database Design

The database contains 11 tables. A custom `User` model extends Django's `AbstractUser` with a `role` field (student or teacher), a bio, and a profile picture.

![Database schema](docs/database_schema.png)

Key relationships:

- A course belongs to one teacher and one category.
- A course has many modules, and a module has many lessons.
- An enrollment links one student to one course; a student can enroll in a course only once.
- Lesson progress records which lessons an enrollment has completed.
- A quiz belongs to a course and has many questions; each question has several choices, one of them correct.
- A result stores a student's score and pass/fail status for one quiz attempt.

# 6. Features

## 6.1 Student features

- Registration, login, logout, and profile editing
- Course search and category filter
- Enrollment and lesson viewing (text, video link, attachments)
- Mark lessons complete; progress percentage shown on My Courses
- Take quizzes and see score with pass/fail result
- My Results page with all attempts

## 6.2 Teacher features

- Dashboard listing courses, publish status, and enrolled student count
- Create, edit, and delete courses
- Add modules and lessons
- Create quizzes and add multiple-choice questions
- View enrolled students with their progress

## 6.3 Administration

All models are registered in the Django admin panel, with filters, search, and inline editing for modules, lessons, questions, and choices.

# 7. Security and Access Control

- Passwords are hashed by Django's authentication system.
- All forms use CSRF protection.
- Pages are protected with `login_required` and role checks.
- Only enrolled students (or the course teacher) can open lessons.
- Only enrolled students can take quizzes.
- Teachers can edit only their own courses, modules, lessons, and quizzes.
- Delete and logout actions accept POST requests only.
- The secret key and debug flag are stored in a `.env` file that is excluded from version control.

# 8. Testing

The system was tested manually using the following checklist:

| Area | Checks |
|---|---|
| Public visitor | Home page, course list, course detail, login prompt for enrolling |
| Student | Register, enroll, complete lessons, progress bar, quiz, results, profile |
| Teacher | Create course, module, lesson, quiz with questions; students list; edit and delete |
| Access control | Student blocked from teacher pages; lessons blocked without enrollment |
| Admin | All models visible and editable |
| Error pages | Custom 404 and 500 pages |

# 9. Limitations

- Quizzes can be attempted any number of times.
- Only multiple-choice questions with a single correct answer are supported.
- Courses are free to enroll in; there is no payment system.
- No email notifications.
- Automated tests are not yet written.

# 10. Future Work

- Quiz attempt limits and time limits
- Course reviews and ratings
- Email notifications
- Payment gateway integration
- REST API with Django REST Framework
- Automated unit tests
- Deployment on a cloud platform with PostgreSQL

# 11. Conclusion

The project delivers a working LMS covering the full learning cycle: course creation, enrollment, learning, progress tracking, and assessment. Its modular structure makes it easy to extend with new features such as payments, ratings, and APIs.
