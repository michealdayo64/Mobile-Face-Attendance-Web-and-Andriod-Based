import 'package:flutter_face_detection/api/take_attendance.dart';
import 'package:flutter_face_detection/models/courseModel.dart';
import 'package:path/path.dart' as path;
import 'package:flutter/material.dart';
import 'dart:io';
import 'package:provider/provider.dart';
import 'dart:convert';
//import 'dart:ui' as ui;
//import 'package:firebase_ml_vision/firebase_ml_vision.dart';
import 'package:flutter_face_detection/api/course.dart';
import 'package:flutter_face_detection/api/level.dart';
import 'package:flutter_face_detection/api/section.dart';
import 'package:flutter_face_detection/screens/attendanceHistory.dart';
import 'package:flutter_face_detection/screens/login.dart';
import 'package:image_picker/image_picker.dart';
import 'package:localstorage/localstorage.dart';

class FaceDetect extends StatefulWidget {
  @override
  _FaceDetectState createState() => _FaceDetectState();
}

class _FaceDetectState extends State<FaceDetect> {
  File _imageFile;
  //List<Face> _faces;
  bool isLoading = false;
  //ui.Image _image;
  List<String> level = [];
  List<String> course_code = [];
  List<String> session = [];
  String levelselected;
  String sessionSelected;
  String courseSelected;
  var leavlid = 0;
  var sessionid = 0;
  int courseIdValue;
  String imgEnc;
  String fileName;
  var scaffoldKey = GlobalKey<ScaffoldState>();
  var _isInit = true;
  LocalStorage storage = new LocalStorage("userToken");

  @override
  void didChangeDependencies() {
    if (_isInit) {
      setState(() {
        isLoading = true;
      });

      Provider.of<ClassN>(context).fetchCour().then((_) {
        setState(() {
          isLoading = false;
        });
      });
    }
    _isInit = false;
    super.didChangeDependencies();
  }

  Future getImage(bool isCamera) async {
    File image;
    if (isCamera) {
      image = await ImagePicker.pickImage(source: ImageSource.camera);
    } else {
      image = await ImagePicker.pickImage(source: ImageSource.gallery);
    }
    setState(() {
      _imageFile = image;
    });
    final bytes = File(image.path).readAsBytesSync();
    imgEnc = base64Encode(bytes);

    final fname = File(image.path);
    fileName = path.basename(fname.path);
  }

  /*detectFaces(File imageFile) async {
    final image = FirebaseVisionImage.fromFile(imageFile);
    final faceDetector = FirebaseVision.instance.faceDetector();
    List<Face> faces = await faceDetector.processImage(image);
    if (mounted) {
      setState(() {
        _imageFile = imageFile;
        _faces = faces;
        _loadImage(imageFile);
      });
    }
  }

  _loadImage(File file) async {
    final data = await file.readAsBytes();
    await decodeImageFromList(data).then(
      (value) => setState(() {
        _image = value;
        isLoading = false;
      }),
    );
  }*/

  void logout() {
    storage.clear();
    Navigator.push(context, MaterialPageRoute(builder: (ctx) => Login()));
  }

  @override
  void initState() {
    getallLeves();
    getallSession();
    getallcourses();
    super.initState();
  }

  getallLeves() async {
    var getlevel = await fetchLevels();
    var totallevel = getlevel.data.length;
    int i = 0;
    for (i = 0; i < totallevel; i++) {
      setState(() {
        level.add(getlevel.data[i].stdLevel);
      });
    }
  }

  getallLevesID(levelselected) async {
// create this at d top of the code
    var getlevel = await fetchLevels();
    var totallevel = getlevel.data.length;
    int i = 0;
    for (i = 0; i < totallevel; i++) {
      if (getlevel.data[i].stdLevel == levelselected) {
        setState(() {
          leavlid = getlevel.data[i].id;
        });
        break;
      }
    }
  }

  getallSession() async {
    var getsession = await fetchsessions();
    var totalsession = getsession.data.length;
    int i = 0;
    for (i = 0; i < totalsession; i++) {
      setState(() {
        session.add(getsession.data[i].sessionStartYear +
            "/" +
            getsession.data[i].sessionEndYear);
      });
    }
  }

  getallsessionID(sessionSelected) async {
    //print(sessionSelected);
    var getsession = await fetchsessions();
    var totalsession = getsession.data.length;
    int i = 0;
    for (i = 0; i < totalsession; i++) {
      if (getsession.data[i].sessionStartYear +
              "/" +
              getsession.data[i].sessionEndYear ==
          sessionSelected) {
        setState(() {
          sessionid = getsession.data[i].id;
        });
        break;
      }
    }
  }

  getallcourses() async {
    var getcourse = await fetchCourses();
    var totalcourse = getcourse.data.length;
    int i = 0;
    for (i = 0; i < totalcourse; i++) {
      setState(() {
        course_code.add(getcourse.data[i].courseCode);
      });
    }
  }

