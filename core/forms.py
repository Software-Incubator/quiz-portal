from django import forms
from core.models import Test, Question, Category, Instruction
from ckeditor.widgets import CKEditorWidget
from .models import Candidate
import re

def category_name_list():
    categories = Category.objects.all()
    CATEGORY_CHOICE = ()

    for category in categories:
        data = ((category.category, category.category),)
        CATEGORY_CHOICE = CATEGORY_CHOICE + data

    return CATEGORY_CHOICE


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
    category = forms.category = forms.ChoiceField(choices=category_name_list,label="Question Category")
    choice1 = forms.CharField(widget=CKEditorWidget())
    choice2 = forms.CharField(widget=CKEditorWidget())
    choice3 = forms.CharField(widget=CKEditorWidget())
    choice4 = forms.CharField(widget=CKEditorWidget())
    correct_choice = forms.IntegerField()

    class Meta:
        fields = ['category', 'question_text','choice1','choice2','choice3','choice4', 'correct_choice']


class CandidateRegistration(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = '__all__'

    def unique_email(self):

        email = self.cleaned_data.get('email')

        if Candidate.objects.all().filter(email=email).exists():
            raise forms.ValidationError("Email already exist in data base")
        return email



