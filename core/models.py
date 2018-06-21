from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from django.contrib.sessions.models import Session


class Test(models.Model):
    test_name = models.CharField(max_length=100, blank=False, unique=True)
    duration = models.PositiveIntegerField(blank=False)
    on_or_off = models.BooleanField(blank=False)

    def __str__(self):
        return self.test_name


class Instruction(models.Model):
    instruction = RichTextUploadingField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Instructions"

    def __str__(self):
        return self.instruction


class Category(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    category = models.CharField(max_length=225)
    number_of_questions = models.IntegerField(null=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category + "--" + self.test.test_name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_number = models.PositiveIntegerField(blank=True)
    question_text = RichTextUploadingField()
    choice1 = RichTextUploadingField()
    choice2 = RichTextUploadingField()
    choice3= RichTextUploadingField()
    choice4 = RichTextUploadingField()
    correct_choice = models.PositiveIntegerField(blank=False)
    negative = models.BooleanField(default=False)
    negative_marks = models.IntegerField(null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.question_text


# def test_name_list():
#     test_name = []
#     all_test = Test.objects.all()
#     for test in all_test:
#         test_name.append((test.test_name, test.test_name))
#     return test_name


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    father_name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r"^[789]\d{9}$")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)
    test_name = models.CharField(max_length=100, null=Test)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + self.email


class SelectedAnswer(models.Model):
    email = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    question_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.IntegerField(blank=True)
    status = models.PositiveIntegerField(default=1)

    def __str__(self):
        st = str(self.question_text) + ' - ' + str(self.selected_choice)
        return st
