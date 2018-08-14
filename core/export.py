import xlwt
from django.http import HttpResponse

def export_xls(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Marksheet.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Marksheet")
    queryset = queryset.order_by('-marks')
    row_num = 0
    
    columns = [
        (u"STUDENT NUMBER", 2000),
        (u"CANDIDATE", 2000),
        (u"TESTNAME", 2000),
        (u"MARKS", 2000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    
    for obj in queryset:
        row_num += 1
        row = [
            obj.candidate.std_no,
            obj.candidate.name,
            obj.test_name.test_name,
            obj.marks,
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response
    
export_xls.short_description = u"Export XLS"