import 'package:flutter/material.dart';
import 'package:flutter_face_detection/api/auth.dart';
import 'package:flutter_face_detection/screens/face_detect.dart';
import 'package:flutter_face_detection/screens/register.dart';
import 'package:provider/provider.dart';

class Login extends StatefulWidget {
  @override
  _LoginState createState() => _LoginState();
}

class _LoginState extends State<Login> {
  var username = TextEditingController();
  var password = TextEditingController();
  var notShowPassword = true;
  bool isLoading = false;

  void passwordToggle() {
    setState(() {
      notShowPassword = !notShowPassword;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Center(
      child: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            image(),
            SizedBox(
              height: 20.0,
            ),
            inputUsername(),
            SizedBox(
              height: 20.0,
            ),
            inputPassword(),
            SizedBox(
              height: 20.0,
            ),
            Container(
                margin: EdgeInsets.only(left: 200.0),
                child: GestureDetector(
                    onTap: () {
                      Navigator.of(context)
                          .push(MaterialPageRoute(builder: (context) {
                        return null;
                      }));
                    },
                    child: Text(
                      "Forget Password",
                      style: TextStyle(
                          color: Colors.pink[800], fontWeight: FontWeight.bold),
                    ))),
            SizedBox(
              height: 20.0,
            ),
            Container(
              width: 300.0,
              height: 50.0,
              child: RaisedButton(
                highlightColor: Colors.transparent,
                splashColor: Color(0xFFf7418c),
                onPressed: () {
                  login(username: username.text, password: password.text);
                },
                child: Text(
                  "Sign In",
                  style: TextStyle(color: Colors.white, fontSize: 20),
                ),
                color: Colors.pink[300],
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20)),
              ),
            ),
            SizedBox(
              height: 20.0,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text(
                  "Don't have an account",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                SizedBox(
                  width: 5.0,
                ),
                GestureDetector(
                    onTap: () {
                      Navigator.of(context).pushReplacement(
                          MaterialPageRoute(builder: (context) => Register()));
                    },
                    child: Text(
                      "Sign Up?",
                      style: TextStyle(
                          color: Colors.pink[800], fontWeight: FontWeight.bold),
                    ))
              ],
            )
          ],
        ),
      ),
    ));
  }

  Widget image() {
    return Container(
        width: 230,
        height: 100,
        alignment: Alignment.center,
        child: CircleAvatar(
          backgroundImage: AssetImage("assets/images/face.gif"),
        ));
  }

  Widget inputUsername() {
    return Container(
      padding: const EdgeInsets.only(left: 20, right: 20),
      child: TextField(
        controller: username,
        decoration: InputDecoration(
            focusColor: Colors.black,
            border: OutlineInputBorder(),
            labelText: 'Username',
            labelStyle: TextStyle(fontSize: 20),
            prefixIcon: Icon(
              Icons.mail,
              color: Colors.pink[800],
            )),
      ),
    );
  }

  Widget inputPassword() {
    return Container(
      padding: const EdgeInsets.only(left: 20, right: 20),
      child: TextField(
        obscureText: notShowPassword,
        controller: password,
        decoration: InputDecoration(
            focusColor: Colors.black,
            border: OutlineInputBorder(),
            labelText: 'Password',
            labelStyle: TextStyle(fontSize: 20),
            prefixIcon: Icon(
              Icons.lock,
              color: Colors.pink[800],
            ),
            suffixIcon: IconButton(
                icon: Icon(
                  Icons.remove_red_eye,
                  color: notShowPassword ? Colors.pink[800] : Colors.grey,
                ),
                onPressed: passwordToggle)),
      ),
    );
  }

  Future<void> login({username, password}) async {
    try {
      bool isToken = await Provider.of<AuthProvider>(context, listen: false)
          .loginApi(username: username, password: password);
      if (isToken) {
        CircularProgressIndicator(
          value: 2.0,
        );
        Navigator.push(
            context, MaterialPageRoute(builder: (ctx) => FaceDetect()));
      } else {
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
                  ),
                ],
              );
            });
      }
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
