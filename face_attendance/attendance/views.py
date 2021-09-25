from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from auths.models import Lecturer, Students, Coursecode, Level, AttendanceReport, CustomUser, SessionYearModel
#from django.contrib.auth.models import User
from django.contrib import messages
from auths.forms import UserForm, LecturerForm
from django.core.files.storage import FileSystemStorage
import json
import base64
import requests
from rest_framework import status



#HOD DASHBOARD STARTS.....

@login_required
def index(request):
    lecture = Lecturer.objects.all().count()
    student = Students.objects.all().count()
    course = Coursecode.objects.all().count()
    level = Level.objects.all().count()

    

    #STUDENT CHART ANALYSIS
    courses = Coursecode.objects.all()
    courses_list = []
    students_in_each_course = []
    
    for cos in courses:
        students = Students.objects.filter(course_id = cos.id).count()
        courses_list.append(cos.course_code)
        students_in_each_course.append(students)

    context = {
        'courses_list': courses_list,
        'students_in_each_course': students_in_each_course,
        'lecture': lecture,
        'student': student,
        'course': course,
        'level': level
    }
    return render(request, 'index.html', context)

@login_required
def admin_profile(request, id):
    user=CustomUser.objects.get(id = id, user_type = "1")
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user.username = username
        user.email = email
        user.set_password = password
        user.save()
        messages.success(request, "Successfully Updated Profile")
        return redirect("index")

    return render(request,"attendance/hod/admin_profile.html", {'user': user})

@login_required
def manageLecturer(request):
    lecturer = Lecturer.objects.all()
    return render(request, 'attendance/hod/manage_lecturer.html', {'lecturer': lecturer})

@login_required    
def addLecturer(request):
    if request.method == "POST":
        user_form = UserForm(request.POST or None)
        lecturer_form = LecturerForm(request.POST or None)

        if user_form.is_valid() and lecturer_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.user_type = "2"
            user.save()

            lecturer = lecturer_form.save(commit = False)
            lecturer.lecturer = user
            lecturer.save()
            messages.success(request, 'Lecturer Details Added Successfully')
            return redirect("manage_lecturer")
            
        else:
            messages.info(request, user_form.errors)
    else:
        user_form = UserForm()
        lecturer_form = LecturerForm()

    context = {
            'user_form': user_form,
            'lecturer_form': lecturer_form
            }
    return render(request,"attendance/hod/add_lecturer.html")

@login_required
def editLecturer(request, id):
    
    user = CustomUser.objects.get(id = id)
    lect = Lecturer.objects.get(lecturer = user)
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        username = request.POST.get("username")
        phone = request.POST.get("phone_num")

        user.email = email
        user.password = password
        user.first_name = firstname
        user.last_name = lastname
        user.lecturer.username = username
        user.save()

        
        lect.phone_num = phone
        lect.save()
        messages.success(request, 'Lecturer Details Updated Successfully')
        return redirect("manage_lecturer")

    return render(request, 'attendance/hod/edit_lecturer.html', {'lect': lect})

@login_required
def addStudent(request):
    levels = Level.objects.all()
    sections = SessionYearModel.objects.all()
    if request.method == 'POST':
        username = request.POST.get("username")
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        password = request.POST.get("password")
        level = request.POST.get("level")
        session = request.POST.get("session")
        sex = request.POST.get("sex")
        photo = request.FILES["photo"]

        fs = FileSystemStorage()
        filename = fs.save(photo.name, photo)
        profile_pic_url = fs.url(filename)
        user = CustomUser.objects.create_user(username = username, first_name = firstname, last_name = lastname, user_type = "3")
        level_id = Level.objects.get(id = level)
        session_id = SessionYearModel.objects.get(id = session)
        student = Students(student = user, level_id = level_id, session_year_id = session_id, sex = sex, photo = profile_pic_url)
        student.save()
        messages.success(request, 'Students Details Added Successfully')
        return redirect('manage_student')
        
    context = {
        'levels': levels,
        'sections': sections
    }
    return render(request, 'attendance/hod/add_student.html', context)

