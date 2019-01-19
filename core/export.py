import xlwt
from django.http import HttpResponse
from .models import Marks

def export_xls(modeladmin, request, queryset):
    queryset = Marks.objects.all()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Marksheet.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Marksheet")
    queryset = queryset.order_by('-marks')
    row_num = 0
    
    columns = [
        (u"STUDENT NUMBER", 1000),
        (u"CANDIDATE", 1000),
        (u"TESTNAME", 1000),
        (u"MARKS", 1000),
        (u"PERCANTAGE",1000)
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        ws.col(col_num).width = columns[col_num][1]*7

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    
    for obj in queryset:
        row_num += 1
        row = [
            obj.candidate.std_no,
            obj.candidate.name,
            obj.test_name.test_name,
            obj.marks,
            obj.percentage,
        ]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response
    
export_xls.short_description = u"Export as XLS"