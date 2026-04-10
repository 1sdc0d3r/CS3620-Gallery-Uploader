from django.db import models

# Create your models here.
#todo model named image

class Image(models.Model):
    # img = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    img = models.ImageField(upload_to='images')