@login_required
def manageStudent(request):
    students = Students.objects.all()

    return render(request, 'attendance/hod/manage_student.html', {'students': students})

@login_required
def editStudent(request, id):
    user = CustomUser.objects.get(id = id) 
    student = get_object_or_404(Students, student = user)
    levels = Level.objects.all()
    sections = SessionYearModel.objects.all()
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        password = request.POST.get("password")
        level = request.POST.get("level")
        sex = request.POST.get("sex")
        photo = request.FILES.get("photo")
        session = request.POST.get("session")

        fs = FileSystemStorage()
        filename = fs.save(photo.name, photo)
        profile_pic_url = fs.url(filename)

        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.password = password
        user.save()
        
        level_id = Level.objects.get(id = level)
        session_id = SessionYearModel.objects.get(id = session)
        #session_id2 = SessionYearModel.objects.get(id = session2)
        student.level_id = level_id
        student.session_year_id = session_id
        #student.session_year_id.session_end_year = session_id2
        student.sex = sex
        student.photo = profile_pic_url
        student.save()
        messages.success(request, 'Students Details Updated Successfully')
        return redirect("manage_student")
    context = {
           'student': student,
           'levels': levels,
           'sections': sections
    }
    return render(request, 'attendance/hod/edit_student.html', context)

def deleteStudent(request, id):
    student = get_object_or_404(Students, id = id)
    student.delete()
    return redirect("manage_student")

@login_required
def studentAddCourse(request, id):
    student = get_object_or_404(Students, id = id)
    courses = Coursecode.objects.all()
    #student_course = Coursecode.objects.filter()
    if request.method == "POST":
        course = request.POST.get("course")

        course_id = Coursecode.objects.get(id = course)
        student.course_id.add(course_id)
        student.save()
        messages.success(request, "Course Added Successfully")
        return redirect("student_add_course", id = id)
    
    return render(request, 'attendance/hod/student_add_course.html', {'courses': courses, 'student': student})



def studentDeleteCourse(request, id):
    course = Coursecode.objects.get(id = id)
    student = Students.objects.get(course_id = course)
    student.course_id.remove(course)
    messages.success(request, "Course Deleted Sucessfully")
    return redirect("student_add_course", id = id)

@login_required
def addCourse(request):
    lecturers = CustomUser.objects.filter(user_type = "2")
    if request.method == "POST":
        lecturer_id = request.POST.get("lecturer")
        course = request.POST.get('course')

        lecturer = CustomUser.objects.get(id = lecturer_id)
        Coursecode.objects.create(course_code = course, lecturer_id = lecturer)
        return redirect("manage_course")
    return render(request, 'attendance/hod/add_course.html', {'lecturers': lecturers})

@login_required
def manageCourse(request):
    manage_course = Coursecode.objects.all()
    return render(request, 'attendance/hod/manage_course.html', {'manage_course': manage_course})

@login_required
def editCourse(request, id):
    lecturers = CustomUser.objects.filter(user_type = "2")
    course = Coursecode.objects.get(id = id)
    if request.method == 'POST':
        lecturer_id = request.POST.get("lecturer")
        getCourse = request.POST.get('course')

        lecturer = CustomUser.objects.get(id = lecturer_id)
        course.lecturer_id = lecturer
        course.course_code = getCourse
        course.save()
        return redirect("manage_course")
    return render(request, 'attendance/hod/edit_course.html', {'course': course, 'lecturers': lecturers })

@login_required
def addSection(request):
    if request.method == 'POST':
        session_start_year = request.POST.get('session_start')
        session_end_year = request.POST.get('session_end')
        SessionYearModel.objects.create(session_start_year = session_start_year, session_end_year = session_end_year)
        return redirect("manage_session")
    return render(request, 'attendance/hod/add_session.html')

