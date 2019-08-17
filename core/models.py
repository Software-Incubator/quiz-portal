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
    negative = models.BooleanField(default=False)
    std_no = models.BooleanField(default=False)
    father_name = models.BooleanField(default=False)
    phone_number = models.BooleanField(default=False)
    branch = models.BooleanField(default=False)
    skills = models.BooleanField(default=False)
    designer = models.BooleanField(default=False)
    hosteler = models.BooleanField(default=False)
    year = models.BooleanField(default=False)
    university_roll_no = models.BooleanField(default=False)

    def __str__(self):
        return self.test_name


class Instruction(models.Model):
    test = models.OneToOneField(Test, on_delete=models.CASCADE)
    instruction = RichTextUploadingField()

    class Meta:
        verbose_name_plural = "Instructions"

    def __str__(self):
        return self.instruction


class Category(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    category = models.CharField(max_length=225)
    total_question_display = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category + "--" + self.test.test_name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_text = RichTextUploadingField()
    choice1 = RichTextUploadingField()
    choice2 = RichTextUploadingField()
    choice3 = RichTextUploadingField()
    choice4 = RichTextUploadingField()
    correct_choice = models.PositiveIntegerField(blank=False)
    negative = models.BooleanField(default=True)
    negative_marks = models.IntegerField(default=1)
    marks = models.IntegerField(null=True, default=4)

    def __str__(self):
        return self.question_text


class Candidate(models.Model):
    name = models.CharField(max_length=100, blank=False)
    std_no_regex = RegexValidator(regex=r"^\d{7}$", message="Invalid Student Number", code="400")
    std_no = models.CharField(validators=[std_no_regex], blank=True, max_length=7, null=True)
    university_roll_no = models.CharField(max_length=10, blank=False, unique=True, null=False)
    email = models.CharField(unique=True,max_length=40, null=False, blank=False)
    father = models.CharField(max_length=255, blank=True, null=True)
    phone_regex = RegexValidator(regex=r"^[56789]\d{9}$")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    branch = models.CharField(max_length=5, blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    designer = models.CharField(max_length=255, blank=True, null=True)
    hosteler = models.CharField(max_length=3, blank=True, null=True)
    test_name = models.CharField(max_length=100, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.name + ' - ' + self.email


class SelectedAnswer(models.Model):
    email = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    question_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.IntegerField(blank=True, null=True)
    status = models.PositiveIntegerField(default=1)

    def __str__(self):
        st = str(self.question_text) + ' - ' + str(self.selected_choice)
        return st


class Marks(models.Model):
    test_name = models.ForeignKey(Test, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    marks = models.IntegerField(blank=False)

    def __str__(self):
        st = str(self.candidate) + ' - ' + str(self.marks) + ' - ' + str(self.test_name)
        return st


class AdditionalQuestion(models.Model):
    question_text = RichTextUploadingField()


class Additional(models.Model):
    test_name = models.ForeignKey(Test, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=False)
    on_or_off = models.BooleanField(blank=False)
    additional_question = models.ManyToManyField(AdditionalQuestion)


class CategoryMarks(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)
    unanswered = models.IntegerField(default=0)
    marks = models.IntegerField(default=0)

    class Meta:
        unique_together = ('candidate', 'category')

