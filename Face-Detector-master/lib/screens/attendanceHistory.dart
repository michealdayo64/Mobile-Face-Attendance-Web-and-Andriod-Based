import 'package:flutter/material.dart';
import 'package:flutter_face_detection/api/attendHis.dart';
import 'package:flutter_face_detection/models/attendHistory.dart';
import 'package:flutter_face_detection/responsive/baseWidget.dart';
//import 'package:intl/intl.dart';
import 'attendanceDetail.dart';

class AttendanceHistory extends StatefulWidget {
  @override
  _AttendanceHistoryState createState() => _AttendanceHistoryState();
}

class _AttendanceHistoryState extends State<AttendanceHistory> {
  Future allAttendance;

  @override
  void initState() {
    allAttendance = attendanceHistoryApi();

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return BaseWidget(
      builder: (context, sizingInformation) {
        return Scaffold(
          appBar: AppBar(
            backgroundColor: Colors.pink[800],
            title: Text("Attendence History"),
          ),
          body: SingleChildScrollView(
            child: Column(
              //crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                SizedBox(
                  height: 20.0,
                ),
                Padding(
                  padding: const EdgeInsets.only(left: 10, right: 10.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: <Widget>[
                      Text("Attendance List",
                          style: TextStyle(
                            color: Colors.pink[800],
                            fontWeight: FontWeight.bold,
                            fontSize: 25.0,
                          )),
                      RaisedButton(
                        onPressed: () {},
                        child: Text(
                          "Save As CSV",
                          style: TextStyle(color: Colors.white),
                        ),
                        color: Colors.green,
                      )
                    ],
                  ),
                ),
                FutureBuilder<Attend>(
                  future: allAttendance,
                  builder: (context, getServ) {
                    switch (getServ.connectionState) {
                      case ConnectionState.none:
                        return Text('');
                        break;
                      case ConnectionState.waiting:
                        // return Center(
                        //     child: CircularProgressIndicator());
                        return Text('');
                        break;
                      case ConnectionState.active:
                        return Text('');
                        break;
                      case ConnectionState.done:
                        if (getServ.hasError) {
                          return Center(
                              child: Text(
                            'No list found! Kindly refresh',
                            style: TextStyle(
                                color: Colors.red, fontWeight: FontWeight.bold),
                          ));
                        } else if (getServ.hasData) {
                          if (getServ.data.attList.isEmpty) {
                            return Center(
                                child: Text('  ',
                                    style: TextStyle(
                                      color: Colors.red,
                                      fontWeight: FontWeight.w800,
                                    )));
                          } else {
                            return body(getServ.data);
                          }
                        } else {
                          return Text('');
                        }
                        break;
                    }
                    return Container();
                  },
                )
              ],
            ),
          ),
        );
      },
    );
  }

  body(Attend data) {
    return Container(
      //padding: EdgeInsets.all(8.0),
      height: 800,
      child: ListView.builder(
        itemCount: data.attList.length,
        shrinkWrap: true,
        physics: NeverScrollableScrollPhysics(),
        itemBuilder: (context, index) {
          return GestureDetector(
            onTap: () {
              Navigator.of(context).push(MaterialPageRoute(builder: (context) {
                return AttendanceDetail();
              }));
            },
            child: Card(
              child: Column(
                children: <Widget>[
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: <Widget>[
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: <Widget>[
                            CircleAvatar(
                              radius: 40.0,
                              backgroundImage: NetworkImage(
                                  "${data.attList[index].studentId.photo}"),
                            ),
                            Text(
                              "${data.attList[index].studentId.matricNo}",
                              style: TextStyle(
                                  color: Colors.green,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16.0),
                            ),
                            Text(
                              "Name: ${data.attList[index].studentId.student.firstName} ${data.attList[index].studentId.student.lastName}",
                              style: TextStyle(
                                  color: Colors.green,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16.0),
                            ),
                            Text(
                              "",
                              style: TextStyle(
                                  color: Colors.green,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16.0),
                            )
                          ],
                        ),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: <Widget>[
                            data.attList[index].status
                                ? Text(
                                    "Present",
                                    style: TextStyle(
                                        color: Colors.green,
                                        fontWeight: FontWeight.bold,
                                        fontSize: 20.0),
                                  )
                                : Text(
                                    "Absent",
                                    style: TextStyle(
                                        color: Colors.red,
                                        fontWeight: FontWeight.bold,
                                        fontSize: 20.0),
                                  ),
                            SizedBox(
                              height: 50.0,
                            ),
                            Text(
                              "Date: ${data.attList[index].created_at}",
                              style: TextStyle(
                                  color: Colors.black,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16.0),
                            ),
                            Text(
                              "",
                              style: TextStyle(
                                  color: Colors.black,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 16.0),
                            )
                          ],
                        )
                      ],
                    ),
                  )
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
