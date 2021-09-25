
import 'package:flutter/material.dart';
import 'package:flutter_face_detection/responsive/baseWidget.dart';

class AttendanceDetail extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BaseWidget(
      builder: (context, sizingInformation){
        return Scaffold(
          appBar: AppBar(
            title: Text("Student Detail"),
            backgroundColor: Colors.red[800],
          ),
          body: SingleChildScrollView(
            child: Column(
              children: <Widget>[
                Container(
                  //height: 330.0,
                  width: double.infinity,
                  child: Image.asset("assets/images/Avatar.png", fit: BoxFit.cover,),
                ),
                SizedBox(
                  height: 20.0,
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: <Widget>[
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: <Widget>[
                      Text("Code: CSC 401", style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold, fontSize: 20.0),),
                      SizedBox(
                    height: 20.0,
                  ),
                      Text("Level: 200", style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold, fontSize: 20.0),),
                      SizedBox(
                    height: 20.0,
                  ),
                      Text("Type: Class", style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold, fontSize: 20.0),)
                                    
                    ],
                  ),
                  Column(
                                    crossAxisAlignment: CrossAxisAlignment.end,
                                    children: <Widget>[
                                      Text("Present", style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold, fontSize: 20.0),),
                                      SizedBox(
                                        height: 50.0,
                                      ),
                                  Text("Date: 20/02/2021", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16.0),),
                                  Text("Time: 12:45pm", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16.0),)
                                    ],
                                  )
              ],),
                )
              ],
              
            ),
          ),
        );
      },
    );
  }
}