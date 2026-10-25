from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from courses.models import Course


def home(request):
    latest_courses = Course.objects.filter(is_published=True).select_related(
        'instructor', 'category'
    )[:6]
    return render(request, 'core/home.html', {'latest_courses': latest_courses})


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        messages.error(request, 'Ye page sirf teachers ke liye hai.')
        return redirect('core:home')

    courses = Course.objects.filter(instructor=request.user)

    return render(request, 'core/teacher_dashboard.html', {'courses': courses})


@login_required
def course_students(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if request.user != course.instructor:
        messages.error(request, 'Aap sirf apne course ke students dekh sakte hain.')
        return redirect('core:home')

    enrollments = course.enrollments.select_related('student')

    return render(
        request,
        'core/course_students.html',
        {'course': course, 'enrollments': enrollments},
    )