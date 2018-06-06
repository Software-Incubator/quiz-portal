from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Test(models.Model):
    Tname = models.CharField(max_length=100, blank=False)
    duration = models.PositiveIntegerField(blank = False)

class Category(models.Model):
    Tname = models.ForeignKey(Test, on_delete=models.CASCADE)
    Cname = models.CharField(max_length=100, blank=False)

class Questions(models.Model):
    Cname = models.ForeignKey(Category, on_delete=models.CASCADE)
    Question = RichTextUploadingField()
    Choice1 = RichTextUploadingField()
    Choice2 = RichTextUploadingField()
    Choice3 = RichTextUploadingField()
    Choice4 = RichTextUploadingField()
    right_choice = RichTextUploadingField()

class Instructions(models.Model):
    Tname = models.ForeignKey(Test, on_delete=models.CASCADE)
    Instruction = RichTextUploadingField()

class Student_details(models.Model):
    Name = models.CharField(max_length=100, blank=True)
    Father_name = models.CharField(max_length=100, blank=True)
    Email = models.EmailField(blank = False)
    Phone_number = models.CharField(max_length=100, blank=True)

class Questions_Answer(models.Model):
    Email = models.ForeignKey(Student_details, on_delete=models.CASCADE)
    Question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    selected_choice = RichTextUploadingField()


