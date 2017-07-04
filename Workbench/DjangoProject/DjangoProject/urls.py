"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from app import views as core_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', auth_views.login, {'template_name': 'logloglog.html'}, name='login'),
    url(r'^menu/$', login_required(TemplateView.as_view(template_name="menu.html")), name='menu'),
    url(r'^login/$', auth_views.login, {'template_name': 'logloglog.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^signup/$', core_views.signup,  name='signup'),
    url(r'^menu/imagenes/$', login_required(core_views.imagenes), name='imagenes'),
    url(r'^menu/showdata/$', login_required(core_views.showdata), name='showdata'),
    url(r'^menu/classify_example/$', login_required(core_views.classify_example), name='classify_example'),
    url(r'^menu/urls/$', login_required(core_views.urls), name='urls'),
    url(r'^menu/entities_example/$', login_required(core_views.entities_example), name='entities_example'),
    url(r'^menu/classify/upload_file/$', login_required(core_views.file_upload), name='upload_file'),
    url(r'^menu/videos/$', login_required(core_views.show_videos), name='videos'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


