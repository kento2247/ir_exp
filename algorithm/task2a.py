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



def select_next_waypoint(self, max_stp current_stp, pos_bboxes):
    """
    waypoints から近い場所にあるものを除外し、最適なwaypointを返す。
    x座標を原点に近い方からxa,xb,xcに定義する。bboxを判断基準として移動先を決定する(デフォルトは0.45間隔)
    pos_bboxesは get_grasp_coordinate() 済みであること
    """
    interval = 0.45
    pos_xa = 1.7
    pos_xb = pos_xa + interval
    pos_xc = pos_xb + interval

    # xa配列はcurrent_stpに関係している
    # 必ず列インデックス番号がcurrent_stpに対応する座標を返すようにする
    waypoints = {
        "xa": [[pos_xa, 2.5, 45], [pos_xa, 2.9, 45], [pos_xa, 3.3, 90]],
        "xb": [[pos_xb, 2.5, 90], [pos_xb, 2.9, 90], [pos_xb, 3.3, 90]],
        "xc": [[pos_xc, 2.5, 135], [pos_xc, 2.9, 135], [pos_xc, 3.3, 90]],
    }

    # posがxa,xb,xcのラインに近い場合は候補から削除
    is_to_xa = True
    is_to_xb = True
    is_to_xc = True
    for bbox in pos_bboxes:
        pos_x = bbox.x
        # TODO デバッグ時にコメントアウトを外す
        # rospy.loginfo("detected object obj.x = {:.2f}".format(bbox.x))

        # NOTE Hint:ｙ座標次第で無視してよいオブジェクトもある。
        if pos_x < pos_xa + (interval / 2):
            is_to_xa = False
            # rospy.loginfo("is_to_xa=False")
            continue
        elif pos_x < pos_xb + (interval / 2):
            is_to_xb = False
            # rospy.loginfo("is_to_xb=False")
            continue
        elif pos_x < pos_xc + (interval / 2):
            is_to_xc = False
            # rospy.loginfo("is_to_xc=False")
            continue

    x_line = None  # xa,xb,xcいずれかのリストが入る
    # NOTE 優先的にxcに移動する
    if is_to_xc:
        x_line = waypoints["xc"]
        rospy.loginfo("select next waypoint_xc")
    elif is_to_xb:
        x_line = waypoints["xb"]
        rospy.loginfo("select next waypoint_xb")
    elif is_to_xa:
        x_line = waypoints["xa"]
        rospy.loginfo("select next waypoint_xa")
    else:
        # a,b,cいずれにも移動できない場合
        x_line = waypoints["xb"]
        rospy.loginfo("select default waypoint")

    return x_line[current_stp]
