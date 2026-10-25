from django import forms

from .models import Quiz, Question


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description', 'pass_marks')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'marks')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }