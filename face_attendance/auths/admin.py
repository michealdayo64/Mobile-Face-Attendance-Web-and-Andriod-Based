from django.contrib import admin
from .models import Lecturer, Coursecode, Level, Students, AttendanceReport, CustomUser, AdminHOD, SessionYearModel
#from django.contrib.auth.admin import UserAdmin
# Register your models here.



admin.site.register(Lecturer)
admin.site.register(Coursecode)
admin.site.register(Level)
admin.site.register(Students)
admin.site.register(AttendanceReport)
admin.site.register(CustomUser)
admin.site.register(AdminHOD)
admin.site.register(SessionYearModel)