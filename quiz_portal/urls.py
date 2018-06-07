from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('admin/', include('core.urls_admin')),
    path('', include('core.urls_candidate')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', TemplateView.as_view(template_name='core/instructions.html'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