  getAllCoursesId(courseSelected) async {
    var getId = await fetchCourses();
    var totalId = getId.data.length;
    for (int i = 0; i < totalId; i++) {
      if (getId.data[i].courseCode == courseSelected) {
        setState(() {
          courseIdValue = getId.data[i].id;
        });
        break;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final product = Provider.of<ClassN>(context);
    print(fileName);
    return Scaffold(
      key: scaffoldKey,
      body: ListView(
        children: <Widget>[
          Column(
            children: <Widget>[
              SizedBox(
                height: 20.0,
              ),
              isLoading
                  ? Center(child: CircularProgressIndicator())
                  : (_imageFile == null)
                      ? Center(child: Text('No image selected'))
                      : Center(
                          child: Image.file(
                            _imageFile,
                            width: double.infinity,
                            fit: BoxFit.cover,
                            height: 330.0,
                          ),
                        ),
              SizedBox(
                height: 10.0,
              ),
              DropdownButton(
                  elevation: 40,
                  hint: Text("Select Level",
                      style: TextStyle(
                          color: Colors.red[800], fontWeight: FontWeight.bold)),
                  value: levelselected,
                  onChanged: (a) {
                    product.setSelectedItem(a);
                    levelselected = product.selected.toString();
                    print(levelselected);
                    //print(a);
                  },
                  items: product.cos
                      .map((dept) => DropdownMenuItem(
                            child: Text(
                              dept,
                              style: TextStyle(color: Colors.red[800]),
                            ),
                            value: dept,
                          ))
                      ?.toList()),
              DropdownButton(
                elevation: 40,
                hint: Text("Select Course Code",
                    style: TextStyle(
                        color: Colors.red[800], fontWeight: FontWeight.bold)),
                value: courseSelected,
                onChanged: (courseSelected) {
                  getAllCoursesId(courseSelected);
                },
                items: course_code
                    .map((course) => DropdownMenuItem(
                          child: Text(
                            course,
                            style: TextStyle(color: Colors.red[800]),
                          ),
                          value: course,
                        ))
                    .toList(),
              ),
              DropdownButton(
                elevation: 40,
                hint: Text("Select Section",
                    style: TextStyle(
                        color: Colors.red[800], fontWeight: FontWeight.bold)),
                value: sessionSelected,
                onChanged: (sessionSelected) {
                  getallsessionID(sessionSelected);
                },
                items: session
                    .map((sess) => DropdownMenuItem(
                          child: Text(
                            sess,
                            style: TextStyle(color: Colors.red[800]),
                          ),
                          value: sess,
                        ))
                    .toList(),
              ),
              RaisedButton(
                //color: Colors.blue,
                onPressed: () {
                  take_attendance(
                      courseIdValue: courseIdValue,
                      sessionIdValue: sessionid,
                      levelIdValue: leavlid,
                      imageEnc: imgEnc,
                      imageName: fileName);
                },
                color: Colors.blue,
                child: !isLoading
                    ? Text(
                        "Take Attendance",
                        style: TextStyle(color: Colors.white),
                      )
                    : Center(child: CircularProgressIndicator()),
              ),
              RaisedButton(
                onPressed: () {
                  logout();
                },
                child: Text("Logout"),
              ),
              RaisedButton(onPressed: () {})
            ],
          ),
        ],
      ),
      floatingActionButton: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          FloatingActionButton(
            heroTag: null,
            onPressed: () {
              getImage(true);
            },
            tooltip: 'Camera',
            child: Icon(Icons.add_a_photo),
          ),
          SizedBox(
            height: 22.0,
          ),
          FloatingActionButton(
            heroTag: null,
            onPressed: () {
              getImage(false);
            },
            tooltip: 'Gallery',
            child: Icon(Icons.folder),
          ),
        ],
      ),
    );
  }

  Future<void> take_attendance(
      {courseIdValue,
      levelIdValue,
      sessionIdValue,
      imageEnc,
      imageName}) async {
    try {
      await Provider.of<TakeAttendanceProvider>(context, listen: false)
          .takeAttendance(
              courseIdValue: courseIdValue,
              levelIdValue: levelIdValue,
              sessionIdValue: sessionIdValue,
              imageEnc: imageEnc,
              imageName: imageName);

      Navigator.push(
          context, MaterialPageRoute(builder: (ctx) => AttendanceHistory()));
      // ignore: deprecated_member_use
      scaffoldKey.currentState.hideCurrentSnackBar();
      // ignore: deprecated_member_use
      scaffoldKey.currentState.showSnackBar(SnackBar(
        content: Text("Attendance Successful"),
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

/*class FacePainter extends CustomPainter {
  final ui.Image image;
  final List<Face> faces;
  final List<Rect> rects = [];

  FacePainter(this.image, this.faces) {
    for (var i = 0; i < faces.length; i++) {
      rects.add(faces[i].boundingBox);
    }
  }

  @override
  void paint(ui.Canvas canvas, ui.Size size) {
    final Paint paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 5.0
      ..color = Colors.yellow;

    canvas.drawImage(image, Offset.zero, Paint());
    for (var i = 0; i < faces.length; i++) {
      canvas.drawRect(rects[i], paint);
    }
  }

  @override
  bool shouldRepaint(FacePainter oldDelegate) {
    return image != oldDelegate.image || faces != oldDelegate.faces;
  }
}*/
