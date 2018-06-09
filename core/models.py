from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Test(models.Model):
    test_name = models.CharField(max_length=100, blank=False)
    duration = models.PositiveIntegerField(blank = False)

    def __str__(self):
        return self.test_name


class Instruction(models.Model):
    instruction = RichTextUploadingField()

    class Meta:
        verbose_name_plural = "Instructions"

    def __str__(self):
        return "Instruction = %s" % self.instruction


class Category(models.Model):
    name = models.CharField(max_length=225)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_text = RichTextUploadingField()
    choice1 = RichTextUploadingField()
    choice2 = RichTextUploadingField()
    choice3= RichTextUploadingField()
    choice4 = RichTextUploadingField()
    correct_choice = models.IntegerField(blank=False)
    negative = models.BooleanField(default=False)
    negative_marks = models.IntegerField(null=True)
    marks = models.IntegerField(null=True)

    def __str__(self):
        return "<Question: %s>" % self.question_text



class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    father_name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r"^[789]\d{9}$")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)

    def __str__(self):
        return "{}".format(self.email)


class SelectedAnswer(models.Model):
    email = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    question_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return (self.question_text + ' ' + self.selected_choice)
