import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from keras.utils import np_utils
import os
import cv2
import shutil
from keras.preprocessing import image
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
import pickle
import datetime
from keras.models import model_from_yaml
from keras.applications.resnet50 import preprocess_input


face_cascade = cv2.CascadeClassifier('C:\\Users\\Mikky\\Documents\\mydjango\\face_project\\venv\\Face_Project\\face_attendance\\haarcascades\\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C:\\Users\\Mikky\\Documents\\mydjango\\face_project\\venv\\Face_Project\\face_attendance\\haarcascades\\haarcascade_eye.xml')



def cropped_image_for_2_eyes(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            return roi_color

def mmm():
    cropped_data_path = "Crop/cropped_images"
    img_dir = "Allimages"
    celebrity_file_names_dict = {}
    cropped_img_dirs = []
    
    img_dirs = []
    file_list = []
    for entry in os.scandir(img_dir):
        if entry.is_dir():
            img_dirs.append(entry.path)
    #print(img_dirs)

    for img_dir in img_dirs:           #Selecting celebrity folders after each and every iteration 
        count = 1
        celebrity_name = img_dir.split('\\')[-1]
        #print(celebrity_name)

        celebrity_file_names_dict[celebrity_name] = []
    
        for entry in os.scandir(img_dir):        #Scanning images inside the current celebrity folder
            roi_color = cropped_image_for_2_eyes(entry.path)
            if roi_color is not None:   #If cropped image is returned store it in cropped folder with celebrity name at it's back
                cropped_folder = cropped_data_path + celebrity_name
                if not os.path.exists(cropped_folder):    #If cropped folder does not exist create it
                    os.makedirs(cropped_folder)
                    cropped_img_dirs.append(cropped_folder)   #Adding cropped celebrity images folder in list
                    print("Generating cropped images in folder: ",cropped_folder)
                cropped_file_name = celebrity_name + str(count) + ".png"  #Name of cropped file stored inside cropped celebrity folder
                cropped_file_path = cropped_folder + "/" + cropped_file_name #Path of cropped image file stored inside cropped celebrity folder
                
                cv2.imwrite(cropped_file_path,roi_color)       #adding cropped files inside cropped celebrity folder
                celebrity_file_names_dict[celebrity_name].append(cropped_file_path) #Creating dictionary of celebrity name as key and their cropped images as value
                count+=1

        #print(cropped_img_dirs)

    for img_dir in cropped_img_dirs:
        celebrity_name = img_dir.split('/')[-1]
        file_list = []
        for entry in os.scandir(img_dir):
            file_list.append(entry.path)
        celebrity_file_names_dict[celebrity_name] = file_list
    #print(celebrity_file_names_dict)

    num_dict = {}
    count = 0
    for celebrity_name in celebrity_file_names_dict.keys():
        num_dict[celebrity_name] = count
        count = count + 1
    #print(num_dict)

    X = []
    y = []

    for celebrity_name, training_files in celebrity_file_names_dict.items():
        for training_image in training_files:
            img = cv2.imread(training_image)
            #img = cv2.cvtColor( img,cv2.COLOR_RGB2GRAY )
            scaled_raw_img = cv2.resize(img,(224,224))
    #         print(scaled_raw_img.shape)
            X.append(scaled_raw_img)
            y.append(num_dict[celebrity_name])

    print(len(X))
    print(len(y))

    print(X)

    len(X[0])
    X = np.array(X)
    print(X.shape)

    num_classes = len(num_dict)
    input_shape = (224, 224, 3)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    X_dup_test = X_test
    total_test_img = len(X_dup_test)

    X_train = X_train.astype("float32") / 255
    X_test = X_test.astype("float32") / 255
    # X_train = X_train.reshape((X_train.shape[0]*224*224*3))
    # X_test = X_test.reshape((X_test.shape[0]*224*224*3))

    print("x_train shape:", X_train.shape)
    print(X_train.shape[0], "train samples")
    print(X_test.shape[0], "test samples")

    print("Shape of X_test", X_test.shape)
    print("Shape of X_train", X_train.shape)

    # convert class vectors to binary class matrices

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    print(y_train.shape)
    print(y_test.shape)

    model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ]
)
    model.summary()
    model.save('model.h5')
    #from tensorflow.keras.models import load_model
    model = load_model('model.h5')
    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    score = model.evaluate(X_train, y_train, verbose=0)
    print("Train loss:", score[0])
    print("Train accuracy:", score[1])

    score = model.evaluate(X_train, y_train, verbose=0)
    print("Train loss:", score[0])
    print("Train accuracy:", score[1])

    predictions = model.predict(X_test)
    type(predictions)
    #loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    #loss="categorical_crossentropy",

    def unique(list1): 
        list_set = set(list1) 
        unique_list = (list(list_set)) 
        return unique_list

    pred_list = []
    val_list = list(num_dict.values()) 
    key_list = list(num_dict.keys())
    for i in range(total_test_img):
        pred_list.append(key_list[val_list.index(np.argmax(predictions[i]))])
    unique_val = unique(pred_list) 
    print(unique_val)
    

def takeAttendance():
    model_path=os.path.join("model.h5")
    model = load_model(model_path)
    test_path="take_attendance" + "/" + "1788621215.png"
    img=cv2.imread(test_path)  # where f_path is the path to the image file
    img=cv2.resize(img, (32,32), interpolation = cv2.INTER_AREA)  
    img=img/255
    
    predictions=model.predict(img)
    pre_class=predictions.argmax()
    print(pre_class)
    '''print(len(attend))

    attend = np.array(attend)
    print(attend.shape)

    X_train, X_test, y_train, y_test = train_test_split(attend, test_size=0.1, random_state=0)
    X_dup_test = X_test
    total_test_img = len(X_dup_test)

    model = load_model('model.h5')

    predictions = model.predict(X_test)
    type(predictions)'''

    

    

        
        

    '''for i in attend:
        cel = i.split('\\')[-1]
        print(cel)'''
        





 
   

'''def get_categories():
    list_categories=[]
    for path in os.listdir('Allimages/'):
        if '.DS_Store' in path:
            pass
        else:
            list_categories.append(path)
    print("Found Categories ",list_categories,'\n')
    return list_categories


def takeAttendance(atended):
    #file_path = os.path.join(settings.BASE_DIR, 'take_attendance/')
    test_path="take_attendance" + "/" + "image_0001_Face_1.jpg"
    
    model_path=os.path.join("model.h5")
    model = load_model(model_path) 
    dimage = image.load_img(test_path,True,target_size=(80,80, 1))
    img = np.expand_dims(dimage, axis=0)
    img = image.img_to_array(img)
    img_preprocessed = preprocess_input(img)
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
        if(prob[0][top_3[i]]>=0.6):
            atended.append({"name":classes[top_3[i]]})
    plt.imshow(dimage)
    print(alldatacount)
    print(atended)
    return atended'''
