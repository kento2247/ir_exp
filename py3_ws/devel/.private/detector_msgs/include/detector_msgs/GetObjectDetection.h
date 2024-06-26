// Generated by gencpp from file detector_msgs/GetObjectDetection.msg
// DO NOT EDIT!


#ifndef DETECTOR_MSGS_MESSAGE_GETOBJECTDETECTION_H
#define DETECTOR_MSGS_MESSAGE_GETOBJECTDETECTION_H

#include <ros/service_traits.h>


#include <detector_msgs/GetObjectDetectionRequest.h>
#include <detector_msgs/GetObjectDetectionResponse.h>


namespace detector_msgs
{

struct GetObjectDetection
{

typedef GetObjectDetectionRequest Request;
typedef GetObjectDetectionResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct GetObjectDetection
} // namespace detector_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::detector_msgs::GetObjectDetection > {
  static const char* value()
  {
    return "44386689b8f2bacd7dd66f142a8c65bc";
  }

  static const char* value(const ::detector_msgs::GetObjectDetection&) { return value(); }
};

template<>
struct DataType< ::detector_msgs::GetObjectDetection > {
  static const char* value()
  {
    return "detector_msgs/GetObjectDetection";
  }

  static const char* value(const ::detector_msgs::GetObjectDetection&) { return value(); }
};


// service_traits::MD5Sum< ::detector_msgs::GetObjectDetectionRequest> should match
// service_traits::MD5Sum< ::detector_msgs::GetObjectDetection >
template<>
struct MD5Sum< ::detector_msgs::GetObjectDetectionRequest>
{
  static const char* value()
  {
    return MD5Sum< ::detector_msgs::GetObjectDetection >::value();
  }
  static const char* value(const ::detector_msgs::GetObjectDetectionRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::detector_msgs::GetObjectDetectionRequest> should match
// service_traits::DataType< ::detector_msgs::GetObjectDetection >
template<>
struct DataType< ::detector_msgs::GetObjectDetectionRequest>
{
  static const char* value()
  {
    return DataType< ::detector_msgs::GetObjectDetection >::value();
  }
  static const char* value(const ::detector_msgs::GetObjectDetectionRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::detector_msgs::GetObjectDetectionResponse> should match
// service_traits::MD5Sum< ::detector_msgs::GetObjectDetection >
template<>
struct MD5Sum< ::detector_msgs::GetObjectDetectionResponse>
{
  static const char* value()
  {
    return MD5Sum< ::detector_msgs::GetObjectDetection >::value();
  }
  static const char* value(const ::detector_msgs::GetObjectDetectionResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::detector_msgs::GetObjectDetectionResponse> should match
// service_traits::DataType< ::detector_msgs::GetObjectDetection >
template<>
struct DataType< ::detector_msgs::GetObjectDetectionResponse>
{
  static const char* value()
  {
    return DataType< ::detector_msgs::GetObjectDetection >::value();
  }
  static const char* value(const ::detector_msgs::GetObjectDetectionResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // DETECTOR_MSGS_MESSAGE_GETOBJECTDETECTION_H
