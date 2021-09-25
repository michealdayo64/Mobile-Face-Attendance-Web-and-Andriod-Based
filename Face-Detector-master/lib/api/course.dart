//import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_face_detection/models/courseModel.dart';
import 'package:localstorage/localstorage.dart';
import 'package:http/http.dart' as http;
//import 'dart:async';
import 'dart:convert';

LocalStorage storage = new LocalStorage("userToken");

Future<Course> fetchCourses() async {
  String url = 'http://192.168.43.80:8080/faceApi/course_api/';
  var token = storage.getItem("token");
  try {
    http.Response response = await http.get(url, headers: {
      'Accept': 'application/json',
      'Authorization': 'token $token'
    });
    var data = json.decode(response.body);
    //print(data);
    if (data.toString().isNotEmpty) {
      Course locModel = Course.fromJson(data);
      return locModel;
    } else {
      return null;
    }
  } catch (e) {
    throw e;
  }
}

class ClassN with ChangeNotifier {
  List<CourseName> couses = [];
  int _selectedItem;

  List<String> get cos {
    List<String> allCous = [];
    couses.map((e) => allCous.add(e.course_code)).toList();
    //notifyListeners();
    return allCous;
  }

  int get selected => _selectedItem;

  void setSelectedItem(String s) {
    final df = couses.indexWhere((element) => element.id == s);
    _selectedItem = df;
    notifyListeners();
  }

  Future<void> fetchCour() async {
    final url = "http://192.168.43.80:8080/faceApi/course_api/";
    var token = storage.getItem("token");

    try {
      http.Response response = await http.get(url, headers: {
        'Accept': 'application/json',
        'Authorization': 'token $token'
      });
      var data = json.decode(response.body)['data'] as List;
      print(data);
      final List<CourseName> courseData = [];
      data
          .map((e) => courseData
              .add(CourseName(id: e['id'], course_code: e['course_code'])))
          .toList();
      couses = courseData;
      notifyListeners();
    } catch (e) {
      throw e;
    }
  }
}
