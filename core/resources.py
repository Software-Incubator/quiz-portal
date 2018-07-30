from import_export import resources
from django.http import HttpResponse
from .models import Marks


class MarksResource(resources.ModelResource):
    class Meta:
        model = Marks

    def export(request):
        mark_resource = MarksResource()
        dataset = mark_resource.export()
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="marks.csv"'
        return response