@login_required
def manageSection(request):
    sections = SessionYearModel.objects.all()
    return render(request, 'attendance/hod/manage_session.html', {'sections': sections})

def editSection(request, id):
    section = SessionYearModel.objects.get(id = id)
    if request.method == "POST":
        session_start_year = request.POST.get('session_start')
        session_end_year = request.POST.get('session_end')

        section.session_start_year = session_start_year
        section.session_end_year = session_end_year
        section.save()
        messages.success(request, 'Date Updated Successfully')
        return redirect("manage_session")
    return render(request, 'attendance/hod/edit_session.html', {"section": section})

@login_required
def addLevel(request):
    if request.method == 'POST':
        level = request.POST.get('level')
       
        Level.objects.create(std_level = level)
        return redirect("manage_level")
    return render(request, 'attendance/hod/add_level.html')

@login_required
def manageLevel(request):
    levels = Level.objects.all()
    return render(request, 'attendance/hod/manage_level.html', {'levels': levels})

@login_required
def editLevel(request, id):
    levels = Level.objects.get(id = id)
    if request.method == 'POST':
        level = request.POST.get('level')
       
        levels.std_level = level
        levels.save()
        return redirect("manage_level")
    return render(request, 'attendance/hod/edit_level.html', {'levels': levels})

@login_required
def viewAttendance(request):
    levels = Level.objects.all()
    courses = Coursecode.objects.all()
    attReport = AttendanceReport.objects.all().order_by('-created_at')
    return render(request, 'attendance/hod/view_attendance.html', {'levels': levels, 'courses': courses, 'attReport': attReport})



'''def getAttendanceDate(request):
    course_id=request.POST.get("courseText")
    level_id=request.POST.get("levelText")

    course_obj=get_object_or_404(Coursecode, id=course_id) 
    level_obj =Level.objects.get(id=level_id)

    attendance=Attendance.objects.filter(course_id=course_obj,level_id=level_obj)
    attendance_obj=[]

    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"level_id":attendance_single.level_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)'''


'''def getAttendanceStudent(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.id,"name":student.student_id.student.first_name+" "+student.student_id.student.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)'''

#HOD DASHBOAD ENDS...

#LECTURER DASHBOARD
def lectureDashboard(request):
    #For Fetch All Student Under Staff
    courses = Coursecode.objects.filter(lecturer_id = request.user.id)
    print(courses)
    final_course = []
    for course in courses:
        if course not in final_course:
            final_course.append(course.id)
    print(final_course)
    student = Students.objects.filter(course_id__in = final_course).count()
    
    #attendance_count=Attendance.objects.filter(course_id__in=courses).count()

    students_attendance = Students.objects.filter(course_id__in = final_course)
    attendance_list = []
    for std in students_attendance:
        if std not in attendance_list:
            attendance_list.append(std.id)
        
    present = AttendanceReport.objects.filter(status = True, student_id__in = attendance_list).count()
    absent = AttendanceReport.objects.filter(status = False, student_id__in = attendance_list).count()
    
    context = {'student_count': student, 
                #'attendance_count': attendance_count,
                'present': present,
                'absent': absent }
    return render(request, 'attendance/lecturer/lecturer_index.html', context)

@login_required
def lecturerManageStudent(request):
    courses = Coursecode.objects.filter(lecturer_id = request.user.id)
    print(courses)
    final_course = []
    for course in courses:
        if course not in final_course:
            final_course.append(course.id)
    students = Students.objects.filter(course_id__in = final_course)
    #print(students)
    return render(request, 'attendance/lecturer/manage_student.html', {'students': students})

