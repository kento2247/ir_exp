// Generated by gencpp from file detector_msgs/GetObjectDetectionResponse.msg
// DO NOT EDIT!


#ifndef DETECTOR_MSGS_MESSAGE_GETOBJECTDETECTIONRESPONSE_H
#define DETECTOR_MSGS_MESSAGE_GETOBJECTDETECTIONRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <detector_msgs/BBoxArray.h>

namespace detector_msgs
{
template <class ContainerAllocator>
struct GetObjectDetectionResponse_
{
  typedef GetObjectDetectionResponse_<ContainerAllocator> Type;

  GetObjectDetectionResponse_()
    : successed(false)
    , error_code()
    , error_string()
    , bboxes()  {
    }
  GetObjectDetectionResponse_(const ContainerAllocator& _alloc)
    : successed(false)
    , error_code(_alloc)
    , error_string(_alloc)
    , bboxes(_alloc)  {
  (void)_alloc;
    }



   typedef uint8_t _successed_type;
  _successed_type successed;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _error_code_type;
  _error_code_type error_code;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _error_string_type;
  _error_string_type error_string;

   typedef  ::detector_msgs::BBoxArray_<ContainerAllocator>  _bboxes_type;
  _bboxes_type bboxes;





  typedef boost::shared_ptr< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> const> ConstPtr;

}; // struct GetObjectDetectionResponse_

typedef ::detector_msgs::GetObjectDetectionResponse_<std::allocator<void> > GetObjectDetectionResponse;

typedef boost::shared_ptr< ::detector_msgs::GetObjectDetectionResponse > GetObjectDetectionResponsePtr;
typedef boost::shared_ptr< ::detector_msgs::GetObjectDetectionResponse const> GetObjectDetectionResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator1> & lhs, const ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator2> & rhs)
{
  return lhs.successed == rhs.successed &&
    lhs.error_code == rhs.error_code &&
    lhs.error_string == rhs.error_string &&
    lhs.bboxes == rhs.bboxes;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator1> & lhs, const ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace detector_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "a1844b0eaadc0a88e74c9b0c7f1b7976";
  }

  static const char* value(const ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xa1844b0eaadc0a88ULL;
  static const uint64_t static_value2 = 0xe74c9b0c7f1b7976ULL;
};

template<class ContainerAllocator>
struct DataType< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "detector_msgs/GetObjectDetectionResponse";
  }

  static const char* value(const ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "bool successed\n"
"string error_code\n"
"string error_string\n"
"detector_msgs/BBoxArray bboxes\n"
"\n"
"\n"
"================================================================================\n"
"MSG: detector_msgs/BBoxArray\n"
"std_msgs/Header header\n"
"detector_msgs/BBox[] bboxes\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: detector_msgs/BBox\n"
"string label\n"
"float64 score\n"
"int64 x\n"
"int64 y\n"
"int64 w\n"
"int64 h\n"
;
  }

  static const char* value(const ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.successed);
      stream.next(m.error_code);
      stream.next(m.error_string);
      stream.next(m.bboxes);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GetObjectDetectionResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::detector_msgs::GetObjectDetectionResponse_<ContainerAllocator>& v)
  {
    s << indent << "successed: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.successed);
    s << indent << "error_code: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.error_code);
    s << indent << "error_string: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.error_string);
    s << indent << "bboxes: ";
    s << std::endl;
    Printer< ::detector_msgs::BBoxArray_<ContainerAllocator> >::stream(s, indent + "  ", v.bboxes);
  }
};

} // namespace message_operations
} // namespace ros

#endif // DETECTOR_MSGS_MESSAGE_GETOBJECTDETECTIONRESPONSE_H