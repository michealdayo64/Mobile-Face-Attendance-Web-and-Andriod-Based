import 'package:flutter/material.dart';
import 'package:flutter_face_detection/api/auth.dart';
import 'package:flutter_face_detection/api/course.dart';
import 'package:flutter_face_detection/api/take_attendance.dart';
//import 'package:flutter_face_detection/api/course.dart';
//import 'package:flutter_face_detection/api/level.dart';
import 'package:flutter_face_detection/screens/face_detect.dart';
//import 'package:flutter_face_detection/face_detect.dart';
import 'package:flutter_face_detection/screens/splashScreen.dart';
import 'package:localstorage/localstorage.dart';

import 'package:provider/provider.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    LocalStorage storage = new LocalStorage("userToken");
    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: AuthProvider()),
        ChangeNotifierProvider.value(value: TakeAttendanceProvider()),
        ChangeNotifierProvider.value(value: ClassN()),
      ],
      child: MaterialApp(
          title: 'Flutter Demo',
          theme: ThemeData(
            primarySwatch: Colors.blue,
          ),
          home: FutureBuilder(
              future: storage.ready,
              builder: (BuildContext context, AsyncSnapshot snapshot) {
                if (snapshot.data == null) {
                  return Scaffold(
                    body: Center(
                      child: CircularProgressIndicator(),
                    ),
                  );
                }
                if (storage.getItem("token") == null) {
                  return Splash();
                }
                return FaceDetect();
              })
          //Splash(),
          ),
    );
  }
}
