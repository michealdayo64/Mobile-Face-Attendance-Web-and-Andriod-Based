class Session {
  List<Data> data;

  Session({this.data});

  Session.fromJson(Map<String, dynamic> json) {
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
  String sessionStartYear;
  String sessionEndYear;

  Data({this.id, this.sessionStartYear, this.sessionEndYear});

  Data.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    sessionStartYear = json['session_start_year'];
    sessionEndYear = json['session_end_year'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['session_start_year'] = this.sessionStartYear;
    data['session_end_year'] = this.sessionEndYear;
    return data;
  }
}
