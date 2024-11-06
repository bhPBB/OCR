from django.db import models

class ImageUpload(models.Model):
    image = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)