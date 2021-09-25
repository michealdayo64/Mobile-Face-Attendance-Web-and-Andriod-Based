import 'dart:convert';
import 'package:http/http.dart' as http;
//import 'package:flutter/material.dart';
import 'package:flutter_face_detection/models/levelModel.dart';

Future<Level> fetchLevels() async {
  String url = 'http://192.168.43.80:8080/faceApi/level_api/';
  try {
    http.Response response = await http.get(url);
    var data = json.decode(response.body);
    if (data.toString().isNotEmpty) {
      Level locModel = Level.fromJson(data);
      return locModel;
    } else {
      return null;
    }
  } catch (e) {
    throw e;
  }
}
