from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=225)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return "Category = %s" % self.category


class Question(models.Model):
    question_text = models.CharField(max_length=5000)
    negative = models.BooleanField()
    negative_marks = models.IntegerField(null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return "<Question: %s>" % self.question_text


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=2000)

    def __str__(self):
        return "<Choice = %s>" % self.choice


class CorrectChoice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE,
                                    db_column='question_id')
    correct_choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)

    def __str__(self):
        return "<Correct choice = %s>" % self.correct_choice

