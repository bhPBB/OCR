from django.db import models

class ImageUpload(models.Model):
    image = models.FileField(upload_to='')