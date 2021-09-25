import 'dart:convert';
import 'package:flutter_face_detection/models/sessionModel.dart';
import 'package:http/http.dart' as http;

Future<Session> fetchsessions() async {
  String url = 'http://192.168.43.80:8080/faceApi/session_api/';
  //var token = storage.getItem("token");
  try {
    http.Response response = await http.get(url);
    //final List<Section> loadedProds = [];
    var data = json.decode(response.body);

    //print(data);
    if (data.toString().isNotEmpty) {
      Session locModel = Session.fromJson(data);
      return locModel;
    } else {
      return null;
    }
  } catch (e) {
    throw e;
  }
}
