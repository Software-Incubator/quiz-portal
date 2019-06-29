from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from core import views_admin

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('admin/', include('core.urls_admin')),
    path('', include('core.urls_candidate')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('secret/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views_admin.error404
handler400 = views_admin.error400
handler500 = views_admin.error500
handler403 = views_admin.error403