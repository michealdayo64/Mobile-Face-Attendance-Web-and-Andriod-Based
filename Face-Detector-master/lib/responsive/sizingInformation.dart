import 'package:flutter/material.dart';
import 'deviceScreenType.dart';
class SizingInformation{
 final Orientation orientation;
 final DeviceScreenType deviceScreenType;
 final Size screenType;
 final Size localWidget;

 SizingInformation({this.orientation, this.deviceScreenType, this.screenType, this.localWidget});

 @override
  String toString() {
    
    return 'Orientation: $orientation DeviceScreenType: $deviceScreenType ScreenType: $screenType LocalWidget: $localWidget';
  }
}