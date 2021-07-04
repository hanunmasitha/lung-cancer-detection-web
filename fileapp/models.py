# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from posixpath import basename

from django.db import models
from datetime import datetime
import os
import patoolib
import shutil


def document_directory_path(instance, filename):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    file_type = ""
    image_list = ['.jpeg', '.jpg', '.gif', '.bmp', '.svg', '.psd', 'cpt',
                  'psp', 'cxf', 'pdn', 'jfif', 'exif', 'tiff', 'ppm', 'pgm ', 'pnm']
    video_list = ['.mp4', '.avi', '.wmv', '.m4a', '.3gp', '.3gpp', '.wav',
                  'mov', 'webm', 'hdv', 'vob', 'm4v', 'f4v', 'm4b', 'oga', 'ogv']
    if ext.lower() in image_list:
        file_type = "images"
    elif ext.lower() in video_list:
        file_type = "videos"
    else:
        file_type = "others"
    print(name)
    path = 'media/uploads/rar/{}{}'.format(name, ext)
    #path = 'media/uploads/%Y/%m/%d/{}/{}{}'.format(file_type, name, ext)
    return datetime.now().strftime(path)

class Extract(object):
    def __init__(self):
        path = 'media/uploads/rar'
        extract_dir = 'media/uploads/patient'
        arr = os.listdir(path)

        for file in arr:
            name, ext = os.path.splitext(file)
            if not os.path.isdir(extract_dir+name):
                new_path = extract_dir + '/{}'.format(name)
                patoolib.extract_archive(path+'/'+file, outdir=new_path)

class DeletePatient(object):
    def __init__(self):
        path = 'media/uploads/patient'
        file_detele = os.listdir(path)

        for detele in file_detele:
            shutil.rmtree(path+'/'+detele)
        
class Fileup(models.Model):
    file = models.FileField(upload_to=document_directory_path)

    def filename(self):
        return os.path.basename(self.file.name)
