from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
import numpy as np
import h5py
import os
import json
import pickle
import time
import datetime
#from keras.utils import to_categorical
from tensorflow.keras.utils import to_categorical
from keras.layers import Flatten
from keras.optimizers import SGD
from keras.layers import MaxPooling2D
from matplotlib import pyplot


def tainMydata():
    # config variables
    test_size     = 0.10
    model_name    = "vgg16"
    seed      = 9
    datatype="attendance"
    features_path   = "output/"+datatype +"/" + model_name + "/features.h5"
    labels_path   = "output/"+datatype +"/" + model_name + "/labels.h5"
    #results     = "output/"+datatype +"/" + model_name + "/results.txt"
    theclassifier_path = "output/"+datatype +"/" + model_name + "/classifiercnn.h5"
    #train_path    = "Allimages/"
    #num_classes   = 17

    # start time
    print ("[STATUS] start time - {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    start = time.time()

    # import features and labels
    h5f_data  = h5py.File(features_path, 'r')
    h5f_label = h5py.File(labels_path, 'r')

    features_string = h5f_data['dataset_1']
    labels_string   = h5f_label['dataset_1']

    features = np.array(features_string)
    labels   = np.array(labels_string)

    h5f_data.close()
    h5f_label.close()

    avg_accuracy = []
    avg_recall = []

    # verify the shape of features and labels
    print ("[INFO] features shape: {}".format(features.shape))
    print ("[INFO] labels shape: {}".format(labels.shape))

    print ("[INFO] training started...")
    # split the training and testing data
    (trainData, testData, trainLabels, testLabels) = train_test_split(np.array(features),
                                                                      np.array(labels),
                                                                      test_size=test_size,
                                                                      random_state=seed)

    X_train=trainData
    y_train=trainLabels 
    X_test=testData
    y_test=testLabels

    # Flattening the images from the 28x28 pixels to 1D 787 pixels
    X_train = X_train.reshape(X_train.shape[0], 64, 64, 1)
    X_test = X_test.reshape(X_test.shape[0], 64, 64, 1)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')

    # normalizing the data to help with the training
    X_train /= 255
    X_test /= 255

    # one-hot encoding using keras' numpy-related utilities
    n_classes = 36
    print("Shape before one-hot encoding: ", y_train.shape)
    Y_train = np_utils.to_categorical(y_train, n_classes)
    Y_test = np_utils.to_categorical(y_test, n_classes)
    print("Shape after one-hot encoding: ", Y_train.shape)

    # CNN train

    # building a linear stack of layers with the sequential model
    if(os.path.isfile(theclassifier_path)):
        model = load_model(theclassifier_path)
    else:
        model = Sequential()
        
        
        # convolutional layer
        model.add(Conv2D(50, kernel_size=(3,3), strides=(1,1), padding='same', activation='relu',input_shape=(64,64,1) ))
        #input_shape=(28, 28, 1)

        # convolutional layer
        model.add(Conv2D(75, kernel_size=(3,3), strides=(1,1), padding='same', activation='relu'))
        model.add(MaxPool2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(125, kernel_size=(3,3), strides=(1,1), padding='same', activation='relu'))
        model.add(MaxPool2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(125, kernel_size=(3,3), strides=(1,1), padding='same', activation='relu'))
        model.add(MaxPool2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        # flatten output of conv
        model.add(Flatten())

        # hidden layer
        model.add(Dense(500, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Dense(250, activation='relu'))
        model.add(Dropout(0.3))
        
        model.add(Dense(36, activation='softmax'))
        model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
        model.summary()
        
    model.fit(X_train, Y_train, batch_size=128, epochs=10, validation_data=(X_test, Y_test))
    print ("[INFO] saving model...")
    model.save(theclassifier_path)  # creates a HDF5 file 'my_model.h5'
    print ("[INFO] DONE saving model")






