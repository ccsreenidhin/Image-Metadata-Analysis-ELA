# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Document(models.Model):
    orimage = models.ImageField(upload_to='original', null = True)
    elaimage = models.ImageField(upload_to='elaimage', null = True)


class DocumentAuthenticity(models.Model):
    authenticity = models.OneToOneField(Document, on_delete=models.CASCADE)
    result= models.IntegerField(null = True)
    exifresult =  models.IntegerField(null = True)
    elaresult =  models.IntegerField(null = True)
