# CMake generated Testfile for 
# Source directory: /workspace/py3_ws/src/third-party/geometry2/tf2_sensor_msgs
# Build directory: /workspace/py3_ws/build/tf2_sensor_msgs
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_tf2_sensor_msgs_nosetests_test.test_tf2_sensor_msgs.py "/workspace/py3_ws/build/tf2_sensor_msgs/catkin_generated/env_cached.sh" "/home/developer/.pyenv/versions/catkin_py3/bin/python3" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/workspace/py3_ws/build/tf2_sensor_msgs/test_results/tf2_sensor_msgs/nosetests-test.test_tf2_sensor_msgs.py.xml" "--return-code" "\"/usr/bin/cmake\" -E make_directory /workspace/py3_ws/build/tf2_sensor_msgs/test_results/tf2_sensor_msgs" "/usr/bin/nosetests -P --process-timeout=60 /workspace/py3_ws/src/third-party/geometry2/tf2_sensor_msgs/test/test_tf2_sensor_msgs.py --with-xunit --xunit-file=/workspace/py3_ws/build/tf2_sensor_msgs/test_results/tf2_sensor_msgs/nosetests-test.test_tf2_sensor_msgs.py.xml")
add_test(_ctest_tf2_sensor_msgs_rostest_test_test.launch "/workspace/py3_ws/build/tf2_sensor_msgs/catkin_generated/env_cached.sh" "/home/developer/.pyenv/versions/catkin_py3/bin/python3" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/workspace/py3_ws/build/tf2_sensor_msgs/test_results/tf2_sensor_msgs/rostest-test_test.xml" "--return-code" "/home/developer/.pyenv/versions/catkin_py3/bin/python3 /opt/ros/melodic/share/rostest/cmake/../../../bin/rostest --pkgdir=/workspace/py3_ws/src/third-party/geometry2/tf2_sensor_msgs --package=tf2_sensor_msgs --results-filename test_test.xml --results-base-dir \"/workspace/py3_ws/build/tf2_sensor_msgs/test_results\" /workspace/py3_ws/src/third-party/geometry2/tf2_sensor_msgs/test/test.launch ")
subdirs("gtest")
