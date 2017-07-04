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
    data_entrenamiento = models.BooleanField(default=False)


class ScrapedImage(AbstractData):
    width = models.IntegerField(default=100)
    height = models.IntegerField(default=100)


class ScrapedVideo(models.Model):
    order = models.TextField(default="Default")
    topic = models.TextField(default="Default")
    url = models.TextField(default="Default")
    information = models.TextField(default="Default")

class ScrapUrl(models.Model):
    url = models.TextField(default="Default")
    propagacion_interna = models.BooleanField(default=False)

class TrainingDocument(models.Model):
    description = models.TextField(default="Descripcion de la Data de entrenamiento contenida en el documento")
    document = models.FileField(upload_to='documents/')
    upload_at = models.DateTimeField(auto_now=True)


