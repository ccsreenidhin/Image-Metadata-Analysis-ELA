from django.conf.urls import url
from imgaut import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     url(r'^$', views.upload, name='upload'),
     url(r'^about/$', views.about, name='about'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
