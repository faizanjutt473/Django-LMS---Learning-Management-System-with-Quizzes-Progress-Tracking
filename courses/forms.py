from django import forms

from .models import Course, Module, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            'title',
            'description',
            'thumbnail',
            'category',
            'level',
            'price',
            'is_published',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('title', 'order')


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content', 'video_url', 'attachment', 'order')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }