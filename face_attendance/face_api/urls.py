from django.urls import path
from .views import (LecturerApi, LecturerRegister, LoginView, LogoutView, CoursecodeApi, LevelApi,
                     SessionyearApi, storeImages, takeAttendanceApi, attendanceHistory)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', csrf_exempt(LecturerRegister.as_view()), name = 'lecturer_register'),
    path('login/', csrf_exempt(LoginView.as_view()), name = 'login'),
    path('logout/', csrf_exempt(LogoutView.as_view()), name = 'api-logout'),
    path('course_api/', csrf_exempt(CoursecodeApi.as_view()), name='course_api'),
    path('level_api/', csrf_exempt(LevelApi.as_view()), name='level_api'),
    path('session_api/', csrf_exempt(SessionyearApi.as_view()), name='session_api'),
    path('lecturer-api/', csrf_exempt(LecturerApi.as_view()), name='lecturer-api'),
    path('store_images/', storeImages, name='store_images'),
    path('take_attendance/', takeAttendanceApi, name='take_attendance'),
    path('attendance_history/', attendanceHistory, name = 'attendance_history'),
    #path('attendance_history_detail/<id>/', AttendanceReportDetail.as_view(), name='attendance_history_detail'),
    #path('apiroot/', ApiRoot.as_view(), name='apiroot')
    
]