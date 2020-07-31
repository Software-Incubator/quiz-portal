from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from core.models import Category, Question, Test, Instruction, Candidate,\
    SelectedAnswer, Marks, Additional, AdditionalQuestion, \
    Practice_Candidate,Practice_SelectedAnswer, Unique_ID
    # Practice_Test,Practice_Category,Practice_Question, Practice_Test_Instructions,\
    
from core.export import export_xls
from core.models import CategoryMarks


class CandidateAdmin(admin.ModelAdmin):
    actions = [export_xls]

    class Meta:
        model = Candidate


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    # list_editable = ['category']
    search_fields = ['category']
    list_display = ('id', 'category')

    class Meta:
        model = Category

#
# class MarksAdmin(admin.ModelAdmin):
#     list_display = ('test_name', 'candidate', 'marks')
#
#     class Meta:
#         model = Marks


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


# class CandidateAdmin(admin.ModelAdmin):
#     search_fields = ['name', 'email', 'phone_number','hosteler','std_no','branch']
#     list_display = ('id', 'name', 'email', 'phone_number','hosteler','std_no','branch')
#
#     class Meta:
#         model = Candidate


class TestAdmin(admin.ModelAdmin):
    search_fields = ['id', 'test_name']
    list_display = ('id', 'test_name', 'duration')

    class Meta:
        model = Test


class MarksAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'candidate', 'marks')
    actions = [export_xls]

    class Meta:
        model = Marks


class AdditionalAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'name', 'on_or_off')
    search_fields = ['test_name', 'name', 'on_or_off']

    class Meta:
        model = Additional


class AdditionalQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text',)
    search_fields = ['id','question_text']

    class Meta:
        model = AdditionalQuestion


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Instruction)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(SelectedAnswer)
admin.site.register(AdditionalQuestion, AdditionalQuestionAdmin)
admin.site.register(Additional, AdditionalAdmin)
admin.site.register(Marks, MarksAdmin)
admin.site.register(CategoryMarks)

admin.site.register(Practice_Candidate)
admin.site.register(Practice_SelectedAnswer)
admin.site.register(Unique_ID)
