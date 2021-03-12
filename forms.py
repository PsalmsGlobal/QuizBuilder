from django.forms import ModelForm
from .models import Question
from django import forms
from . import models

class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        fields=['course_name',]

class CreateQuestionForm(forms.ModelForm):
    course_name=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Question
        fields = ('course', 'question', 'answer', 'marks', 'option1', 'option2', 'option3', 'option4',)
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

        
        widgets = {
            'course': forms.Textarea(attrs={'class': 'form-control'}),
            'question': forms.Textarea(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
            'marks': forms.TextInput(attrs={'class': 'form-control'}),
            'option1': forms.TextInput(attrs={'class': 'form-control'}),
            'option2': forms.TextInput(attrs={'class': 'form-control'}),
            'option3': forms.TextInput(attrs={'class': 'form-control'}),
            'option4': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
