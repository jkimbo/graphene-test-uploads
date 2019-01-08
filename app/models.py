from django.db import models

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=100)

class Image(models.Model):
    image_file = models.ImageField()
    post = models.ForeignKey(
        Post,
        related_name="gallery",
        on_delete=models.CASCADE
    )