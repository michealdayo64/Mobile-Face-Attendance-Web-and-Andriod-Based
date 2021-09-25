#!/usr/bin/env python
# coding: utf-8

# In[2]:


# organize imports
from __future__ import print_function

# keras imports
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.applications.vgg19 import VGG19, preprocess_input
from keras.applications.xception import Xception, preprocess_input
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input
from keras.applications.mobilenet import MobileNet, preprocess_input
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing import image
from keras.models import Model
from keras.models import model_from_json
from keras.layers import Input
from keras.models import load_model

# other imports
# from sklearn.linear_model import LogisticRegression
import numpy as np
import os
import json
import pickle
#import cv2
import re
import time
import datetime
import gc
import _pickle as cPickle


def get_categories():
    list_categories=[]
    for path in os.listdir('Allimages/'):
        if '.DS_Store' in path:
            pass
        else:
            list_categories.append(path)
    print("Found Categories ",list_categories,'\n')
    return list_categories


def takeAttendance():
        # config variables
        model_name    = "vgg16"
        weights       = "imagenet"
        include_top   = 0 
        datatype="attendance"
        train_path    =  "Allimages/"
        test_path 		= "take_attendance/"
        features_path 	= "output/"+datatype +"/" + model_name + "/features.h5"
        labels_path 	= "output/"+datatype +"/" + model_name + "/labels.h5"
        test_size 		= 0.10
        results 		= "output/"+datatype +"/" + model_name + "/results.txt"
        model_path 		= "output/"+datatype +"/" + model_name + "/model"
        seed 			= 9
        thecnnclassifier_path = "output/"+datatype +"/" + model_name + "/classifiercnn.h5"



        gc.disable()

        # start time
        print ("[STATUS] start time - {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        start = time.time()

        # load the trained classifier
        print ("[INFO] loading the classifier CNN...")
        classifierann = load_model(thecnnclassifier_path)
        print("classifrer")
        print(classifierann)
        # pretrained models needed to perform feature extraction on test data too!
        if model_name == "vgg16":
          base_model = VGG16(weights=weights)
          model = Model(base_model.input, base_model.get_layer('fc1').output)
          image_size = (224, 224)
        elif model_name == "vgg19":
          base_model = VGG19(weights=weights)
          model = Model(input=base_model.input, output=base_model.get_layer('fc1').output)
          image_size = (224, 224)
        elif model_name == "resnet50":
          base_model = ResNet50(weights=weights)
          model = Model(input=base_model.input, output=base_model.get_layer('flatten').output)
          image_size = (224, 224)
        elif model_name == "inceptionv3":
          base_model = InceptionV3(include_top=include_top, weights=weights, input_tensor=Input(shape=(299,299,3)))
          model = Model(input=base_model.input, output=base_model.get_layer('flatten').output)
          image_size = (299, 299)
        elif model_name == "inceptionresnetv2":
          base_model = InceptionResNetV2(include_top=include_top, weights=weights, input_tensor=Input(shape=(299,299,3)))
          model = Model(input=base_model.input, output=base_model.get_layer('conv_7b').output)
          image_size = (299, 299)
        elif model_name == "mobilenet":
          base_model = MobileNet(include_top=include_top, weights=weights, input_tensor=Input(shape=(224,224,3)), input_shape=(224,224,3))
          model = Model(input=base_model.input, output=base_model.get_layer('conv1_relu').output)
          image_size = (224, 224)
        elif model_name == "xception":
          base_model = Xception(weights=weights)
          model = Model(input=base_model.input, output=base_model.get_layer('avg_pool').output)
          image_size = (299, 299)
        else:
          base_model = None

        # get all the train labels
        train_labels = os.listdir(train_path)

        # get all the test images paths
        test_images = os.listdir(test_path)
        classes =get_categories()
        themainindex=0;
        # loop through each image in the test data
        for image_path in test_images:
            path = test_path + "/" + image_path
            print(path)
            img  = image.load_img(path, target_size=image_size)
            x  = image.img_to_array(img)
            x  = np.expand_dims(x, axis=0)
            x  = preprocess_input(x)
            feature  = model.predict(x)
            flat = feature.flatten()
            flat= np.vstack([flat])
            flat= flat.reshape(64, 64,1)
        #     flat = flat.astype('float32')
        #     flat = flat / 255.0
            flat  = np.expand_dims(flat, axis=0)
            predscnn  = classifierann.predict_classes(flat)
            print(predscnn[0])
        #     themainindexcnn=predscnn[0]# CNN
            print(train_labels)
            print(predscnn)
            top_3 = np.argsort(predscnn[0])[:-4:-1]
            print(top_3)
            for i in range(len(top_3)):
                  print("{}".format(classes[top_3[i]]))
                  #print("{}".format(classes[top_3[i]])+" ({:.3})".format(predscnn[0][top_3[i]]))
            print("----------------------------------");

        #     img  = image.load_img(path, target_size=image_size)
        #     x  = image.img_to_array(img)
        #     x  = np.expand_dims(x, axis=0)
        #     x  = preprocess_input(x)
        #     feature  = model.predict(x)
        #     flat = feature.flatten()
        #     flat= flat.reshape( 64, 64, 1)
        #     flat  = np.expand_dims(flat, axis=0)
        # #     predscnn  = classifierann.predict_classes(flat)
        #     predscnn  = classifierann.predict(flat)
        #     themainindexcnn=predscnn[0]# CNN
        #     print(train_labels)
        #     print(predscnn[0])
        #     print("----------------------------------");
        #     top_3 = np.argsort(predscnn[0])[:-4:-1]
        #     for i in range(3):
        #           print("{}".format(train_labels[top_3[i]])+" ({:.3})".format(predscnn[0][top_3[i]]))
        #     print("----------------------------------");
        #     print ("Output sorted array indices index : ", top_3)
        #     print("Output sorted array : ", themainindexcnn[top_3])
        #      for i in top_3:
        #     themainindex=themainindexcnn[-1:0]
        #     themainindex = int(themainindex)
        #     print("SELECTED INDEX IS"+ str(themainindex))
        #     prediction  = train_labels[themainindex] 


        #     # perform prediction on test image
        #     thelabel = train_labels[themainindex]
        #     thelabel= re.sub('\s+',' ',thelabel)
        #     print ("I think it is a " + thelabel)
        #     img_color = cv2.imread(path, 1)
        #     cv2.putText(img_color, "I think it is a " + thelabel, (140,445), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        #     cv2.imshow("test", img_color)

        #     # key tracker
        #     key = cv2.waitKey(0) & 0xFF
        #     if (key == ord('q')):
        #         cv2.destroyAllWindows()
        end = time.time()
        gc.enable()
        print ("[STATUS] end time - {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))