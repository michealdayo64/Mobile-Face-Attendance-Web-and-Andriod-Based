import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:convert';
import 'package:localstorage/localstorage.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class TakeAttendanceProvider with ChangeNotifier {
  LocalStorage storage = new LocalStorage("userToken");

  Future<void> takeAttendance({courseIdValue, levelIdValue, sessionIdValue, imageEnc, imageName}) async {
    String url = 'http://192.168.43.224:8080/faceApi/take_attendance/';
    var token = storage.getItem("token");
    try {
      http.Response response = await http.post(url,
          body: json.encode({
            'courseIdValue': courseIdValue,
            'levelIdValue': levelIdValue,
            'sessionIdValue': sessionIdValue,
            'imageEnc': imageEnc,
            'imageName': imageName,
          }),
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'token $token'
            });

      var responseData = json.decode(response.body) as Map;
      print(responseData);
    } catch (e) {
      print('e attendanceApi');
      //print(e);
      throw e;
    }
  }
}
