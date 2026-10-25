from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from courses.models import Course
from enrollments.models import Enrollment
from .forms import QuizForm, QuestionForm
from .models import Quiz, Choice, Result


@login_required
def quiz_create(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if request.user != course.instructor:
        messages.error(request, 'Aap sirf apne course ka quiz bana sakte hain.')
        return redirect('core:home')

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.success(request, 'Quiz kamyabi se ban gaya! Ab sawalat add karein.')
            return redirect('quizzes:question_create', quiz_id=quiz.id)
    else:
        form = QuizForm()

    return render(request, 'quizzes/quiz_form.html', {'form': form, 'course': course})


@login_required
def question_create(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.user != quiz.course.instructor:
        messages.error(request, 'Aap sirf apne quiz me sawal add kar sakte hain.')
        return redirect('core:home')

    error = None

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        choice_texts = [request.POST.get(f'choice_{i}', '').strip() for i in range(1, 5)]
        correct = request.POST.get('correct')

        filled = [t for t in choice_texts if t]

        if not form.is_valid():
            pass
        elif len(filled) < 2:
            error = 'Kam az kam 2 options likhna zaroori hai.'
        elif not correct or not choice_texts[int(correct) - 1]:
            error = 'Sahi jawab select karein (wo option khali nahi hona chahiye).'
        else:
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            for i, text in enumerate(choice_texts, start=1):
                if text:
                    Choice.objects.create(
                        question=question,
                        text=text,
                        is_correct=(str(i) == correct),
                    )
            messages.success(request, 'Sawal kamyabi se add ho gaya!')
            return redirect('quizzes:question_create', quiz_id=quiz.id)
    else:
        form = QuestionForm()

    questions = quiz.questions.prefetch_related('choices')

    context = {
        'quiz': quiz,
        'form': form,
        'questions': questions,
        'error': error,
    }
    return render(request, 'quizzes/question_form.html', context)


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    course = quiz.course

    if not request.user.is_student:
        messages.error(request, 'Sirf students quiz de sakte hain.')
        return redirect('core:home')

    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'Quiz dene ke liye pehle course me enroll karein.')
        return redirect('courses:course_detail', slug=course.slug)

    questions = quiz.questions.prefetch_related('choices')

    if request.method == 'POST':
        score = 0
        total = 0
        for question in questions:
            total += question.marks
            selected = request.POST.get(f'question_{question.id}')
            if selected and question.choices.filter(id=selected, is_correct=True).exists():
                score += question.marks

        if total > 0:
            percentage = (score / total) * 100
        else:
            percentage = 0

        result = Result.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            total_marks=total,
            passed=percentage >= quiz.pass_marks,
        )
        return redirect('quizzes:quiz_result', result_id=result.id)

    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'questions': questions})


@login_required
def quiz_result(request, result_id):
    result = get_object_or_404(Result, id=result_id, student=request.user)
    return render(request, 'quizzes/quiz_result.html', {'result': result})

@login_required
def my_results(request):
    if not request.user.is_student:
        messages.error(request, 'Ye page sirf students ke liye hai.')
        return redirect('core:home')

    results = Result.objects.filter(student=request.user).select_related('quiz', 'quiz__course')

    return render(request, 'quizzes/my_results.html', {'results': results})