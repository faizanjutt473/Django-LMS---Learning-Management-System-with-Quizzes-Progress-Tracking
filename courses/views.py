from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import CourseForm, ModuleForm, LessonForm
from .models import Course, Category, Lesson, Module


def course_list(request):
    courses = Course.objects.filter(is_published=True).select_related('instructor', 'category')
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    query = request.GET.get('q')
    if query:
        courses = courses.filter(title__icontains=query)

    context = {
        'courses': courses,
        'categories': categories,
        'selected_category': category_slug,
        'query': query or '',
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.select_related('instructor', 'category'),
        slug=slug,
        is_published=True,
    )
    modules = course.modules.prefetch_related('lessons')

    is_enrolled = False
    if request.user.is_authenticated and request.user.is_student:
        is_enrolled = course.enrollments.filter(student=request.user).exists()

    context = {
        'course': course,
        'modules': modules,
        'is_enrolled': is_enrolled,
        'quizzes': course.quizzes.all(),
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def lesson_detail(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    is_teacher_owner = request.user == course.instructor
    is_enrolled = (
        request.user.is_student
        and course.enrollments.filter(student=request.user).exists()
    )

    if not (is_teacher_owner or is_enrolled):
        messages.error(request, 'Lesson dekhne ke liye pehle course me enroll karein.')
        return redirect('courses:course_detail', slug=course.slug)

    is_completed = False
    if is_enrolled:
        is_completed = lesson.progress.filter(
            enrollment__student=request.user,
            is_completed=True,
        ).exists()

    modules = course.modules.prefetch_related('lessons')

    context = {
        'course': course,
        'lesson': lesson,
        'modules': modules,
        'is_enrolled': is_enrolled,
        'is_completed': is_completed,
    }
    return render(request, 'courses/lesson_detail.html', context)


@login_required
def course_create(request):
    if not request.user.is_teacher:
        messages.error(request, 'Sirf teachers course bana sakte hain.')
        return redirect('core:home')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course kamyabi se ban gaya!')
            return redirect('core:teacher_dashboard')
    else:
        form = CourseForm()

    return render(request, 'courses/course_form.html', {'form': form})


@login_required
def module_create(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if request.user != course.instructor:
        messages.error(request, 'Aap sirf apne course me module add kar sakte hain.')
        return redirect('core:home')

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, 'Module kamyabi se add ho gaya!')
            return redirect('core:teacher_dashboard')
    else:
        next_order = course.modules.count() + 1
        form = ModuleForm(initial={'order': next_order})

    return render(request, 'courses/module_form.html', {'form': form, 'course': course})


@login_required
def lesson_create(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course = module.course

    if request.user != course.instructor:
        messages.error(request, 'Aap sirf apne course me lesson add kar sakte hain.')
        return redirect('core:home')

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, 'Lesson kamyabi se add ho gaya!')
            return redirect('courses:course_detail', slug=course.slug)
    else:
        next_order = module.lessons.count() + 1
        form = LessonForm(initial={'order': next_order})

    return render(
        request,
        'courses/lesson_form.html',
        {'form': form, 'module': module, 'course': course},
    )

@login_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if request.user != course.instructor:
        messages.error(request, 'Aap sirf apna course edit kar sakte hain.')
        return redirect('core:home')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course update ho gaya!')
            return redirect('core:teacher_dashboard')
    else:
        form = CourseForm(instance=course)

    return render(
        request,
        'courses/course_form.html',
        {'form': form, 'course': course, 'is_edit': True},
    )


@login_required
@require_POST
def course_delete(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if request.user != course.instructor:
        messages.error(request, 'Aap sirf apna course delete kar sakte hain.')
        return redirect('core:home')

    course.delete()
    messages.success(request, 'Course delete ho gaya.')
    return redirect('core:teacher_dashboard')    