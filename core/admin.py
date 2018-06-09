from django.contrib import admin
from core.models import Category, Question, Test, Instruction, Candidate, SelectedAnswer


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    # list_editable = ['category']
    search_fields = ['name']
    list_display = ('id', 'name')

    class Meta:
        model = Category


class QuestionAdmin(admin.ModelAdmin):
    # list_editable = ['question_text']
    search_fields = ['question_text']
    list_display = ('id', 'question_text',)

    class Meta:
        model = Category


class ChoiceAdmin(admin.ModelAdmin):
    # list_editable = ['question_text']
    search_fields = ['choice']
    list_display = ('id', 'choice', 'question')

    class Meta:
        model = Category

class CandidateAdmin(admin.ModelAdmin):
    search_fields = ['name','email','phone_number','father_name']
    list_display = ('name','email','phone_number','father_name',)

    class Meta:
        model = Candidate


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test)
admin.site.register(Instruction)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(SelectedAnswer)