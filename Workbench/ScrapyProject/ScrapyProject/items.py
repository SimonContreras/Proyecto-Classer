# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from app.models import ScrapedData
from app.models import ScrapedImage
from app.models import ScrapedVideo


class ScrapedDataItem(DjangoItem):
    django_model = ScrapedData


class ScrapedImageItem(DjangoItem):
    django_model = ScrapedImage


class ScrapedVideoItem(DjangoItem):
    django_model = ScrapedVideo


