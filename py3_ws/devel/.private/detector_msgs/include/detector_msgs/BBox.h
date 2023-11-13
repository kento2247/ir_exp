// Generated by gencpp from file detector_msgs/BBox.msg
// DO NOT EDIT!


#ifndef DETECTOR_MSGS_MESSAGE_BBOX_H
#define DETECTOR_MSGS_MESSAGE_BBOX_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace detector_msgs
{
template <class ContainerAllocator>
struct BBox_
{
  typedef BBox_<ContainerAllocator> Type;

  BBox_()
    : label()
    , score(0.0)
    , x(0)
    , y(0)
    , w(0)
    , h(0)  {
    }
  BBox_(const ContainerAllocator& _alloc)
    : label(_alloc)
    , score(0.0)
    , x(0)
    , y(0)
    , w(0)
    , h(0)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _label_type;
  _label_type label;

   typedef double _score_type;
  _score_type score;

   typedef int64_t _x_type;
  _x_type x;

   typedef int64_t _y_type;
  _y_type y;

   typedef int64_t _w_type;
  _w_type w;

   typedef int64_t _h_type;
  _h_type h;





  typedef boost::shared_ptr< ::detector_msgs::BBox_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::detector_msgs::BBox_<ContainerAllocator> const> ConstPtr;

}; // struct BBox_

typedef ::detector_msgs::BBox_<std::allocator<void> > BBox;

typedef boost::shared_ptr< ::detector_msgs::BBox > BBoxPtr;
typedef boost::shared_ptr< ::detector_msgs::BBox const> BBoxConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::detector_msgs::BBox_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::detector_msgs::BBox_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::detector_msgs::BBox_<ContainerAllocator1> & lhs, const ::detector_msgs::BBox_<ContainerAllocator2> & rhs)
{
  return lhs.label == rhs.label &&
    lhs.score == rhs.score &&
    lhs.x == rhs.x &&
    lhs.y == rhs.y &&
    lhs.w == rhs.w &&
    lhs.h == rhs.h;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::detector_msgs::BBox_<ContainerAllocator1> & lhs, const ::detector_msgs::BBox_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace detector_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::detector_msgs::BBox_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::detector_msgs::BBox_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::detector_msgs::BBox_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::detector_msgs::BBox_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::detector_msgs::BBox_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::detector_msgs::BBox_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::detector_msgs::BBox_<ContainerAllocator> >
{
  static const char* value()
  {
    return "3d82f40a3288314466c1bd6f266ea212";
  }

  static const char* value(const ::detector_msgs::BBox_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x3d82f40a32883144ULL;
  static const uint64_t static_value2 = 0x66c1bd6f266ea212ULL;
};

template<class ContainerAllocator>
struct DataType< ::detector_msgs::BBox_<ContainerAllocator> >
{
  static const char* value()
  {
    return "detector_msgs/BBox";
  }

  static const char* value(const ::detector_msgs::BBox_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::detector_msgs::BBox_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string label\n"
"float64 score\n"
"int64 x\n"
"int64 y\n"
"int64 w\n"
"int64 h\n"
;
  }

  static const char* value(const ::detector_msgs::BBox_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::detector_msgs::BBox_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.label);
      stream.next(m.score);
      stream.next(m.x);
      stream.next(m.y);
      stream.next(m.w);
      stream.next(m.h);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct BBox_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::detector_msgs::BBox_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::detector_msgs::BBox_<ContainerAllocator>& v)
  {
    s << indent << "label: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.label);
    s << indent << "score: ";
    Printer<double>::stream(s, indent + "  ", v.score);
    s << indent << "x: ";
    Printer<int64_t>::stream(s, indent + "  ", v.x);
    s << indent << "y: ";
    Printer<int64_t>::stream(s, indent + "  ", v.y);
    s << indent << "w: ";
    Printer<int64_t>::stream(s, indent + "  ", v.w);
    s << indent << "h: ";
    Printer<int64_t>::stream(s, indent + "  ", v.h);
  }
};

} // namespace message_operations
} // namespace ros

#endif // DETECTOR_MSGS_MESSAGE_BBOX_H
