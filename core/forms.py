from django import forms
from core.models import Test, Question, Category, Instruction
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Candidate
import re


def category_name_list():
    categories = Category.objects.all()
    CATEGORY_CHOICE = ()

    for category in categories:
        data = ((category.category, category.category),)
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
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

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

    class Meta:
        model = Category
        fields = ['category', 'test_name']


class QuestionForm(forms.Form):
    test_name = forms.ChoiceField(choices=test_name_list, label="Test Category", widget=forms.Select() )
    question_text = forms.CharField(widget=CKEditorUploadingWidget())
    category = forms.ChoiceField(choices=category_name_list,label="Question Category")
    choice1 = forms.CharField(widget=CKEditorUploadingWidget())
    choice2 = forms.CharField(widget=CKEditorUploadingWidget())
    choice3 = forms.CharField(widget=CKEditorUploadingWidget())
    choice4 = forms.CharField(widget=CKEditorUploadingWidget())
    correct_choice = forms.ChoiceField(choices=answer_choice, label="Select answer")

    class Meta:
        fields = ['category', 'question_text','choice1','choice2','choice3','choice4', 'correct_choice','test_name']


class CandidateRegistration(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = '__all__'

    def unique_email(self):

        email = self.cleaned_data.get('email')

        if Candidate.objects.all().filter(email=email).exists():
            raise forms.ValidationError("Email already exist in data base")
        return email



