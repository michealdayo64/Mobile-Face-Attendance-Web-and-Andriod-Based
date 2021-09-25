from rest_framework import serializers
from auths.models import CustomUser, Coursecode, Lecturer, Level, SessionYearModel, Students, AttendanceReport



class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = [
            'id',
            'phone_num'
        ]

class CustomUserSerializer(serializers.ModelSerializer):
    #phoneNo = LecturerSerializer(many = True)
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name'
        ]


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ('email',)


class CourseCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coursecode
        fields = [
            'id',
            'course_code'
        ]

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = [
            'id',
            'std_level'
        ]

class SessionYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionYearModel
        fields = [
            'id',
            'session_start_year',
            'session_end_year'
        ]

class StudentSerializer(serializers.ModelSerializer):
    student = CustomUserSerializer(many = False)
    course_id = CourseCodeSerializer(many = True, read_only = True)
    #course_id = serializers.SlugRelatedField(queryset = Coursecode.objects.all(), slug_field = 'created_at')
    class Meta:
        model = Students
        fields = [
            'id',
            'matric_no',
            'sex',
            'photo',
            'student',
            'course_id'
        ]

class AttendanceReportSerializer(serializers.ModelSerializer):
    #student_id = serializers.SlugRelatedField(queryset = Students.objects.all(), slug_field = 'matric_no')
    student_id = StudentSerializer(many = False)
    class Meta:
        model = AttendanceReport
        fields = [
            'id',
            'status',
            'created_at',
            'student_id'
        ]