from django.contrib import admin
from .models import Quiz, Question, Choice, Result


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'marks')
    list_filter = ('quiz',)
    search_fields = ('text',)
    inlines = [ChoiceInline]


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'pass_marks', 'created_at')
    list_filter = ('course',)
    search_fields = ('title',)
    inlines = [QuestionInline]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'total_marks', 'passed', 'attempted_at')
    list_filter = ('passed', 'quiz')
    search_fields = ('student__username', 'quiz__title')
