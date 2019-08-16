import xlwt
from django.http import HttpResponse
from .models import Marks
from .models import SelectedAnswer, Candidate,CategoryMarks
from .models import Test, Category


def export_xls(modeladmin, request, queryset):
    category_marks = CategoryMarks.objects.all()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Marksheet.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Marksheet")
    # queryset = queryset.order_by('-marks')
    row_num = 0
    
    columns = [
        (u"NAME", 1000),
        (u"UNIVERSITY ROLL.", 1000),
        (u"BRANCH", 1000),
        (u"EMAIL", 1000),
        (u"PHONE NUMBER", 1000),
        (u"CORRECT MATHEMATICS", 1000),
        (u"INCORRECT MATHEMATICS", 1000),
        (u"SCORE MATHEMATICS", 1000),
        (u"CORRECT VERBAL", 1000),
        (u"INCORRECT VERBAL", 1000),
        (u"SCORE VERBAL", 1000),
        (u"CORRECT ANALYTICAL", 1000),
        (u"INCORRECT ANALYTICAL", 1000),
        (u"SCORE ANALYTICAL", 1000),
        (u"TOTAL CORRECT", 1000),
        (u"TOTAL INCORRECT", 1000),
        (u"TOTAL SCORE", 1000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        ws.col(col_num).width = columns[col_num][1]*7

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    for obj in queryset:
        candidate_all_category = category_marks.filter(candidate=obj)
        maths = candidate_all_category[0]
        verbal = candidate_all_category[1]
        analytical = candidate_all_category[2]
        row_num += 1
        row = [
            obj.name.upper(),
            obj.university_roll_no,
            obj.branch.upper(),
            obj.email,
            obj.phone_number,
            maths.correct,
            maths.incorrect,
            maths.marks,
            verbal.correct,
            verbal.incorrect,
            verbal.marks,
            analytical.correct,
            analytical.incorrect,
            analytical.marks,
            maths.correct+verbal.correct+analytical.correct,
            maths.incorrect + verbal.incorrect + analytical.incorrect,
            maths.marks + verbal.marks + analytical.marks

        ]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response
    
export_xls.short_description = u"Export as XLS"

