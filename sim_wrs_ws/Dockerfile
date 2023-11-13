FROM ghcr.io/hsr-project/tmc_wrs_docker:nvidia

# detect_contact が衝突情報を送るコードに変更
RUN rm -rf /wrs_ws/src/tmc_gazebo_task_evaluators
COPY ./src/tmc_gazebo_task_evaluators /wrs_ws/src/tmc_gazebo_task_evaluators

# 変更されたコードでbuild, installを実行
RUN cd /wrs_ws/ \
    && source /opt/ros/melodic/setup.bash \
    && catkin_make install -DCMAKE_INSTALL_PREFIX=/opt/ros/melodic
