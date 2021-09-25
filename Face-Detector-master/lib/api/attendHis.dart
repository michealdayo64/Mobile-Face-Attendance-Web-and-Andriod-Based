import 'dart:async';
import 'dart:convert';
import 'package:flutter_face_detection/models/attendHistory.dart';
import 'package:http/http.dart' as http;
import 'package:localstorage/localstorage.dart';

LocalStorage storage = new LocalStorage("userToken");

Future<Attend> attendanceHistoryApi() async {
  String url = 'http://192.168.43.224:8080/faceApi/attendance_history/';
  var token = storage.getItem("token");
  try {
    http.Response response = await http.get(url, headers: {
      'Accept': 'application/json',
      'Authorization': 'token $token'
    });
    var data = json.decode(response.body);
    print(data);
    if (data.toString().isNotEmpty) {
      Attend locModel = Attend.fromJson(data);
      return locModel;
    } else {
      return null;
    }
  } catch (e) {
    throw e;
  }
}
