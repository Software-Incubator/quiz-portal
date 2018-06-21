from django import forms
from core.models import Test, Question, Category, Instruction
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Candidate
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import re


def category_name_list():
    categories = Category.objects.all()
    CATEGORY_CHOICE = ()

    for category in categories:
        data = ((category.category, category),)
        CATEGORY_CHOICE = CATEGORY_CHOICE + data

    return CATEGORY_CHOICE


def test_name_list():
    tests = Test.objects.all()
    TEST_CHOICE = ()

    for test in tests:
        data = ((test.test_name, test.test_name),)
        TEST_CHOICE = TEST_CHOICE + data

    return TEST_CHOICE


answer_choice = ((1,1),(2,2),(3,3),(4,4))

TRUE_FALSE_CHOICES = (
    (True, 'START'),
    (False, 'STOP')
)


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=30,required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required= True)


class TestForm(forms.ModelForm):
    on_or_off = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Some Label", 
                              initial='', widget=forms.RadioSelect(), required=True)

    class Meta:
        model = Test
        fields = ['test_name','duration','on_or_off']


class InstructionForm(forms.ModelForm):
    test_name = forms.ChoiceField(choices=test_name_list,label="Test Category", widget=forms.Select() )
    
    class Meta:
        model = Instruction
        fields = ['instruction','test_name']


class CategoryForm(forms.ModelForm):
    test_name = forms.ChoiceField(choices=test_name_list,label="Test Category", widget=forms.Select() )
    number_of_questions = forms.CharField(label="Number of Questions to be selected for candidate's test")

    class Meta:
        model = Category
        fields = ['category', 'test_name','number_of_questions']


class QuestionForm(forms.Form):
    question_text = forms.CharField(widget=CKEditorUploadingWidget())
    category = forms.ChoiceField(choices=category_name_list,label="Question Category")
    choice1 = forms.CharField(widget=CKEditorUploadingWidget())
    choice2 = forms.CharField(widget=CKEditorUploadingWidget())
    choice3 = forms.CharField(widget=CKEditorUploadingWidget())
    choice4 = forms.CharField(widget=CKEditorUploadingWidget())
    correct_choice = forms.ChoiceField(choices=answer_choice, label="Select correct choice")

    class Meta:
        fields = ['category', 'question_text','choice1','choice2','choice3','choice4', 'correct_choice']


class CandidateRegistration(forms.ModelForm):
    test_name = forms.ModelChoiceField(queryset=Test.objects.filter(on_or_off= True), empty_label='Please Choose')

    class Meta:
        model = Candidate
        fields = ['name','email','father_name','phone_number','test_name']

    def unique_email(self):

        email = self.cleaned_data.get('email')

        if Candidate.objects.all().filter(email=email).exists():
            raise forms.ValidationError("Email already exist in data base")
        return email

class ChooseTestForm(forms.Form):
    test_name = forms.ChoiceField(choices=test_name_list,label="Choose Test", widget=forms.Select() )

    class Meta:
        fields = ['test_name']

