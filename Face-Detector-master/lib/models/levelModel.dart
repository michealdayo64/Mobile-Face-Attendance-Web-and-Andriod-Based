//import 'dart:convert';
//import 'package:http/http.dart' as http;

class Level {
  List<Data> data;

  Level({this.data});

  Level.fromJson(Map<String, dynamic> json) {
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
  String stdLevel;

  Data({this.id, this.stdLevel});

  Data.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    stdLevel = json['std_level'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['std_level'] = this.stdLevel;
    return data;
  }
}
