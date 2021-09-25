import base64
import requests
from django.conf import settings
from face_api.views import LevelApi
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserForm, LecturerForm
from .models import Coursecode, Level, Students, CustomUser, SessionYearModel
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.authtoken.models import Token
#from face_api.serializers import StudentImageSerializer
from rest_framework.response import Response
from rest_framework import status
import os
import json
#import extract as cnnExtract
import newtrain as trainCnn
#import realpredict as pred
#import newpredict as pred
import correct_train as oo
import cv2
import sys

#pred.takeAttendance()


def takePicture(request):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    # grab the reference to the webcam
    vs = cv2.VideoCapture(0)

    # keep looping
    while True:
        # grab the current frame
        ret, frame = vs.read()
    
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if frame is None:
            break
        faces = faceCascade.detectMultiScale(frame)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)

        # show the frame to our screen
        cv2.imshow("Video", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' or ESC key is pressed, stop the loop
        if key == ord("q") or key == 27:
            break

    #close all windows
    cv2.destroyAllWindows()
    return redirect('user_login')


#STUDENT REGISTRATION
def StudentEnroll(request):
    
    levels = Level.objects.all()#LIST LEVELS
    sections = SessionYearModel.objects.all()#LIST SECCTIONS
    if request.method == 'POST':
        #Django Post
        username = request.POST.get("username")
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        matric_no = request.POST.get("mat_no")
        password = request.POST.get("password")
        level = request.POST.get("std_level")
        session = request.POST.get("session")
        sex = request.POST.get("sex")
        photo = request.FILES["photo"]
        if photo == None:
            return messages.info(request, "Need to fill in all photos")
        photo2 = request.FILES["photo2"]
        photo3 = request.FILES["photo3"]
        photo4 = request.FILES["photo4"]
        photo5 = request.FILES["photo5"]
       
        #CREATE STUDENT USER
        user = CustomUser.objects.create_user(username = username, first_name = firstname, last_name = lastname, password = password, user_type = "3")
        
        level_id = Level.objects.get(id = level)#GOTTON ID FOR LEVEL FROM POST
        session_id = SessionYearModel.objects.get(id = session)#GOTTEN ID FROM SESSION

        #CREATE STUDENT
        student = Students(student = user, level_id = level_id, session_year_id = session_id, sex = sex, matric_no = matric_no,
         photo = photo, photo2 = photo2, photo3 = photo3, photo4 = photo4, photo5 = photo5)
        student.save()
        messages.success(request, 'Students Details Added Successfully')
        
        image_name_list = []
        image_encode_list = []
        userMatric = student.matric_no

        #ENCODE STUDENT IMAGES TO BASE64 AND APPEND TO A LIST
        img1 = base64.b64encode(student.photo.file.read())
        image_encode_list.append(img1.decode("utf-8"))
        img2 = base64.b64encode(student.photo2.file.read())
        image_encode_list.append(img2.decode("utf-8"))
        img3 = base64.b64encode(student.photo3.file.read())
        image_encode_list.append(img3.decode("utf-8"))
        img4 = base64.b64encode(student.photo4.file.read())
        image_encode_list.append(img4.decode("utf-8"))
        img5 = base64.b64encode(student.photo5.file.read())
        image_encode_list.append(img5.decode("utf-8"))

        #GET 
        imgName1 = photo
        image_name_list.append(imgName1.name)
        imgName2 = photo2
        image_name_list.append(imgName2.name)
        imgName3 = photo3
        image_name_list.append(imgName3.name)
        imgName4 = photo4
        image_name_list.append(imgName4.name)
        imgName5 = photo5
        image_name_list.append(imgName5.name)

        userData = {
            'imagebase64': image_encode_list,
            'imagename': image_name_list,
            'uname': userMatric
        }

        url = "http://127.0.0.1:8000/faceApi/store_images/"
        
        r = requests.post(url,
                    data= json.dumps(userData),
                    headers={'Content-Type': 'application/json'})
        
        if r.status_code == 200:
            data = r.json()
            #cnnExtract.extract_all_data()
            #trainCnn.tainMydata()
            return JsonResponse(data, status = status.HTTP_200_OK)
            
        return redirect('user_login')
    
    context = {
        'levels': levels,
        'sections': sections,
        #'messages': messages
    }
        
    return render(request, 'authentication/student_signup.html', context)

def trainDataset(request):
    trainCnn.tainMydata()
    #oo.mmm()
    #oo.takeAttendance()
    return redirect('index')
    

#LECTURER REGISTRATION
def LecturerSignup(request):
    if request.method == "POST":
        user_form = UserForm(request.POST or None)
        lecturer_form = LecturerForm(request.POST or None)

        if user_form.is_valid() and lecturer_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.user_type = "2"
            user.save()

            #LECTURER TOKEN GENERATION
            Token.objects.create(user = user)

            lecturer = lecturer_form.save(commit = False)
            lecturer.lecturer = user
            lecturer.save()
            messages.success(request, 'Lecturer Details Added Successfully')
            return redirect("user_login")
        else:
            messages.info(request, user_form.errors)
    else:
        user_form = UserForm()
        lecturer_form = LecturerForm()
    return render(request, 'authentication/lecturer_signup.html')

#ADMIN OR HOD REGISTRATION
def adminSignup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST or None)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.user_type = "1"
            user.is_staff = True
            user.save()
            messages.success(request,"Successfully Created Admin")
            return redirect("user_login")
        else:
            messages.info(request,"Failed to Create Admin")
            return redirect("admin_signup")
    return render(request, 'authentication/admin_signup.html')

#ADMIN, LECTURER, STIDENT LOGIN
def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user:
            #REDIRECT TO ADMIN OR HOD DASHBOARD PAGE
            if user.is_active and user.user_type == "1" and user.is_staff:
                login(request, user)
                messages.success(request, "Login Successfully")
                return redirect("index")
            #REDIRECT TO LECTURER DASHBOARD PAGE              
            if user.is_active and user.user_type == "2":
                login(request, user)
                messages.success(request, "Login Successfully")
                return redirect("lecturer_index")
            #REDIRECT TO STUDENT DASHBOARD PAGE
            if user.is_active and user.user_type == "3":
                login(request, user)
                messages.success(request, "Login Successfully")
                return redirect("student_login_add_course") 
        else:
            #print("Someone tried to login and failed")
            #print("username:{} and password:{}".format(username,password))
            messages.info(request, "Invalid Details")
            return redirect("user_login")
    return render(request, 'authentication/login.html')

#ADMIN, LECTURER, STIDENT LOGOUT
@login_required
def userLogout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect("user_login")
    

