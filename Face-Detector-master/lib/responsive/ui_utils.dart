
import 'package:flutter/material.dart';

import 'deviceScreenType.dart';

DeviceScreenType getDeviceType(MediaQueryData mediaQuery){
  var orientation = mediaQuery.orientation;

  double deviceWidth = 0;

  if(orientation == Orientation.landscape){
    deviceWidth = mediaQuery.size.height;
  }else{
    deviceWidth = mediaQuery.size.width;
  }

  if(deviceWidth > 950){
   return DeviceScreenType.Desktop;
  }else if(deviceWidth > 600){
    return DeviceScreenType.Tablet;
  }else{
    return DeviceScreenType.Mobile;
  }
}