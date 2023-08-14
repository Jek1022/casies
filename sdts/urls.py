"""
URL configuration for sdts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, re_path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Update the site header
admin.site.site_header = 'SDTS Administration'

urlpatterns = [
    re_path(r'^$', login_required(TemplateView.as_view(template_name='dashboard/index.html')), name='overview-panel'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),

    # Maintenance URLs
    re_path(r'^cas/', include('cas.urls', namespace='cas')),
    re_path(r'^maintenance/mainmodule/', include('mainmodule.urls', namespace='mainmodule')),
    re_path(r'^maintenance/company/', include('company.urls', namespace='company')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
