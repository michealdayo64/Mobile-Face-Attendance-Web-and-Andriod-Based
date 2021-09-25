#!/usr/bin/env python

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
#from keras.preprocessing import image
#from keras.callbacks import EarlyStopping
#from keras.callbacks import ModelCheckpoint
#from keras.preprocessing.image import ImageDataGenerator
#import pandas as pd 
import numpy as np 
#from tqdm import tqdm
#import matplotlib.pyplot as plt
import cv2
#from keras import models
#from keras import layers
#from keras import optimizers
#from PIL import Image
#import sklearn
#from sklearn.model_selection import train_test_split
#from statistics import mean
import os
import pickle
from keras.utils import np_utils



# In[ ]:


class MasterImage(object):

    def __init__(self,PATH='', IMAGE_SIZE = 50):
        self.PATH = PATH
        self.IMAGE_SIZE = IMAGE_SIZE

        self.image_data = []
        self.x_data = []
        self.y_data = []
        self.CATEGORIES = []

        # This will get List of categories
        self.list_categories = []

    def get_categories(self):
        for path in os.listdir(self.PATH):
            if '.DS_Store' in path:
                pass
            else:
                self.list_categories.append(path)
        print("Found Categories ",self.list_categories,'\n')
        return self.list_categories

    def Process_Image(self):
        try:
            """
            Return Numpy array of image
            :return: X_Data, Y_Data
            """
            self.CATEGORIES = self.get_categories()
            for categories in self.CATEGORIES:                                                  # Iterate over categories

                train_folder_path = os.path.join(self.PATH, categories)                         # Folder Path
                class_index = self.CATEGORIES.index(categories)                                 # this will get index for classification

                for img in os.listdir(train_folder_path):                                       # This will iterate in the Folder
                    new_path = os.path.join(train_folder_path, img)                             # image Path

                    try:        # if any image is corrupted
                        image_data_temp = cv2.imread(new_path,cv2.IMREAD_GRAYSCALE)                 # Read Image as numbers
                        image_temp_resize = cv2.resize(image_data_temp,(self.IMAGE_SIZE,self.IMAGE_SIZE))
                        self.image_data.append([image_temp_resize,class_index])
                    except:
                        pass

            data = np.asanyarray(self.image_data)
            
            # Iterate over the Data
            for x in data:
                self.x_data.append(x[0])        # Get the X_Data
                self.y_data.append(x[1])        # get the label

            X_Data = np.asarray(self.x_data) / (255.0)      # Normalize Data
            Y_Data = np.asarray(self.y_data)

            # reshape x_Data

            X_Data = X_Data.reshape(-1, self.IMAGE_SIZE, self.IMAGE_SIZE, 1)

            return X_Data, Y_Data
        except:
            print("Failed to run Function Process Image ")

    def pickle_image(self):

        """
        :return: None Creates a Pickle Object of DataSet
        """
        # Call the Function and Get the Data
        X_Data,Y_Data = self.Process_Image()
        # Write the Entire Data into a Pickle File
        pickle_out = open('output/X_Data','wb')
        pickle.dump(X_Data, pickle_out)
        pickle_out.close()

        # Write the Y Label Data
        pickle_out = open('output/Y_Data', 'wb')
        pickle.dump(Y_Data, pickle_out)
        pickle_out.close()

        print("Pickled Image Successfully ")
        return X_Data,Y_Data

    def load_dataset(self):

        try:
            # Read the Data from Pickle Object
            X_Temp = open('output/X_Data','rb')
            X_Data = pickle.load(X_Temp)

            Y_Temp = open('output/Y_Data','rb')
            Y_Data = pickle.load(Y_Temp)

            print('Reading Dataset from PIckle Object')

            return X_Data,Y_Data

        except:
            print('Could not Found Pickle File ')
            print('Loading File and Dataset  ..........')

            X_Data,Y_Data = self.pickle_image()
            return X_Data,Y_Data


    


# In[ ]:


def tainMydata():
    path = 'Allimages'
    a = MasterImage(PATH=path,IMAGE_SIZE=80)

    X_Data,Y_Data = a.load_dataset()
    print(X_Data.shape)
    classes=[]
    for path in os.listdir("Allimages"):
        if '.DS_Store' in path:
            pass
        else:
            classes.append(path)
    catlen =len(classes)
    print(classes)
    print(catlen)
    
    # one-hot encoding using keras' numpy-related utilities
    n_classes = catlen
    print("Shape before one-hot encoding: ", X_Data.shape)
    X_train = np_utils.to_categorical(X_Data, n_classes)
    Y_test = np_utils.to_categorical(Y_Data, n_classes)
    print("Shape after one-hot encoding: ", X_train.shape)
    
    num_classes = catlen
    model = Sequential()
    model.add(Conv2D(filters=16, kernel_size=(5, 5), activation="relu", input_shape=(X_train.shape[1:])))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(filters=64, kernel_size=(5, 5), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(filters=64, kernel_size=(5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))
    model.summary()
    
    #model.compile(loss='binary_crossentropy',
    #optimizer=keras.optimizers.Adagrad(),
    #metrics=['accuracy'])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    #model.compile(optimizer=optimizers.RMSprop(lr=1e-4), loss='binary_crossentropy', metrics=['accuracy'])

    # history = model.fit(X_train, Y_train, epochs=30, validation_data=(X_val, Y_val), batch_size=64)
    history = model.fit(X_train, Y_test, batch_size=40, epochs=10, validation_split=0.3)
    model.save('Model_6c.h5')

    #tf.reset_default_graph()
    '''convnet = input_data((X_train.shape[1:]))
    convnet = conv_2d(convnet, 32, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)
    convnet = conv_2d(convnet, 64, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)
    convnet = conv_2d(convnet, 128, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)
    convnet = conv_2d(convnet, 64, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)
    convnet = conv_2d(convnet, 32, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)
    convnet = fully_connected(convnet, num_classes, activation='softmax')
    convnet = regression(convnet, optimizer='adam', learning_rate = 0.001, loss='categorical_crossentropy')
    model = tflearn.DNN(convnet, tensorboard_verbose=1)
    model.fit(X_train, Y_test, batch_size=40, n_epoch=12, validation_set=(X_train, Y_test), show_metric = True)
    #model.save(os.path.join("/model/my_model.tflearn"))
    tf.saved_model.save(model, "my_model.h5")'''
    #model.save("export/1")

    
    

