
import 'package:flutter/material.dart';
import 'package:flutter_face_detection/responsive/sizingInformation.dart';
import 'package:flutter_face_detection/responsive/ui_utils.dart';

class BaseWidget extends StatelessWidget {
  final Widget Function(BuildContext context, SizingInformation sizingInformation) builder;
  BaseWidget({this.builder});
  @override
  Widget build(BuildContext context) {
    var mediaQuery = MediaQuery.of(context);
  
    return LayoutBuilder(builder: (context, boxConstraints){
        var sizingInformation = SizingInformation(
      orientation: mediaQuery.orientation,
      deviceScreenType: getDeviceType(mediaQuery),
      screenType: mediaQuery.size,   
      localWidget: Size(boxConstraints.maxWidth, boxConstraints.maxHeight)
    );
      return builder(context, sizingInformation);
    });
    
  }
}