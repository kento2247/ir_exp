from __future__ import absolute_import, division, print_function, unicode_literals

import json
import math
import os
import traceback
from select import select
from turtle import pos

import putIn_positionLabel as PLM
import rospkg
import rospy
import tf2_ros
from detector_msgs.srv import (
    GetObjectDetection,
    GetObjectDetectionRequest,
    SetTransformFromBBox,
    SetTransformFromBBoxRequest,
)
from std_msgs.msg import String
from wrs_algorithm.util import gripper, omni_base, whole_body

def execute_task2a(self):
    """
    task2aを実行する
    """
    rospy.loginfo("#### start Task 2a ####")
    self.change_pose("look_at_near_floor")
    gripper.command(0)
    self.change_pose("look_at_near_floor")
    self.goto_name("standby_2a")

    # 落ちているブロックを避けて移動
    self.execute_avoid_blocks()

    self.goto_name("go_throw_2a")
    whole_body.move_to_go()

# def execute_avoid_blocks(self):
#     # blockを避ける
#     for i in range(3):
#         detected_objs = self.get_latest_detection()
#         bboxes = detected_objs.bboxes
#         pos_bboxes = [self.get_grasp_coordinate(bbox) for bbox in bboxes]
#         waypoint = self.select_next_waypoint(i, pos_bboxes)
#         # TODO メッセージを確認するためコメントアウトを外す
#         rospy.loginfo(waypoint)
#         self.goto_pos(waypoint)

def execute_avoid_blocks(self):
    # blockを避けるのではなく、掴んで移動させる
    detected_objs = self.get_latest_detection()
    bboxes = detected_objs.bboxes

    # 物体を掴む
    if bboxes:
        graspable_obj = self.get_most_graspable_obj(bboxes)
        if graspable_obj is not None:
            label = graspable_obj["label"]
            grasp_bbox = graspable_obj["bbox"]
            rospy.loginfo("grasp the " + label)
            grasp_pos = self.get_grasp_coordinate(grasp_bbox)
            self.change_pose("grasp_on_table")
            self.exec_graspable_method(grasp_pos, label)
            self.change_pose("all_neutral")

            # 物体を移動させる場所を定義する
            destination = [0, 0, 0]  # ここに移動させる座標を指定する
            self.goto_pos(destination)
