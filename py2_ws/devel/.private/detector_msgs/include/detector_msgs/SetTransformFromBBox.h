// Generated by gencpp from file detector_msgs/SetTransformFromBBox.msg
// DO NOT EDIT!


#ifndef DETECTOR_MSGS_MESSAGE_SETTRANSFORMFROMBBOX_H
#define DETECTOR_MSGS_MESSAGE_SETTRANSFORMFROMBBOX_H

#include <ros/service_traits.h>


#include <detector_msgs/SetTransformFromBBoxRequest.h>
#include <detector_msgs/SetTransformFromBBoxResponse.h>


namespace detector_msgs
{

struct SetTransformFromBBox
{

typedef SetTransformFromBBoxRequest Request;
typedef SetTransformFromBBoxResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct SetTransformFromBBox
} // namespace detector_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::detector_msgs::SetTransformFromBBox > {
  static const char* value()
  {
    return "cf10ef4f67b53145111605419d2c8caa";
  }

  static const char* value(const ::detector_msgs::SetTransformFromBBox&) { return value(); }
};

template<>
struct DataType< ::detector_msgs::SetTransformFromBBox > {
  static const char* value()
  {
    return "detector_msgs/SetTransformFromBBox";
  }

  static const char* value(const ::detector_msgs::SetTransformFromBBox&) { return value(); }
};


// service_traits::MD5Sum< ::detector_msgs::SetTransformFromBBoxRequest> should match
// service_traits::MD5Sum< ::detector_msgs::SetTransformFromBBox >
template<>
struct MD5Sum< ::detector_msgs::SetTransformFromBBoxRequest>
{
  static const char* value()
  {
    return MD5Sum< ::detector_msgs::SetTransformFromBBox >::value();
  }
  static const char* value(const ::detector_msgs::SetTransformFromBBoxRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::detector_msgs::SetTransformFromBBoxRequest> should match
// service_traits::DataType< ::detector_msgs::SetTransformFromBBox >
template<>
struct DataType< ::detector_msgs::SetTransformFromBBoxRequest>
{
  static const char* value()
  {
    return DataType< ::detector_msgs::SetTransformFromBBox >::value();
  }
  static const char* value(const ::detector_msgs::SetTransformFromBBoxRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::detector_msgs::SetTransformFromBBoxResponse> should match
// service_traits::MD5Sum< ::detector_msgs::SetTransformFromBBox >
template<>
struct MD5Sum< ::detector_msgs::SetTransformFromBBoxResponse>
{
  static const char* value()
  {
    return MD5Sum< ::detector_msgs::SetTransformFromBBox >::value();
  }
  static const char* value(const ::detector_msgs::SetTransformFromBBoxResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::detector_msgs::SetTransformFromBBoxResponse> should match
// service_traits::DataType< ::detector_msgs::SetTransformFromBBox >
template<>
struct DataType< ::detector_msgs::SetTransformFromBBoxResponse>
{
  static const char* value()
  {
    return DataType< ::detector_msgs::SetTransformFromBBox >::value();
  }
  static const char* value(const ::detector_msgs::SetTransformFromBBoxResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // DETECTOR_MSGS_MESSAGE_SETTRANSFORMFROMBBOX_H
