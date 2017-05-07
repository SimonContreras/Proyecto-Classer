from django.db import models


# Create your models here.
class ScrapedData(models.Model):
    order = models.TextField(default="Default")
    topic = models.TextField(default="Default")
    url = models.TextField(default="Default")
    information = models.TextField(default="Default")

    def __str__(self):
        return self.topic


class ScrapedImage(models.Model):
    order = models.TextField(default="Default")
    topic = models.TextField(default="Default")
    url = models.TextField(default="Default")
    information = models.TextField(default="Default")

    def __str__(self):
        return self.topic
