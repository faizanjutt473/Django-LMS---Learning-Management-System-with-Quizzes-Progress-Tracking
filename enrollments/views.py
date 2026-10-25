from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from courses.models import Course, Lesson
from .models import Enrollment, LessonProgress


@login_required
@require_POST
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)

    if not request.user.is_student:
        messages.error(request, 'Sirf students course me enroll ho sakte hain.')
        return redirect('courses:course_detail', slug=course.slug)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
    )

    if created:
        messages.success(request, f'Aap "{course.title}" me enroll ho gaye hain!')
    else:
        messages.info(request, 'Aap pehle se is course me enroll hain.')

    return redirect('courses:course_detail', slug=course.slug)


@login_required
def my_courses(request):
    if not request.user.is_student:
        messages.error(request, 'Ye page sirf students ke liye hai.')
        return redirect('core:home')

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course', 'course__instructor')

    return render(request, 'enrollments/my_courses.html', {'enrollments': enrollments})


@login_required
@require_POST
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course

    if not request.user.is_student:
        messages.error(request, 'Sirf students lesson complete mark kar sakte hain.')
        return redirect('core:home')

    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson,
    )
    if not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        messages.success(request, 'Lesson complete mark ho gaya!')

    return redirect('courses:lesson_detail', slug=course.slug, lesson_id=lesson.id)