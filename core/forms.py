from django import forms
from core.models import Test, Question, Category, Instruction
from ckeditor.widgets import CKEditorWidget
from .models import Candidate
import re

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ['test_name','duration',]

class InstructionForm(forms.ModelForm):

    class Meta:
        model = Instruction
        fields = ['instruction']

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category']

class QuestionForm(forms.Form):
    question_text = forms.CharField(widget=CKEditorWidget())
    category = forms.CharField(max_length=500,required=True)
    choice = forms.CharField(widget=CKEditorWidget())
    correct_choice = forms.CharField(widget=CKEditorWidget())
    class Meta:
        fields = ['category', 'question_text','choice', 'correct_choice']


class CandidateRegistration(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = '__all__'

