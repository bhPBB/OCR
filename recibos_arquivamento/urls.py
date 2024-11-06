# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', OCRUploadView.as_view(), name='upload'),
    # path('resultado/', OCRResultView.as_view(), name='ocr_result'),
]