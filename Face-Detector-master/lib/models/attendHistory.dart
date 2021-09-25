class Attend {
  List<AttList> attList;

  Attend({this.attList});

  Attend.fromJson(Map<String, dynamic> json) {
    if (json['att_list'] != null) {
      // ignore: deprecated_member_use
      attList = new List<AttList>();
      json['att_list'].forEach((v) {
        attList.add(new AttList.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    if (this.attList != null) {
      data['att_list'] = this.attList.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class AttList {
  int id;
  bool status;
  String created_at;
  StudentId studentId;

  AttList({this.id, this.status, this.created_at, this.studentId});

  AttList.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    status = json['status'];
    created_at = json['created_at'];
    studentId = json['student_id'] != null
        ? new StudentId.fromJson(json['student_id'])
        : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['status'] = this.status;
    if (this.studentId != null) {
      data['student_id'] = this.studentId.toJson();
    }
    return data;
  }
}

class StudentId {
  int id;
  String matricNo;
  String sex;
  String photo;
  Student student;
  List<CourseId> courseId;

  StudentId(
      {this.id,
      this.matricNo,
      this.sex,
      this.photo,
      this.student,
      this.courseId});

  StudentId.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    matricNo = json['matric_no'];
    sex = json['sex'];
    photo = json['photo'];
    student =
        json['student'] != null ? new Student.fromJson(json['student']) : null;
    if (json['course_id'] != null) {
      // ignore: deprecated_member_use
      courseId = new List<CourseId>();
      json['course_id'].forEach((v) {
        courseId.add(new CourseId.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['matric_no'] = this.matricNo;
    data['sex'] = this.sex;
    data['photo'] = this.photo;
    if (this.student != null) {
      data['student'] = this.student.toJson();
    }
    if (this.courseId != null) {
      data['course_id'] = this.courseId.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class Student {
  int id;
  String username;
  String email;
  String firstName;
  String lastName;

  Student({this.id, this.username, this.email, this.firstName, this.lastName});

  Student.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    username = json['username'];
    email = json['email'];
    firstName = json['first_name'];
    lastName = json['last_name'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['username'] = this.username;
    data['email'] = this.email;
    data['first_name'] = this.firstName;
    data['last_name'] = this.lastName;
    return data;
  }
}

class CourseId {
  int id;
  String courseCode;

  CourseId({this.id, this.courseCode});

  CourseId.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    courseCode = json['course_code'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['course_code'] = this.courseCode;
    return data;
  }
}
