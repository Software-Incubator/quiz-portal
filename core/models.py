from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Test(models.Model):
    test_name = models.CharField(max_length=100, blank=False)
    duration = models.PositiveIntegerField(blank = False)

    def __str__(self):
        return self.test_name

class Instruction(models.Model):
    instruction = RichTextUploadingField()

    def __str__(self):
        return self.instruction

class Category(models.Model):
    category = models.CharField(max_length=225)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


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
        return self.question_text


# class QuestionChoice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice = RichTextUploadingField()
#     def __str__(self):
#         return "<Choice = %s>" % self.choice

# class CorrectChoice(models.Model):
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE,
#                                     db_column='question_id')
#     correct_choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)

#     def __str__(self):
#         return "<Correct choice = %s>" % self.correct_choice

# class Category(models.Model):
#     test_name = models.ForeignKey(Test, on_delete=models.CASCADE)
#     category_name = models.CharField(max_length=100, blank=False)
#
# class Question(models.Model):
#     category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
#     question = RichTextUploadingField()
#     choice1 = RichTextUploadingField()
#     choice2 = RichTextUploadingField()
#     choice3 = RichTextUploadingField()
#     choice4 = RichTextUploadingField()
#     right_choice = RichTextUploadingField()
