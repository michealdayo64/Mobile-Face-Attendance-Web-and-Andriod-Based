import 'package:flutter/material.dart';
import 'package:flutter_face_detection/api/auth.dart';
import 'package:flutter_face_detection/screens/login.dart';
import 'package:provider/provider.dart';
//import 'package:fluttertoast/fluttertoast.dart';

class Register extends StatefulWidget {
  @override
  _RegisterState createState() => _RegisterState();
}

class _RegisterState extends State<Register> {
  var firstname = TextEditingController();
  var lastname = TextEditingController();
  var username = TextEditingController();
  var email = TextEditingController();
  var password = TextEditingController();
  var phoneNo = TextEditingController();
  var scaffoldKey = GlobalKey<ScaffoldState>();

  var notShowPassword = true;

  void passwordToggle() {
    setState(() {
      notShowPassword = !notShowPassword;
    });
  }

  @override
  void initState() {
    super.initState();
  }

/*FlutterToast flutterToast;
_showToast(message) {
    Widget toast = Container(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
        color: Colors.greenAccent,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.check),
          SizedBox(
            width: 12.0,
          ),
          Text(message),
        ],
      ),
    );

    flutterToast.showToast(
      child: toast,
      gravity: ToastGravity.CENTER,
      toastDuration: Duration(seconds: 4),
    );
  }*/
  @override
  Widget build(BuildContext context) {
    print(username);
    String defaultFontFamily = 'Roboto-Light.ttf';
    double defaultFontSize = 14;
    double defaultIconSize = 17;

    return Scaffold(
      key: scaffoldKey,
      body: Container(
        padding: EdgeInsets.only(left: 20, right: 20, top: 35, bottom: 30),
        width: double.infinity,
        height: double.infinity,
        color: Colors.white70,
        child: ListView(
          children: <Widget>[
            InkWell(
              child: Container(
                child: Align(
                  alignment: Alignment.topLeft,
                  child: Icon(Icons.close),
                ),
              ),
              onTap: () {
                Navigator.pop(context);
              },
            ),
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Container(
                    width: 230,
                    height: 100,
                    alignment: Alignment.center,
                    child: CircleAvatar(
                      backgroundImage: AssetImage("assets/images/face.gif"),
                    )),
                SizedBox(
                  height: 15,
                ),
                Row(
                  children: <Widget>[
                    Flexible(
                      flex: 1,
                      child: TextField(
                        controller: firstname,
                        showCursor: true,
                        decoration: InputDecoration(
                          border: OutlineInputBorder(
                            borderRadius:
                                BorderRadius.all(Radius.circular(10.0)),
                            borderSide: BorderSide(
                              width: 0,
                              style: BorderStyle.none,
                            ),
                          ),
                          filled: true,
                          fillColor: Color(0xFFF2F3F5),
                          hintStyle: TextStyle(
                            color: Color(0xFF666666),
                            fontFamily: defaultFontFamily,
                            fontSize: defaultFontSize,
                          ),
                          hintText: "First Name",
                        ),
                      ),
                    ),
                    SizedBox(
                      width: 10,
                    ),
                    Flexible(
                      flex: 1,
                      child: TextField(
                        controller: lastname,
                        showCursor: true,
                        decoration: InputDecoration(
                          border: OutlineInputBorder(
                            borderRadius:
                                BorderRadius.all(Radius.circular(10.0)),
                            borderSide: BorderSide(
                              width: 0,
                              style: BorderStyle.none,
                            ),
                          ),
                          filled: true,
                          fillColor: Color(0xFFF2F3F5),
                          hintStyle: TextStyle(
                            color: Color(0xFF666666),
                            fontFamily: defaultFontFamily,
                            fontSize: defaultFontSize,
                          ),
                          hintText: "Last Name",
                        ),
                      ),
                    ),
                  ],
                ),
                SizedBox(
                  height: 15,
                ),
                TextField(
                  controller: username,
                  showCursor: true,
                  //keyboardType: TextInputType.emailAddress,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(10.0)),
                      borderSide: BorderSide(
                        width: 0,
                        style: BorderStyle.none,
                      ),
                    ),
                    filled: true,
                    prefixIcon: Icon(
                      Icons.phone,
                      color: Color(0xFF666666),
                      size: defaultIconSize,
                    ),
                    fillColor: Color(0xFFF2F3F5),
                    hintStyle: TextStyle(
                        color: Color(0xFF666666),
                        fontFamily: defaultFontFamily,
                        fontSize: defaultFontSize),
                    hintText: "Username",
                  ),
                ),
                SizedBox(
                  height: 15,
                ),
                TextField(
                  showCursor: true,
                  controller: email,
                  keyboardType: TextInputType.emailAddress,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(10.0)),
                      borderSide: BorderSide(
                        width: 0,
                        style: BorderStyle.none,
                      ),
                    ),
                    filled: true,
                    prefixIcon: Icon(
                      Icons.phone,
                      color: Color(0xFF666666),
                      size: defaultIconSize,
                    ),
                    fillColor: Color(0xFFF2F3F5),
                    hintStyle: TextStyle(
                        color: Color(0xFF666666),
                        fontFamily: defaultFontFamily,
                        fontSize: defaultFontSize),
                    hintText: "Email",
                  ),
                ),
                SizedBox(
                  height: 15,
                ),
                TextField(
                  controller: password,
                  showCursor: true,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(10.0)),
                      borderSide: BorderSide(
                        width: 0,
                        style: BorderStyle.none,
                      ),
                    ),
                    filled: true,
                    prefixIcon: Icon(
                      Icons.phone,
                      color: Color(0xFF666666),
                      size: defaultIconSize,
                    ),
                    suffixIcon: IconButton(
                        icon: Icon(
                          notShowPassword
                              ? Icons.visibility
                              : Icons.visibility_off,
                          size: defaultIconSize,
                        ),
                        onPressed: passwordToggle),
                    fillColor: Color(0xFFF2F3F5),
                    hintStyle: TextStyle(
                        color: Color(0xFF666666),
                        fontFamily: defaultFontFamily,
                        fontSize: defaultFontSize),
                    hintText: "Password",
                  ),
                ),
                SizedBox(
                  height: 15,
                ),
                TextField(
                  controller: phoneNo,
                  keyboardType: TextInputType.phone,
                  showCursor: true,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.all(Radius.circular(10.0)),
                      borderSide: BorderSide(
                        width: 0,
                        style: BorderStyle.none,
                      ),
                    ),
                    filled: true,
                    prefixIcon: Icon(
                      Icons.phone,
                      color: Color(0xFF666666),
                      size: defaultIconSize,
                    ),
                    fillColor: Color(0xFFF2F3F5),
                    hintStyle: TextStyle(
                        color: Color(0xFF666666),
                        fontFamily: defaultFontFamily,
                        fontSize: defaultFontSize),
                    hintText: "Phone Number",
                  ),
                ),
                SizedBox(
                  height: 15,
                ),
                Container(
                  width: double.infinity,
                  decoration: new BoxDecoration(
                    borderRadius: BorderRadius.all(Radius.circular(5.0)),
                    boxShadow: <BoxShadow>[
                      BoxShadow(
                        color: Color(0xFFfbab66),
                      ),
                      BoxShadow(
                        color: Color(0xFFf7418c),
                      ),
                    ],
                    gradient: new LinearGradient(
                        colors: [Color(0xFFf7418c), Color(0xFFfbab66)],
                        begin: const FractionalOffset(0.2, 0.2),
                        end: const FractionalOffset(1.0, 1.0),
                        stops: [0.0, 1.0],
                        tileMode: TileMode.clamp),
                  ),
                  child: MaterialButton(
                      highlightColor: Colors.transparent,
                      splashColor: Color(0xFFf7418c),
                      //shape: RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(5.0))),
                      child: Padding(
                        padding: const EdgeInsets.symmetric(
                            vertical: 10.0, horizontal: 42.0),
                        child: Text(
                          "SIGN UP",
                          style: TextStyle(
                              color: Colors.white,
                              fontSize: 25.0,
                              fontFamily: "WorkSansBold"),
                        ),
                      ),
                      onPressed: () {
                        register(
                            username: username.text,
                            email: email.text,
                            password: password.text,
                            firstname: firstname.text,
                            lastname: lastname.text,
                            phoneNo: phoneNo.text);
                      }),
                ),
              ],
            ),
            SizedBox(
              height: 20.0,
            ),
            Align(
              alignment: Alignment.bottomCenter,
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Container(
                    child: Text(
                      "Already have an account? ",
                      style: TextStyle(
                        color: Color(0xFF666666),
                        fontFamily: defaultFontFamily,
                        fontSize: defaultFontSize,
                        fontStyle: FontStyle.normal,
                      ),
                    ),
                  ),
                  InkWell(
                    onTap: () {
                      Navigator.push(context,
                          MaterialPageRoute(builder: (ctx) => Login()));
                    },
                    child: Container(
                      child: Text(
                        "Sign In",
                        style: TextStyle(
                          color: Color(0xFFf7418c),
                          fontFamily: defaultFontFamily,
                          fontSize: defaultFontSize,
                          fontStyle: FontStyle.normal,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> register(
      {username, email, password, firstname, lastname, phoneNo}) async {
    try {
      await Provider.of<AuthProvider>(context, listen: false).registerApi(
          username: username,
          email: email,
          password: password,
          firstname: firstname,
          lastname: lastname,
          phoneNo: phoneNo);

      //Navigator.push(context, MaterialPageRoute(builder: (ctx) => Login()));
      // ignore: deprecated_member_use
      scaffoldKey.currentState.hideCurrentSnackBar();
      // ignore: deprecated_member_use
      scaffoldKey.currentState.showSnackBar(SnackBar(
        content: Text("Registration Successful"),
        duration: Duration(seconds: 2),
      ));
    } catch (error) {
      await showDialog(
          context: context,
          builder: (ctx) {
            return AlertDialog(
              title: Text("Something is wrong, Pls try again"),
              actions: <Widget>[
                RaisedButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  child: Text("Ok"),
                )
              ],
            );
          });
    }
    //
  }
}
