# CMake generated Testfile for 
# Source directory: /workspace/py3_ws/src/third-party/geometry2/tf2_kdl
# Build directory: /workspace/py3_ws/build/tf2_kdl
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_tf2_kdl_rostest_test_test.launch "/workspace/py3_ws/build/tf2_kdl/catkin_generated/env_cached.sh" "/home/developer/.pyenv/versions/catkin_py3/bin/python3" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/workspace/py3_ws/build/tf2_kdl/test_results/tf2_kdl/rostest-test_test.xml" "--return-code" "/home/developer/.pyenv/versions/catkin_py3/bin/python3 /opt/ros/melodic/share/rostest/cmake/../../../bin/rostest --pkgdir=/workspace/py3_ws/src/third-party/geometry2/tf2_kdl --package=tf2_kdl --results-filename test_test.xml --results-base-dir \"/workspace/py3_ws/build/tf2_kdl/test_results\" /workspace/py3_ws/src/third-party/geometry2/tf2_kdl/test/test.launch ")
add_test(_ctest_tf2_kdl_rostest_test_test_python.launch "/workspace/py3_ws/build/tf2_kdl/catkin_generated/env_cached.sh" "/home/developer/.pyenv/versions/catkin_py3/bin/python3" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/workspace/py3_ws/build/tf2_kdl/test_results/tf2_kdl/rostest-test_test_python.xml" "--return-code" "/home/developer/.pyenv/versions/catkin_py3/bin/python3 /opt/ros/melodic/share/rostest/cmake/../../../bin/rostest --pkgdir=/workspace/py3_ws/src/third-party/geometry2/tf2_kdl --package=tf2_kdl --results-filename test_test_python.xml --results-base-dir \"/workspace/py3_ws/build/tf2_kdl/test_results\" /workspace/py3_ws/src/third-party/geometry2/tf2_kdl/test/test_python.launch ")
subdirs("gtest")
