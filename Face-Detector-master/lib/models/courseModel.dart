class Course {
  List<Data> data;

  Course({this.data});

  Course.fromJson(Map<String, dynamic> json) {
    if (json['data'] != null) {
      // ignore: deprecated_member_use
      data = new List<Data>();
      json['data'].forEach((v) {
        data.add(new Data.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    if (this.data != null) {
      data['data'] = this.data.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class Data {
  int id;
  String courseCode;

  Data({this.id, this.courseCode});

  Data.fromJson(Map<String, dynamic> json) {
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

class CourseName {
  int id;
  String course_code;

  CourseName({this.id, this.course_code});
}
