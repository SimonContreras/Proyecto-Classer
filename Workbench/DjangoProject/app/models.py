from django.db import models


# Create your models here.
class AbstractData(models.Model):
    order = models.TextField(default="Default")
    topic = models.TextField(default="Default")
    url = models.TextField(default="Default")
    information = models.TextField(default="Default")
    tags = models.TextField(default="Default")
    metadata = models.TextField(default="Default")

    class Meta:
        abstract = True


class ScrapedData(AbstractData):
    code = models.BooleanField(default=False)
    classification = models.TextField(default="Default")
    tags = models.TextField(default="Default")


class ScrapedImage(AbstractData):
    width = models.IntegerField(default=100)
    height = models.IntegerField(default=100)


class ScrapedVideo(models.Model):
    order = models.TextField(default="Default")
    topic = models.TextField(default="Default")
    url = models.TextField(default="Default")
    information = models.TextField(default="Default")


class TrainingDocument(models.Model):
    description = models.TextField(default="Descripción de la Data de entrenamiento contenida en el documento")
    document = models.FileField(upload_to='documents/')
    upload_at = models.DateTimeField(auto_now=True)


