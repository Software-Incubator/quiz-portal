"""quiz_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.urls import path

from django.views.generic.base import TemplateView
from core import views as core_views


urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('admin/', include('core.urls_admin')),
    # path('', include('core.urls_candidate'))
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', TemplateView.as_view(template_name='core/instructions.html'), name='home'),
    path('signup/', core_views.signup, name='signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
