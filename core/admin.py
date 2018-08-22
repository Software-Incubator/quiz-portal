from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from core.models import Category, Question, Test, Instruction, Candidate, SelectedAnswer, Algorithm, Marks, DesignQuestion
from core.export import export_xls


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    # list_editable = ['category']
    search_fields = ['category']
    list_display = ('id', 'category')

    class Meta:
        model = Category


class QuestionAdmin(admin.ModelAdmin):
    # list_editable = ['question_text']
    search_fields = ['question_text']
    list_display = ('id', 'question_text',)

    class Meta:
        model = Question


class ChoiceAdmin(admin.ModelAdmin):
    # list_editable = ['question_text']
    search_fields = ['choice']
    list_display = ('id', 'choice', 'question')

    class Meta:
        model = SelectedAnswer


class CandidateAdmin(admin.ModelAdmin):
    search_fields = ['name', 'email', 'phone_number','hosteler','std_no','branch']
    list_display = ('id', 'name', 'email', 'phone_number','hosteler','std_no','branch')

    class Meta:
        model = Candidate


class TestAdmin(admin.ModelAdmin):
    search_fields = ['id', 'test_name']
    list_display = ('id', 'test_name', 'duration')

    class Meta:
        model = Test


class MarksAdmin(admin.ModelAdmin):

    # actions = [export_csv, export_xls, export_xlsx]
    list_display = ('test_name', 'candidate', 'marks')
    actions = [export_xls]


    class Meta:
        model = Marks


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Instruction)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(SelectedAnswer)
admin.site.register(Algorithm)

admin.site.register(Marks, MarksAdmin)
admin.site.register(DesignQuestion)