'''@login_required
def lecturerEditStudent(request, id):
    courses = Coursecode.objects.filter(lecturer_id = request.user.id)
    print(courses)
    final_course = []
    for course in courses:
        if course not in final_course:
            final_course.append(course.id)
    student = Students.objects.get(course_id = final_course.id)
    sections = SessionYearModel.objects.all()
    levels = Level.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        section = request.POST.get('session')
        level = request.POST.get('level')
        sex = request.POST.get('sex')

        section_id = SessionYearModel.objects.get(id = section)
        level_id = Level.get.objects.get(id = level)
        student.student.username = username
        student.student.first_name = firstname
        student.student.last_name = lastname
        student.session_year_id = section_id
        student.level_id = level_id
        student.sex = sex
        student.save()
        messages.success(request, 'Updated successful')
        return redirect("lecturer_manage_student")
    context = {
        'student':student,
        'sections': sections,
        'levels': levels
    }
    return render(request, 'attendance/lecturer/edit_student.html', context)'''


def editLecturerProfile(request, id):
    user = CustomUser.objects.get(id = request.user.id)
    lecturer = Lecturer.objects.get(lecturer = user.id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user.username = username
        user.email = email
        user.first_name = firstname
        user.last_name = lastname
        user.password = password
        user.save()

        lecturer.phone_num = phone
        lecturer.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect('lecturer_index')
    return render(request, 'attendance/lecturer/edit_profile.html', {'user': user, 'lecturer': lecturer })

def lecturerViewStudentAttendance(request):
    courses = Coursecode.objects.filter(lecturer_id = request.user.id)
    session_years = SessionYearModel.objects.all()
    levels = Level.objects.all()
    final_course = []
    for course in courses:
        if course not in final_course:
            final_course.append(course.id)

    allStudent = Students.objects.filter(course_id__in = final_course)
    attendance_list = []
    for std in allStudent:
        if std not in attendance_list:
            attendance_list.append(std.id)
    attendance = AttendanceReport.objects.filter(student_id__in = attendance_list)
    context = {
                "courses":courses, 
                "session_years":session_years, 
                'levels': levels, 
                'attendance': attendance
                }

    return render(request,"attendance/lecturer/view_attendance.html", context)


def lecturerGetStudentAttendance(request):
    course_id = request.POST.get('courseText')
    session_id = request.POST.get('sessionText')
    level_id = request.POST.get('levelText')

    course = Coursecode.objects.get(id = course_id)
    session = SessionYearModel.objects.get(id = session_id)
    level = Level.objects.get(id = level_id)

    attendance = Attendance.objects.filter(course_id = course, session_year_id = session, level_id = level)
    attendance_report = AttendanceReport.objects.filter(attendance_id__in = attendance)
    print(attendance_report)
    student_obj = []
    for student in attendance_report:
        data = {
            'id': student.id, 
            'name': student.student_id.student.first_name+ " " +student.student_id.student.last_name,  
            'course': student.attendance_id.course_id.course_code,
            'level': student.attendance_id.level_id.std_level,
            'date': str(student.attendance_id.attendance_date),
            'status': student.status,
            'matric_no': student.student_id.matric_no
        }
        student_obj.append(data)

    return JsonResponse(json.dumps(student_obj),safe=False)


#STUDENT ADD COURSE
@login_required
def studentLoginToAddCourse(request):
    student = get_object_or_404(Students, student = request.user)
    courses = Coursecode.objects.all()
    #student_course = Coursecode.objects.filter()
    if request.method == "POST":
        course = request.POST.get("course")

        course_id = Coursecode.objects.get(id = course)
        student.course_id.add(course_id)
        student.save()
        messages.success(request, "Course Added Successfully")
        return redirect("student_login_add_course")
    return render(request, 'attendance/student/student_index.html', {'student': student, 'courses': courses })

@login_required
def studentLoginToRemoveCourse(request, id):
    student = get_object_or_404(Students, student = request.user)
    course = Coursecode.objects.get(id = id)
    student.course_id.remove(course)
    messages.success(request, "Course Removed Successfully")
    return redirect("student_login_add_course")





