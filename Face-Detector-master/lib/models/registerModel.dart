class RegisterModel {
  int id;
  String username;
  String email;
  String password;
  String firstName;
  String lastName;

  RegisterModel(
      {this.id,
      this.username,
      this.email,
      this.password,
      this.firstName,
      this.lastName});

  RegisterModel.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    username = json['username'];
    email = json['email'];
    password = json['password'];
    firstName = json['first_name'];
    lastName = json['last_name'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['username'] = this.username;
    data['email'] = this.email;
    data['password'] = this.password;
    data['first_name'] = this.firstName;
    data['last_name'] = this.lastName;
    return data;
  }
}