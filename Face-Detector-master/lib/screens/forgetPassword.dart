import 'package:flutter/material.dart';
import 'package:flutter_face_detection/responsive/baseWidget.dart';

import 'login.dart';
//import 'package:student_app/responsive/baseWidget.dart';

class ForgotPassword extends StatefulWidget {
  @override
  _ForgotPasswordState createState() => _ForgotPasswordState();
}

class _ForgotPasswordState extends State<ForgotPassword> {
  TextEditingController _email;
  @override
  Widget build(BuildContext context) {
    return BaseWidget(
      builder: (context, sizingInformation) {
        return Scaffold(
          appBar: AppBar(
            backgroundColor: Colors.red[800],
            title: Text("Forgot Password"),
          ),
          body: SingleChildScrollView(
            child: Center(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: <Widget>[
                  SizedBox(
                    height: 20.0,
                  ),
                  Container(
                      margin: EdgeInsets.only(right: 20.0),
                      child: IconButton(
                          icon: Icon(
                            Icons.cancel,
                            color: Colors.red,
                            size: 50.0,
                          ),
                          onPressed: () {
                            Navigator.of(context).pop();
                          })),
                  SizedBox(
                    height: 50.0,
                  ),
                  Center(
                      child: Image.asset(
                    "assets/images/lock.png",
                    height: 100.0,
                  )),
                  SizedBox(
                    height: 20.0,
                  ),
                  Text(
                    "Forget",
                    style: TextStyle(fontSize: 40.0),
                  ),
                  Text(
                    "Your Password?",
                    style: TextStyle(fontSize: 40.0),
                  ),
                  SizedBox(
                    height: 50.0,
                  ),
                  //Text("", style: TextStyle(fontSize: 25.0, color: Colors.grey),),
                  Padding(
                    padding: const EdgeInsets.only(left: 25.0),
                    child: Text(
                      "Do not worry, we'll send the account details to your mail",
                      style: TextStyle(fontSize: 25.0, color: Colors.grey),
                    ),
                  ),

                  SizedBox(
                    height: 50.0,
                  ),
                  Card(
                    elevation: 5.0,
                    color: Colors.grey[200],
                    margin: EdgeInsets.only(left: 40.0, right: 40.0),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20.0)),
                    child: Container(
                      padding: EdgeInsets.only(left: 20.0, right: 20.0),
                      //alignment: Alignment.center,
                      child: TextField(
                        controller: _email,
                        decoration: InputDecoration(
                          hintText: 'Enter Your Email Address',
                          border: InputBorder.none,
                          hintStyle: TextStyle(fontSize: 20.0),
                          //alignLabelWithHint: true
                        ),
                      ),
                    ),
                  ),
                  SizedBox(
                    height: 20.0,
                  ),
                  Container(
                    height: 50.0,
                    width: 250.0,
                    child: RaisedButton(
                      onPressed: () {
                        Navigator.push(context,
                            MaterialPageRoute(builder: (ctx) => Login()));
                      },
                      color: Colors.green,
                      child: Text(
                        "Send Password",
                        style: TextStyle(fontSize: 20.0, color: Colors.white),
                      ),
                      shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(20.0)),
                      elevation: 5.0,
                    ),
                  ),
                  SizedBox(
                    height: 30.0,
                  )
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
