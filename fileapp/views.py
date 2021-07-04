# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from .forms import FileupForm
from .models import Fileup, Extract, DeletePatient

import tensorflow as tf
from keras.models import load_model
import numpy as np
import operator
import glob
import os


class BasicUploadView(View):
    visibility = False
    final_result = []
    def get(self, request):
        Extract()
        file_list = Fileup.objects.all()
        return render(self.request, 'fileapp/index.html', {'files': file_list, 
                                                            'visibiliy': self.visibility, 
                                                            'result' : self.final_result})

    def post(self, request):
        form = FileupForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            files = form.save()
            data = {'is_valid': True, 'name': files.file.name,
                    'url': files.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

def clear_database(request):
    for files in Fileup.objects.all():
        files.file.delete()
        files.delete()
    DeletePatient()
    BasicUploadView.visibility  = False
    print(BasicUploadView.visibility)
    BasicUploadView.final_result.clear()
    return redirect(request.POST.get('next'))

def detection(request):
    BasicUploadView.visibility = True
    print(BasicUploadView.visibility)

    model_path = r'E:\Koding\Backend\TA coba 2\django-multiple-fileupload-master\media\model.h5'
    cnn = load_model(model_path)

    picture_size = 64
    result = {
    "Kanker": 0,
    "Normal": 0,
    "Tumor": 0
    }
    result_key = list(result)

    path = r"E:\Koding\Backend\TA Beneran\mywebsite\media\uploads\patient\*"
    for address_patient in glob.glob(path):
        name = os.path.basename(address_patient)
        patient_result = []
        print("Folder : {}".format(address_patient))
        idx = 0
        for address in glob.glob(address_patient+"/*"):
            idx += 1
            print("Deteksi file {}".format(address))
            test_image = tf.keras.preprocessing.image.load_img(address, target_size = (picture_size, picture_size))
            x = tf.keras.preprocessing.image.img_to_array(test_image)
            x = np.expand_dims(x, axis=0)

            test_image_try = np.vstack([x])

            prediction = cnn.predict(test_image_try, verbose=0)

            for i in range(len(result_key)):
                if (prediction[0][i] == 1):
                    result[result_key[i]] += 1

        patient_result.append(name)
        patient_result.append(result["Kanker"]*100/idx)
        patient_result.append(result["Tumor"]*100/idx)
        patient_result.append(result["Normal"]*100/idx)
        patient_result.append(max(result.items(), key=operator.itemgetter(1))[0])
        BasicUploadView.final_result.append(patient_result)
        
        for i in range(len(result_key)):
            result[result_key[i]] = 0
    return redirect(request.POST.get('next'))
