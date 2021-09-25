from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.utils import timezone


# Create your models here.

class SessionYearModel(models.Model):
    session_start_year=models.DateField()
    session_end_year=models.DateField()

    def __str__(self):
        return str(self.session_start_year) + " - " + str(self.session_end_year)

class CustomUser(AbstractUser):
    user_type_data=(("1","HOD"),("2","Staff"),("3","Student"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class AdminHOD(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Lecturer(models.Model):
    lecturer = models.OneToOneField(CustomUser, on_delete = models.CASCADE, related_name='phoneNo')
    phone_num = models.CharField(max_length = 30, default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lecturer.username

class Coursecode(models.Model):
    lecturer_id = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null = True, related_name='lecturer_id')
    course_code = models.CharField(max_length = 10, unique = True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_code

class Level(models.Model):
    std_level = models.CharField(max_length = 10)
    
    def __str__(self):
        return self.std_level


class Students(models.Model):
    student = models.OneToOneField(CustomUser, on_delete = models.CASCADE, related_name='stud')
    matric_no = models.CharField(max_length = 20, default = False)
    course_id = models.ManyToManyField(Coursecode, related_name='cours')
    level_id = models.ForeignKey(Level, on_delete = models.CASCADE, null = True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE, null = True)
    sex = models.CharField(max_length = 20, default = '')
    photo = models.ImageField(upload_to = '', blank = True)
    photo2 = models.ImageField(upload_to = '', blank = True)
    photo3 = models.ImageField(upload_to = '', blank = True)
    photo4 = models.ImageField(upload_to = '', blank = True)
    photo5 = models.ImageField(upload_to = '', blank = True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    def __str__(self):
        return self.student.first_name +" "+ self.student.last_name

class AttendanceReport(models.Model):
    #student_id = models.CharField(max_length=200, null=True, blank=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING, default=False, related_name='student_att')
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Matric No: " + str(self.student_id.matric_no)

