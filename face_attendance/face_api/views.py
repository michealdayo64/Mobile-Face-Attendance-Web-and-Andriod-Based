import json
from django.http.response import JsonResponse
from django.shortcuts import render
from .serializers import AttendanceReportSerializer, CourseCodeSerializer, CustomUserSerializer, ForgotPasswordSerializer, LecturerSerializer, LevelSerializer, SessionYearSerializer
from rest_framework.views import APIView
from auths.models import Coursecode, Lecturer, CustomUser, Level, SessionYearModel, Students, AttendanceReport
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import random
import os
import base64
from django.contrib.auth.hashers import make_password
from glob import glob
import newpredict as pred
from datetime import date

#import newtrain as ko
#import correct_train as pred
# Create your views here.



class LecturerRegister(APIView):
    def get(self, request):
        userLecturer = CustomUser.objects.filter(user_type = "2")
        serializers = CustomUserSerializer(userLecturer, many = True)
        return Response(serializers.data, status = status.HTTP_200_OK)

    def post(self, request):
        userLecturer = CustomUserSerializer(data = request.data or None)
        phone_num = request.data['phone_no']
        if userLecturer.is_valid():
            user = userLecturer.save()
            user.set_password(user.password)
            user.user_type = "2"
            user.save()
            Token.objects.create(user = user)
            Lecturer.objects.create(lecturer = user, phone_num = phone_num)
            data = {
                'Success': True,
            }
            return Response(data, status = status.HTTP_200_OK)
        data = {
            'Error': False,
        }
        return Response(data, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request,):
        username = self.request.data.get("username")
        password = self.request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active and user.user_type == '2':
                login(request, user)
                data = {
                    "token": user.auth_token.key, 
                    "success": "Login Successfully"
                    }
                return Response(data = data, status = status.HTTP_200_OK)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
            logout(request)
            data = {'success': 'success loggout'}
            return Response(data = data, status = status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # Generating Random Password of specific Type or use according to your need
        str_1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
        str_2 = ['!', '@', '#', '$', '%', '&', '*', '/', '-', '+']
        str_3 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        str = random.choice(str_1)
        for s in range(4):
            str += random.choice(str_1).lower()
        str += random.choice(str_2)
        for x in range(2):
            str += random.choice(str_3)

        password = make_password(str)

        if serializer.is_valid():
            email = request.data['email']
            print(email)
            CustomUser.objects.filter(email=email).update(password=password)

            subject = 'Forgot Password Request'
            message = 'Your request for Forgot Password has been received, your new password is ' + str
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(
                subject,
                message,
                email_from,
                recipient_list,
                fail_silently=False,
            )
            return Response({'msg': 'done'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Not a valid request'}, status=status.HTTP_400_BAD_REQUEST)

class LecturerApi(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        lecturer = Lecturer.objects.all()
        serializers = LecturerSerializer(lecturer, many = True)
        return Response(serializers.data, status = status.HTTP_200_OK)

class CoursecodeApi(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        course_code = Coursecode.objects.filter(lecturer_id = request.user.id)
        serializers = CourseCodeSerializer(course_code, many = True)
        return Response({"data": serializers.data}, status = status.HTTP_200_OK)


class LevelApi(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        level = Level.objects.all()
        serializers = LevelSerializer(level, many = True)
        return Response({'data':serializers.data}, status = status.HTTP_200_OK)


class SessionyearApi(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        session_year = SessionYearModel.objects.all()
        serializers = SessionYearSerializer(session_year, many = True)
        return Response({"data":serializers.data}, status = status.HTTP_200_OK)


@api_view(['POST', 'GET',])
@permission_classes((IsAuthenticated,))
def takeAttendanceApi(request):
    if request.method == "POST":
        course_id = request.data['courseIdValue']
        level_id = request.data['levelIdValue']
        session_id = request.data['sessionIdValue']
        image_enc = request.data['imageEnc']
        image_name = request.data['imageName']
        
        # ADD IMAGE TO TAKE ATTENDANCE FOLDER
        attendloc = 'take_attendance' + '/'
        with open(f"{attendloc}{image_name}", "wb") as fh:
            fh.write(base64.b64decode(image_enc)) 
        
        #PREDICT IMAGE
        li = []
        preData = []
        jjjj = pred.takeAttendance(preData)
        print(jjjj[0].get('name'))
        for i in jjjj:
            li.append(i.get('name'))
        print(li)
        courseId = Coursecode.objects.get(id = course_id)
        levelId = Level.objects.get(id = level_id)
        sessionId = SessionYearModel.objects.get(id = session_id)

        students=Students.objects.filter(course_id=courseId, session_year_id=sessionId, level_id = levelId)

        for i in students:
            if i.matric_no in li:
                stud = Students.objects.get(id = i.id)
                AttendanceReport.objects.create(student_id = stud, status = True)
            else:
                stud = Students.objects.get(id = i.id)          
                AttendanceReport.objects.create(student_id = stud, status = False)

        test_path="take_attendance"
        for f in os.listdir(test_path):
            os.remove(os.path.join(test_path, f))
        data = {
            'Success': True
        }
        return Response(data, status = status.HTTP_200_OK)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def attendanceHistory(request):
    courses = Coursecode.objects.filter(lecturer_id = request.user.id)
    final_course = []
    for course in courses:
        if course not in final_course:
            final_course.append(course.id)
    students = Students.objects.filter(course_id__in = final_course)

    final_studentId = []
    for student in students:
        if student not in final_studentId:
            final_studentId.append(student.id)

    today = date.today()
    att = AttendanceReport.objects.filter(student_id__in = final_studentId, created_at__day = today.day)
    serializer = AttendanceReportSerializer(att, many = True, context = {'request': request})
    data = {
        'att_list': serializer.data,
    }
    return Response(data = data, status = status.HTTP_200_OK)



test_path="AllImages"
def saveTheImage(imagelocation,imagename,username,imagebase64): 

    mainloc =imagelocation + "/" + str(username) + "/"
    if not os.path.exists(mainloc):
            os.makedirs(mainloc)

    '''files = glob(mainloc)
    for f in files:
        os.remove(f)'''

    totallen=len(imagebase64)
    for i in range(0,totallen):
        u=1
        with open(f"{mainloc}{u}{imagename[i]}", "wb") as fh:
            fh.write(base64.b64decode(imagebase64[i])) #decodebytes
        u=u+1


@api_view(['POST',])
@permission_classes((AllowAny,))
def storeImages(request):
    data = {} # dictionary to store result 
    data["status"] = False
    if request.method == "POST": 
        if request.data['imagebase64'] and  request.data['imagename']:
            imagename=request.data['imagename']
            imagebase64=request.data['imagebase64']
            username =request.data['uname']
            imagestorage=test_path+"/"
            saveTheImage(imagestorage,imagename,username,imagebase64)
            
            data["status"] = True

    # return JSON response 
    return Response(data = data, status = status.HTTP_200_OK)


    