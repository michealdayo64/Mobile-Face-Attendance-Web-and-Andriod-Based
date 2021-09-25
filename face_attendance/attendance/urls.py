from django.urls import path
from attendance.views import (index, admin_profile, manageLecturer, addLecturer, addStudent, manageStudent, editStudent, lectureDashboard,
                                     addCourse, manageCourse, editCourse, viewAttendance, editLecturer, studentAddCourse, studentLoginToAddCourse, editLecturerProfile, manageSection, addSection,
                                        editSection, editLevel, manageLevel, addLevel, lecturerViewStudentAttendance, lecturerGetStudentAttendance, lecturerManageStudent, 
                                        studentDeleteCourse, deleteStudent, studentLoginToRemoveCourse
                                        )
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('index/', index, name = 'index'),
    path('admin_profile/<id>/', admin_profile, name = 'admin_profile'),
    path('manage_lecturer/', manageLecturer, name = 'manage_lecturer'),
    path('lecturer_index', lectureDashboard, name = 'lecturer_index'),
    path('add_lecturer/', addLecturer, name = 'add_lecturer'),
    path('edit_lecturer/<id>/', editLecturer, name = 'edit_lecturer'),
    path('add_student/', addStudent, name = 'add_student'),
    path('student_add_course/<id>', studentAddCourse, name = 'student_add_course'),
    path('manage_student/', manageStudent, name = 'manage_student'),
    path('edit_student/<id>/', editStudent, name = 'edit_student'),
    path('delete_student/<id>', deleteStudent, name = 'delete_student'),
    path('student_delete_course/<id>', studentDeleteCourse, name = 'student_delete_course'),
    path('student_login_add_course', studentLoginToAddCourse, name = 'student_login_add_course'),
    path('add_course/', addCourse, name = 'add_course'),
    path('manage_course/', manageCourse, name = 'manage_course'),
    path('edit_course/<id>', editCourse, name = 'edit_course'),
    path('add_session/', addSection, name = 'add_session'),
    path('manage_session/', manageSection, name = 'manage_session'),
    path('edit_session/<id>/', editSection, name = 'edit_session'),
    path('add_level', addLevel, name = 'add_level'),
    path('manage_level', manageLevel, name = 'manage_level'),
    path('edit_level/<id>', editLevel, name = 'edit_level'),
    path('view_attendance/', viewAttendance, name = 'view_attendance'),
    #path('get_attendance_date/', csrf_exempt(getAttendanceDate), name = 'get_attendance_date'),
    #path('get_attendance_student/', csrf_exempt(getAttendanceStudent), name = 'get_attendance_student'),
    path('edit_lecturer_profile/<id>/', editLecturerProfile, name = 'edit_lecturer_profile'),
    path('lecturer_manage_student/', lecturerManageStudent, name = 'lecturer_manage_student'),
    #path('lecturer_edit_student/<id>/', lecturerEditStudent, name = 'lecturer_edit_student'),
    path('lecturer_view_student_attendance/', lecturerViewStudentAttendance, name = 'lecturer_view_student_attendance'),
    path('lecturer_get_student_attendance/', csrf_exempt(lecturerGetStudentAttendance), name = 'lecturer_get_student_attendance'),
    path('student_login_remove_course/<id>/', studentLoginToRemoveCourse, name = 'student_login_remove_course'),
    #path('train_images/', trainImages, name='train_images')
]