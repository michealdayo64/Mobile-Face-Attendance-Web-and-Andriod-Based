from django.urls import path
from auths.views import StudentEnroll, userLogin, LecturerSignup, userLogout, adminSignup, trainDataset, takePicture
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('', userLogin, name = 'user_login'),
    path('logout/', userLogout, name = 'logout'),
    path('student-signup/', csrf_exempt(StudentEnroll), name = 'student_enroll'),
    #path('student_id/<id>', StudentId, name = 'student_id'),
    path('lecturer-signup/', LecturerSignup, name = 'lecturer_signup'),
    path('admin_signup/', adminSignup, name = 'admin_signup'),
    path('train_data_set/', trainDataset, name='train_data_set'),
    path('take_pic/', takePicture, name = 'take_pic')
    
]