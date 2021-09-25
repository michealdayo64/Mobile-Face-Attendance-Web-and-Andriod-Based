from keras.applications.vgg16 import VGG16, preprocess_input
from keras.applications.vgg19 import VGG19, preprocess_input
from keras.applications.xception import Xception, preprocess_input
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input
from keras.applications.mobilenet import MobileNet, preprocess_input
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing import image
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.utils import np_utils
from keras.models import Model
from keras.models import model_from_json
from keras.layers import Input
from keras.models import load_model
from django.conf import settings
from PIL import Image
import newtrain as oo
import numpy as np
import os
#import json
#import pickle
#import cv2
#import re
#import time
#import datetime
#import gc
#import _pickle as cPickle


def get_categories():
    list_categories=[]
    for path in os.listdir('Allimages/'):
        if '.DS_Store' in path:
            pass
        else:
            list_categories.append(path)
    print("Found Categories ",list_categories,'\n')
    return list_categories

'''def takeAttendance():
    from keras.models import load_model'''

def takeAttendance(atended):
    #file_path = os.path.join(settings.BASE_DIR, 'take_attendance/')
    test_path="take_attendance"
    for filename in os.listdir(test_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            kk = os.path.join(test_path, filename)
            model_path=os.path.join("model_6c.h5")
            model = load_model(model_path) 
            dimage = image.load_img(kk,True,target_size=(80,80))
            img = np.expand_dims(dimage, axis=0)
            img = image.img_to_array(img)
            img = img/255
            allcatlist=get_categories()
            catlen = len(allcatlist)
            n_classes = catlen
            print("Shape before one-hot encoding: ", img.shape)
            img = np_utils.to_categorical(img, n_classes)
            print("Shape after one-hot encoding: ", img.shape)
            prob = model.predict(img)
        #     print(prob[0])

            top_3 = np.argsort(prob[0])#[:-4:-1]
        #     print(top_3)
            classes=[]
            for path in os.listdir("Allimages"):
                    if '.DS_Store' in path:
                        pass
                    else:
                        classes.append(path)
            print(classes)
        #     column_lookups = pd.read_csv("Encoded_data_column_lookup.csv", delimiter=" ")
        #     classes = np.asarray(column_lookups.iloc[1:29, 0])

            alldatacount=[]
            atended=[]
            for i in range(0,len(classes)):
                print("{}".format(classes[top_3[i]])+" ({:.3})".format(prob[0][top_3[i]]))
                alldatacount.append({"name":classes[top_3[i]],"percent":prob[0][top_3[i]]})
                if(prob[0][top_3[i]]>=0.5):
                    atended.append({"name":classes[top_3[i]]})
            plt.imshow(dimage)
            print(alldatacount)
            print(atended)
            return atended

