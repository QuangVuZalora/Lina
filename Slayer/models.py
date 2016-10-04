from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ImageFile(models.Model):
    image = models.ImageField(upload_to = 'img/', default = 'img/no-img.jpg')
