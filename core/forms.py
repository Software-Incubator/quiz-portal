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



class RegisterForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'


    def clean_email(self):
        email = self.cleaned_data.get("email")
        # print(email)
        pattern = "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
        prog = re.compile(pattern)
        result = prog.match(email)

        if not bool(result):
            raise forms.ValidationError("Invalid Email address. Use a valid email address.")

        if len(str(email)) > 60:
            raise forms.ValidationError("Invalid Length")

        return email


    def clean_name(self):
        name = self.cleaned_data.get('name')
        # print(name)

        pat = "^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$"
        pro = re.compile(pat)
        result = pro.match(name)

        if not bool(result):
            raise forms.ValidationError("Invalid Nameformat")


        if len(str(name)) > 100:
            raise forms.ValidationError("Invalid length ")

        return name

    # def clean_Contact(self):
    #     contact = self.cleaned_data.get('Contact')
    #     patt = "^[7-9][0-9]{9}"
    #     pro = re.compile(patt)
    #     result = pro.match(str(contact))
    #
    #     if not bool(result):
    #         raise forms.ValidationError("Invalid Contact number format ")
    #
    #     if len(str(contact)) != 10:
    #         raise forms.ValidationError("Invalid Contact number format ")
    #     return contact

