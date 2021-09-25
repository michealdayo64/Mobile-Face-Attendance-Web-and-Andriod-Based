import 'dart:async';
//import 'dart:html';
import 'package:flutter/material.dart';
import 'package:flutter_face_detection/screens/login.dart';


class Splash extends StatefulWidget {
  @override
  _SplashState createState() => _SplashState();
}

class _SplashState extends State<Splash> {
  @override
  void initState() {
    
    super.initState();
    Timer(Duration(seconds: 5), () {
      Navigator.of(context).pushReplacement(MaterialPageRoute(builder: (ctx) => Login()));
    });
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
       resizeToAvoidBottomPadding: false,
      body: Stack(
        fit: StackFit.expand,
        children: <Widget>[
          Container(
            decoration: BoxDecoration(
              
              color: Colors.pinkAccent[700]
            ),
          ),
          Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: <Widget>[
              Expanded(
                flex: 2,
                child: Container(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Container(
                       // decoration: BoxDecoration(borderRadius: BorderRadius.circular(10), color: Colors.black),
                        child: CircleAvatar(
                          backgroundColor: Colors.white,
                          //backgroundColor: Colors.white,
                          radius: 40.0,
                          backgroundImage: AssetImage("assets/images/face.gif"),
                        ),
                      ),
                      Container(
                        padding: EdgeInsets.only(top: 10),
                        child: Text("Student Face App", 
                        style: TextStyle(color: Colors.white, fontSize: 24.0, fontWeight: FontWeight.bold),),
                      )
                    ],
                  ),
                ),
              ),
              Expanded(
                flex: 1,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    CircularProgressIndicator(
                      
                    ),
                    Padding(padding: EdgeInsets.only(top: 20)),
                    Text("Made Attendance Eazy",
                    style: TextStyle(color: Colors.white, fontSize: 20),)
                  ],
                ),
              )
            ],
          )
        ],
      ),
    );
  }
}