from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include('recibos_arquivamento.urls')),
]

if settings.LOCAL:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
