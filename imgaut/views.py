# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Document, DocumentAuthenticity
from .forms import DocumentForm
from django.views.generic import TemplateView
from django.http import HttpResponse
import StringIO
from PIL import Image
from PIL.ExifTags import TAGS
import json
from django.core.files.base import ContentFile
import os


def about(request):
    return render(request, 'about.html', {})

class cELA():
    def __init__(self, trigger, enhance, coloronly):
        self.trigger = trigger
        self.enhance = enhance
        self.coloronly = coloronly

    def CalculateELA(self, pixelA, pixelB):
        pixelDiff = map(lambda x, y: abs(x - y), pixelA, pixelB)
        if sum(pixelDiff) > self.trigger and (not self.coloronly or pixelDiff[0] != pixelDiff[1] or pixelDiff[0] != pixelDiff[2]):
            return tuple([x * self.enhance for x in pixelDiff])
        else:
	    DocumentAuthenticity.elaresult
            return (0, 0, 0)

def ELA(filenameInput, options):
    name = str(filenameInput)
    oELA = cELA(options[0], options[1], options[3])
    imOriginal = Image.open(filenameInput)
    oStringIO = StringIO.StringIO()
    imOriginal.save(oStringIO, 'JPEG', quality=options[2])
    oStringIO.seek(0)
    imJPEGSaved = Image.open(oStringIO)
    iStringIO = StringIO.StringIO()
    imNew = Image.new('RGB', imOriginal.size)
    imNew.putdata(map(oELA.CalculateELA, imOriginal.getdata(), imJPEGSaved.getdata()))
    imNew.seek(0)
    imNew.save(iStringIO, "jpeg")
    img_content = ContentFile(iStringIO.getvalue(), name)
    return img_content

def metaexif(imag):
    ret = {}
    img = Image.open(imag)
    info = img._getexif()
    print info
    try:
        for tag, value in info.items():
            decoded = TAGS.get(tag)
            try:
                ret[decoded] = value.encode('UTF-8').strip()
            except:
                try:
                    ret[decoded] = value.encode('ascii').strip()
                except:
                    pass
    except:
        DocumentAuthenticity.exifresult=0
    return ret

# upload file
def upload(request):
    metadic = {}
    exif = True
    extension = "JPEG"
    urls = {}
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            if str(document.orimage).endswith('.jpg') or str(document.orimage).endswith('.jpeg') or str(document.orimage).endswith('.JPG') or str(document.orimage).endswith('.JPEG'):
                metadic = metaexif(document.orimage)
                if len(metadic)<1:
                    urls.update({"exif":False})
                urls.update({ "orimage": document.orimage })
                document.elaimage = ELA(document.orimage, options = (10, 20, 80, False))
                urls.update({'imagela':document.elaimage })
                print "hi"
                document.save()
            else:
                extension = "not JPEG"
                urls.update({ "extension": extension })
    else:
        form = DocumentForm()
    return render(request, 'index.html', { 'form': form, 'meta':metadic, "urls":urls })
