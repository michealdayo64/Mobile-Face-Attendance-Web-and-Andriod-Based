import 'dart:async';
import 'dart:convert';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:localstorage/localstorage.dart';

class AuthProvider with ChangeNotifier {
  LocalStorage storage = new LocalStorage("userToken");

  // ignore: missing_return
  Future<void> registerApi(
      {username, email, password, firstname, lastname, phoneNo}) async {
    String url = 'http://192.168.43.80:8080/faceApi/register/';
    try {
      http.Response response = await http.post(url,
          body: json.encode({
            'username': username,
            'email': email,
            'password': password,
            'first_name': firstname,
            'last_name': lastname,
            'phone_no': phoneNo
          }),
          headers: {'Content-Type': 'application/json'});

      var responseData = json.decode(response.body) as Map;
      print(responseData);
    } catch (e) {
      print('e registerApi');
      //print(e);
      throw e;
    }
  }

  Future<bool> loginApi({username, password}) async {
    String url = 'http://192.168.43.80:8080/faceApi/login/';
    try {
      http.Response response = await http.post(url,
          body: json.encode({'username': username, 'password': password}),
          headers: {'Content-Type': 'application/json'});
      var responseData = json.decode(response.body) as Map;
      if (responseData.containsKey("token")) {
        storage.setItem("token", responseData['token']);
        return true;
      }
      print(false);
      return false;
    } catch (e) {
      return false;
      //throw e;

    }
  }
}
