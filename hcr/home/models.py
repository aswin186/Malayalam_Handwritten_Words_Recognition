from django.db import models

# Create your models here.

class UpImages(models.Model):
    image = models.ImageField(upload_to='images', blank=False)

    def __str__(self):
        return self.image