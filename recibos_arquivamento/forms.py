# forms.py
from django import forms

class ImageUploadForm(forms.Form):
    imagem = forms.FileField()
