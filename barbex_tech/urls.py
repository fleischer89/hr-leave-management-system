"""uhg_intranet URL Configuration

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
from django.conf.urls import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

handler400 = 'intranet.views.handler400'
handler403 = 'intranet.views.handler403'
handler404 = 'intranet.views.handler404'
handler500 = 'intranet.views.handler500'

urlpatterns = [
    url(r'', include('intranet.urls')),
    url(r'^panel/?', include('intranet.urls')),
    url(r'^v1/?', include('intranet.api_urls')),
    url(r'^admin/', admin.site.urls),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
