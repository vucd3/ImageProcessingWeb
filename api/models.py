from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, default='name')
    passwd = models.CharField(max_length=50, default='passwd')

class Image(models.Model):
    image = models.ImageField(upload_to='image/', blank=False)

class ImageProcessing(models.Model):
    mask_size = models.IntegerField(default=1)
    brightness = models.IntegerField(default=1)
    