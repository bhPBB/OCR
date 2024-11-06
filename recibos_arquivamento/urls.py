# urls.py
from django.urls import path
from .views import OCRUploadView

urlpatterns = [
    path('', OCRUploadView.as_view(), name='upload'),
]