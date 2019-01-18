from django import forms
from core.models import Test, Question, Category, Instruction
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Candidate
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.core.validators import RegexValidator


BRANCH_CHOICES = (('cse', 'CSE'),
                  ('it', 'IT'),
                  ('ec', 'ECE'),
                  ('en', 'EN'),
                  ('me', 'ME'),
                  ('ce', 'CE'),
                  ('ei', 'EI'),
                  ('mca', 'MCA'),
                  )
YES_OR_NO = (('yes' ,'Hosteler'),
             ('no', 'Dayscholar'))

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
    on_or_off = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Status", 
                              initial='', widget=forms.RadioSelect(), required=True)

    class Meta:
        model = Test
        fields = ['test_name','duration','on_or_off']


class InstructionForm(forms.ModelForm):
    test_name = forms.ChoiceField(choices=test_name_list, label="Test Category", widget=forms.Select() )
    
    class Meta:
        model = Instruction
        fields = ['instruction','test_name']


class CategoryForm(forms.ModelForm):
    test_name = forms.ChoiceField(choices=test_name_list, label="Test Category", widget=forms.Select() )
    number_of_questions = forms.CharField(label="Number of selected questions")

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
    name = forms.CharField(max_length=100, required=True)
    std_no_regex = RegexValidator(regex=r"^\d{7}$")
    std_no = forms.CharField(validators=[std_no_regex], max_length=7, required=False)
    email = forms.EmailField(required=True)
    father = forms.CharField(max_length=255, required=False)
    phone_regex = RegexValidator(regex=r"^[789]\d{9}$")
    phone_number = forms.CharField(validators=[phone_regex], max_length=10, required=False)
    branch = forms.ChoiceField(choices=BRANCH_CHOICES, required=False)
    skills = forms.CharField(max_length=255, required=False)
    designer = forms.CharField(max_length=255, required=False)
    # test_name = forms.CharField(max_length=100, required=False)

    # test_name = forms.ModelChoiceField(queryset=Test.objects.filter(on_or_off= True), empty_label='Please Choose')
    # test_obj = Test.objects.get(test_name=request.session["test_name"])


    hosteler = forms.ChoiceField(widget=forms.RadioSelect(), label = 'Are you a Hosteler?', choices = YES_OR_NO, required=False)
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
    class Meta:
        model = Candidate
        fields = ['name','email','std_no','phone_number','branch','hosteler','skills','designer','test_name','father', 'captcha']


class ChooseTestForm(forms.Form):
    test_name = forms.ChoiceField(choices=test_name_list, label="Choose Test", widget=forms.Select() )

    class Meta:
        fields = ['test_name']


class AlgorithmForm(forms.Form):
    question_text = forms.CharField(widget=CKEditorUploadingWidget())
    test_name = forms.ChoiceField(choices=test_name_list, label="Choose Test", widget=forms.Select() )

    class Meta:
        fields = ['category', 'test_name']


class GetTestNameForm(forms.Form):
    test_name = forms.ChoiceField(choices=test_name_list, label="Choose Test", widget=forms.Select() )

    class Meta:
        fields = ['test_name']

