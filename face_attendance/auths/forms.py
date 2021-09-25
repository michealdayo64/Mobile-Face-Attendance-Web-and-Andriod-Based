import uuid
from django import forms
from django.conf import settings
from django.db import models
from django.db.models import fields
#from django.contrib.auth.models import CustomUser
from .models import Coursecode, Lecturer, CustomUser, Level, SessionYearModel, Students
import base64
import os


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

class LecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ('phone_num',)





class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = [
            'sex', 'photo'
        ]

class SessionForm(forms.ModelForm):
    class Meta:
        model = SessionYearModel
        fields = [
            'session_start_year', 'session_end_year'
        ]

class CourseForm(forms.ModelForm):
    class Meta:
        model = Coursecode
        fields = [
            'course_code'
        ]

class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = [
            'std_level'
        ]