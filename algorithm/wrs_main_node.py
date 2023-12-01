#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
the main program to operate a robot in WRS environment 
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import math
import os
import traceback
from select import select
from turtle import pos


from find_waypoints  import PathPlanning
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


class WrsMainController(object):
    """
    this class executes tasks under WRS simulation
    """

    IGNORE_LIST = [  # labels of omitted objects that asre hard to grasp
        "small_marker",
        "large_marker",
        "lego_duplo",
        "spatula",
        "nine_hole_peg_test",
        "plum",
    ]
    GRASP_TF_NAME = "object_grasping"
    GRASP_BACK_SAFE = {"z": 0.05, "xy": 0.3}
    GRASP_BACK = {"z": 0.05, "xy": 0.1}
    HAND_PALM_OFFSET = 0.05  # hand_palm_link is at the base of the hand so it needs an offset for grasping
    DETECT_CNT = 1
    TROFAST_Y_OFFSET = 0.3
    ignoreList = [
        "small_marker",
        "large_marker",
        "lego_duplo",
        "spatula",
        "nine_hole_peg_test",
        "plum",
    ]

    def __init__(self):
        # initialization of variables
        self.instruction_list = []
        self.detection_list = []

        # receiving of congifuration files
        self.coordinates = self.load_json(self.get_path(["config", "coordinates.json"]))
        self.poses = self.load_json(self.get_path(["config", "poses.json"]))
        self.positionLabels = self.load_json(
            self.get_path(["config", "positionLabels.json"])
        )

        # Initialization of ROS communication related factors
        tf_from_bbox_srv_name = "set_tf_from_bbox"
        rospy.wait_for_service(tf_from_bbox_srv_name)
        self.tf_from_bbox_clt = rospy.ServiceProxy(
            tf_from_bbox_srv_name, SetTransformFromBBox
        )

        obj_detection_name = "detection/get_object_detection"
        rospy.wait_for_service(obj_detection_name)
        self.detection_clt = rospy.ServiceProxy(obj_detection_name, GetObjectDetection)

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)

        self.instruction_sub = rospy.Subscriber(
            "/message", String, self.instruction_cb, queue_size=10
        )
        self.detection_sub = rospy.Subscriber(
            "/detect_msg", String, self.detection_cb, queue_size=10
        )

    @staticmethod
    def get_path(pathes, package="wrs_algorithm"):
        """
        Get a file path by specifying the ROS package name and the pathes to those files
        """
        if not pathes:  # check if the list is empty
            rospy.logerr("Can NOT resolve file path.")
            raise ValueError("You must specify the path to file.")
        pkg_path = rospkg.RosPack().get_path(package)
        path = os.path.join(*pathes)
        return os.path.join(pkg_path, path)

    @staticmethod
    def load_json(path):
        """
        Load JSON File Data as Dictionary Type
        No Change Needed
        """
        with open(path, "r") as json_file:
            return json.load(json_file)

    def instruction_cb(self, msg):
        """
        Receive instruction
        No Change Needed
        """
        rospy.loginfo("instruction received. [%s]", msg.data)
        self.instruction_list.append(msg.data)

    def detection_cb(self, msg):
        """
        Receive Detection Information
        No Change Needed
        """
        rospy.loginfo("received [Collision detected with %s]", msg.data)
        self.detection_list.append(msg.data)

    def get_relative_coordinate(self, parent, child):
        """
        Get Relative Coordinates using tf
        No Change Needed
        """
        try:
            # Wait Four Seconds, if each tf exists, set the relativity info
            trans = self.tf_buffer.lookup_transform(
                parent, child, rospy.Time.now(), rospy.Duration(2.0)
            )
            return trans.transform
        except (
            tf2_ros.LookupException,
            tf2_ros.ConnectivityException,
            tf2_ros.ExtrapolationException,
        ):
            log_str = "failed to get transform between [{}] and [{}]\n".format(
                parent, child
            )
            log_str += traceback.format_exc()
            rospy.logerr(log_str)
            return None

    def goto_name(self, name):
        """
        Move to a Specified Location by the Waypoint Name
        No Change Needed
        """
        if name in self.coordinates["positions"].keys():
            pos = self.coordinates["positions"][name]
            rospy.loginfo("go to [%s](%.2f, %.2f, %.2f)", name, pos[0], pos[1], pos[2])
            return omni_base.go_abs(pos[0], pos[1], pos[2])
        else:
            rospy.logerr("unknown waypoint name [%s]", name)
            return False

    def goto_pos(self, pos):
        """
        Go to (x, y) Coordinate Facing z Direction
        No Change Neede
        """
        rospy.loginfo("go to [raw_pos](%.2f, %.2f, %.2f)", pos[0], pos[1], pos[2])
        return omni_base.go_abs(pos[0], pos[1], pos[2])

    def change_pose(self, name):
        """
        Transform to a Specified Pose
        No Change Needed
        """
        if name in self.poses.keys():
            rospy.loginfo("change pose to [%s]", name)
            return whole_body.move_to_joint_positions(self.poses[name])

        rospy.logerr("unknown pose name [%s]", name)
        return False

    def check_positions(self):
        """
        読み込んだ座標ファイルの座標を巡回する
        Go Around the Coordinates From the Coordinate Files
        """
        whole_body.move_to_go()
        for wp_name in self.coordinates["routes"]["test"]:
            self.goto_name(wp_name)
            rospy.sleep(1)

    def get_latest_detection(self):
        """
        Wait till the Newest Recognition Data Arrives
        No Change Needed
        """
        res = self.detection_clt(GetObjectDetectionRequest())
        return res.bboxes

    def get_grasp_coordinate(self, bbox):
        """
        Get the Grasping Coordinate from BBox Information
        No Change Needed
        """
        # BBox情報からtfを生成して、座標を取得
        # Create tf from Bbox Info and get the Coordinates
        self.tf_from_bbox_clt.call(
            SetTransformFromBBoxRequest(bbox=bbox, frame=self.GRASP_TF_NAME)
        )
        rospy.sleep(1.0)  # Wait Untill tf Stabilizes
        return self.get_relative_coordinate("map", self.GRASP_TF_NAME).translation

    @classmethod
    def get_most_graspable_bbox(cls, obj_list):
        """
        Return the most graspable bbox
        No Change Needed
        """
        # if no object exists, return None
        obj = cls.get_most_graspable_obj(obj_list)
        if obj is None:
            return None
        return obj["bbox"]

    @classmethod
    def get_most_graspable_obj(cls, obj_list):
        """
        Return the Object with the Highest Graspable Scores
        """
        print("obj list: ", obj_list)
        extracted = []
        extract_str = "detected object list\n"
        ignore_str = ""
        for obj in obj_list:
            info_str = "{:<15}({:.2%}, {:3d}, {:3d}, {:3d}, {:3d})\n".format(
                obj.label, obj.score, obj.x, obj.y, obj.w, obj.h
            )
            if obj.label in cls.ignoreList:
                ignore_str += "- ignored  : " + info_str
            else:
                score = cls.calc_score_bbox(obj)
                extracted.append({"bbox": obj, "score": score, "label": obj.label})
                extract_str += "- extracted: {:07.3f} ".format(score) + info_str

        rospy.loginfo(extract_str + ignore_str)

        # Return the Object with the Highest Graspable Scores
        #
        for obj_info in sorted(extracted, key=lambda x: x["score"], reverse=True):
            obj = obj_info["bbox"]
            info_str = "{} ({:.2%}, {:3d}, {:3d}, {:3d}, {:3d})\n".format(
                obj.label, obj.score, obj.x, obj.y, obj.w, obj.h
            )
            rospy.loginfo("selected bbox: " + info_str)
            return obj_info

        # If no Object exist, return None
        return None

    @classmethod
    def calc_score_bbox(cls, bbox):
        """
        Calculate the detector_msgs/BBox Scores
        """
        gravity_x = bbox.x + bbox.w / 2
        gravity_y = bbox.y + bbox.h / 2
        xy_diff = abs(320 - gravity_x) / 320 + abs(360 - gravity_y) / 240

        return 1 / xy_diff

    @classmethod
    def get_second_best_graspable_bboxes_by_label(cls, obj_list, label):
        """
        Return the Bbox of the Second Most Graspable Object from Ones that Matches the label Name
        Filter the obj_list with the label name and run get_most_graspable_bbox()
        """
        match_objs = [obj for obj in obj_list if obj.label in label]
        if len(match_objs) < 2:
            rospy.logwarn("Cannot find enough objects which labeled with similar name.")
            return None
        sorted_objs = sorted(match_objs, key=lambda x: x.score, reverse=True)
        return sorted_objs[1].bbox

    @classmethod
    def get_most_graspable_bboxes_by_label(cls, obj_list, label):
        """
        Return the Bbox of the Most Graspable Object from Ones that Matches the label Name
        Filter the obj_list with the label name and run get_most_graspable_bbox()
        No Change Needed
        """
        match_objs = [obj for obj in obj_list if obj.label in label]
        if not match_objs:
            rospy.logwarn("Cannot find a object which labeled with similar name.")
            return None
        return cls.get_most_graspable_bbox(match_objs)

    @staticmethod
    def extract_target_obj_and_person(instruction):
        """
        指示文から対象となる物体名称と対象の人物を抽出する
        Extract the Target Object Name and the Person From The Instruction
        No Change Needed
        """
        rospy.loginfo("[extract_target_obj_and_person] instruction:" + instruction)

        parts = instruction.split(" to ")
        target_obj = parts[0]
        target_person = parts[1].split(" ")[1]

        return target_obj, target_person

    def grasp_from_side(self, pos_x, pos_y, pos_z, yaw, pitch, roll, preliminary="-y"):
        """
        Execute the Whole Grasping Motion
        Note: if you are creating an initial movement against "tall_table" set preliminary="-y"
        """
        if preliminary not in ["+y", "-y", "+x", "-x"]:
            raise RuntimeError(
                "unnkown graps preliminary type [{}]".format(preliminary)
            )

        rospy.loginfo("move hand to grasp (%.2f, %.2f, %.2f)", pos_x, pos_y, pos_z)

        grasp_back_safe = {"x": pos_x, "y": pos_y, "z": pos_z + self.GRASP_BACK["z"]}
        grasp_back = {"x": pos_x, "y": pos_y, "z": pos_z + self.GRASP_BACK["z"]}
        grasp_pos = {"x": pos_x, "y": pos_y, "z": pos_z}

        if "+" in preliminary:
            sign = 1
        elif "-" in preliminary:
            sign = -1

        if "x" in preliminary:
            grasp_back_safe["x"] += sign * self.GRASP_BACK_SAFE["xy"]
            grasp_back["x"] += sign * self.GRASP_BACK["xy"]
        elif "y" in preliminary:
            grasp_back_safe["y"] += sign * self.GRASP_BACK_SAFE["xy"]
            grasp_back["y"] += sign * self.GRASP_BACK["xy"]

        gripper.command(1)
        whole_body.move_end_effector_pose(
            grasp_back_safe["x"],
            grasp_back_safe["y"],
            grasp_back_safe["z"],
            yaw,
            pitch,
            roll,
        )
        whole_body.move_end_effector_pose(
            grasp_back["x"], grasp_back["y"], grasp_back["z"], yaw, pitch, roll
        )
        whole_body.move_end_effector_pose(
            grasp_pos["x"], grasp_pos["y"], grasp_pos["z"], yaw, pitch, roll
        )
        gripper.command(0)
        whole_body.move_end_effector_pose(
            grasp_back_safe["x"],
            grasp_back_safe["y"],
            grasp_back_safe["z"],
            yaw,
            pitch,
            roll,
        )

    def grasp_tuna_side(self, grasp_pos):
        """
        正面把持を行う
        ややアームを下に向けている
        微調整必要かも
        """
        grasp_pos.y -= self.HAND_PALM_OFFSET
        rospy.loginfo(
            "grasp_from_front_side (%.2f, %.2f, %.2f)",
            grasp_pos.x,
            grasp_pos.y,
            grasp_pos.z,
        )
        self.grasp_from_side(grasp_pos.x, grasp_pos.y, grasp_pos.z, -90, -120, 0, "-y")

    def grasp_from_front_side(self, grasp_pos):
        """
        Grasping from the Front
        The Arm is Tilting Downwards a Little
        Might Need Changes
        """
        grasp_pos.y -= self.HAND_PALM_OFFSET
        rospy.loginfo(
            "grasp_from_front_side (%.2f, %.2f, %.2f)",
            grasp_pos.x,
            grasp_pos.y,
            grasp_pos.z,
        )
        self.grasp_from_side(grasp_pos.x, grasp_pos.y, grasp_pos.z, -90, -100, 0, "-y")

    def grasp_from_upper_side(self, grasp_pos):
        """
        Grasping from Uppserside
        Grasps the Object from the Y-axis
        Might Need Changes
        """
        grasp_pos.z += self.HAND_PALM_OFFSET
        rospy.loginfo(
            "grasp_from_upper_side (%.2f, %.2f, %.2f)",
            grasp_pos.x,
            grasp_pos.y,
            grasp_pos.z,
        )
        self.grasp_from_side(grasp_pos.x, grasp_pos.y, grasp_pos.z, -90, -160, 0, "-y")
    
    def grasp_from_left_side(self, grasp_pos):
        grasp_pos.x += self.HAND_PALM_OFFSET
        rospy.loginfo(
            "grasp_from_left_side (%.2f, %.2f, %.2f)",
            grasp_pos.x,
            grasp_pos.y,
            grasp_pos.z,
        )
        self.grasp_from_side(grasp_pos.x, grasp_pos.y, grasp_pos.z, 0, -100, 0, "-x")

    def exec_graspable_method(self, grasp_pos, grasp_method, label=""):
        """
        task1: Decides the Grasping Motion from the positions
        Might Need Changes
        """
        method = None
        graspable_y = 1.85  # Can't Grasp Any Further
        desk_y = 1.5
        desk_z = 0.35

        # No Grasping Conditions
        if graspable_y < grasp_pos.y and desk_z > grasp_pos.z:
            return False
        
        if grasp_method == "above":
            method = self.grasp_from_left_side
        elif grasp_method == "front":
            method = self.grasp_from_front_side
        else:
            #not implemented yet
            method = self.grasp_from_left_side

        # if label in ["cup", "frisbee", "bowl"]:
        #     # Avoiding Bowl Sticking to the Arm
        #     method = self.grasp_from_upper_side
        # else:
        #     if desk_y < grasp_pos.y and desk_z > grasp_pos.z:
        #         # If the object is under the desk
        #         method = self.grasp_from_front_side
        #     else:
        #         method = self.grasp_from_upper_side

        method(grasp_pos)
        return True

    def put_in_place(self, place, into_pose):
        # 指定場所に入れ、all_neutral姿勢を取る
        # Put the object in a corresponding location and pose all_neutral
        self.change_pose("look_at_near_floor")
        self.goto_name(place)
        self.change_pose("all_neutral")
        self.change_pose(into_pose)
        gripper.command(1)
        rospy.sleep(5.0)
        self.change_pose("all_neutral")

    def pull_out_trofast(self, x, y, z, yaw, pitch, roll):
        # pull the trofast drawers
        y_back_offset = self.coordinates["drawer_positions"]["back_offset"]["y"]
        self.goto_pos([x, y + y_back_offset, -90])  # go to pulling position
        # self.goto_name("stair_like_drawer")  #goto_nameだとうまくいかない。pos
        self.change_pose("grasp_on_table")
        gripper.command(1)
        whole_body.move_end_effector_pose(
            x, y + self.TROFAST_Y_OFFSET, z, yaw, pitch, roll
        )
        whole_body.move_end_effector_pose(x, y, z, yaw, pitch, roll)
        gripper.command(0)
        whole_body.move_end_effector_pose(
            x, y + self.TROFAST_Y_OFFSET, z, yaw, pitch, roll
        )
        gripper.command(1)
        self.change_pose("all_neutral")

    def push_in_trofast(self, pos_x, pos_y, pos_z, yaw, pitch, roll):
        """
        push in the trofast drawers
        NOTE:Sample
            self.push_in_trofast(0.178, -0.29, 0.75, -90, 100, 0)
        """
        self.goto_name("stair_like_drawer")

        self.change_pose("grasp_on_table")
        pos_y += self.HAND_PALM_OFFSET

        # Getting ready & Pushing in the drawer
        whole_body.move_end_effector_pose(
            pos_x, pos_y + self.TROFAST_Y_OFFSET * 1.5, pos_z, yaw, pitch, roll
        )
        gripper.command(0)
        whole_body.move_end_effector_pose(
            pos_x, pos_y + self.TROFAST_Y_OFFSET, pos_z, yaw, pitch, roll
        )
        whole_body.move_end_effector_pose(pos_x, pos_y, pos_z, yaw, pitch, roll)

        self.change_pose("all_neutral")

    def deliver_to_target(self, target_obj, target_person):
        """
        Handing the Person the Object from the Shelf
        """
        self.change_pose("look_at_near_floor")
        self.goto_name("shelf")
        self.change_pose("look_at_shelf")

        rospy.loginfo("target_obj: " + target_obj + "  target_person: " + target_person)
        if target_obj == "master_chef_can":
            target_obj = "cracker_box"
        # Decides which bbox to grasp from the object detection result
        detected_objs = self.get_latest_detection()
        grasp_bbox = self.get_most_graspable_bboxes_by_label(
            detected_objs.bboxes, target_obj
        )
        if grasp_bbox is None:
            rospy.logwarn("Cannot find object to grasp. task2b is aborted.")
            return

        # Get the 3D coordinates of the bbox and grasp at that location
        grasp_pos = self.get_grasp_coordinate(grasp_bbox)
        self.change_pose("grasp_on_shelf")
        self.grasp_from_front_side(grasp_pos)
        self.change_pose("all_neutral")

        # Bring the object to the target_person
        self.change_pose("look_at_near_floor")
        if target_person == "left":
            self.goto_name("person_a")
        elif target_person == "right":
            self.goto_name("person_b")
        else:
            self.goto_name("person_a")
        self.change_pose("deliver_to_human")
        rospy.sleep(10.0)
        gripper.command(1)
        self.change_pose("all_neutral")

    def execute_avoid_blocks(self):
        # Avoid Obstacles
        path_planning_instance = PathPlanning(obstacle_coordinates)
        waypoints = path_planning_instance.get_waypoints()
        print("waypoints: ", waypoints)
        for i in waypoints:
            rospy.loginfo(i)
            self.goto_pos(i)
        """
        for i in range(3):
            detected_objs = self.get_latest_detection()
            bboxes = detected_objs.bboxes  # [{x:n,y:n,w:n,h:n,label:n,score:n}]
            # bboxes=[{x:n,y:n,w:n,h:n,label:n,score:n}]かな？
            pos_bboxes = [self.get_grasp_coordinate(bbox) for bbox in bboxes]
            print("detected_objs: ", detected_objs)
            print("bboxes: ", bboxes)
            print("pos_bboxes: ", pos_bboxes)
            waypoint = self.select_next_waypoint(i, pos_bboxes)
            # TODO remove the commentout to check the message
            rospy.loginfo(waypoint)
            self.goto_pos(waypoint)
        """

    def select_next_waypoint(self, current_stp, pos_bboxes):
        """
        Remove Objects that are Close to the Waypoints and Return the Optimal Waypoint.
        xa, xb, xc are Defined in the Order that is Closer to the Origin (x coordinates).
        Using bboxes as deciding factors to decide its desination (default is 0.45 aoart).
        pos_bboxes are to have already been used get_grasp_coordinate().
        """
        interval = 0.45
        pos_xa = 1.7
        pos_xb = pos_xa + interval
        pos_xc = pos_xb + interval

        # xa list is related to current_stp
        waypoints = {
            "xa": [[pos_xa, 2.5, 45], [pos_xa, 2.9, 45], [pos_xa, 3.3, 90]],
            "xb": [[pos_xb, 2.5, 90], [pos_xb, 2.9, 90], [pos_xb, 3.3, 90]],
            "xc": [[pos_xc, 2.5, 135], [pos_xc, 2.9, 135], [pos_xc, 3.3, 90]],
        }

        # posがxa,xb,xcのラインに近い場合は候補から削除
        # pos that is close to xa, xb, xc line will be deleted from
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

        x_line = None  # one of xa, xb, or xc is in here
        # NOTE Priortize xc
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
            # if we cannot move to neither a, b, or c
            x_line = waypoints["xb"]
            rospy.loginfo("select default waypoint")

        return x_line[current_stp]

    def goto_initial_place(self):
        self.goto_name("initial_place")
        self.change_pose("all_neutral")

    def open_drawer(self):
        drawer_positions = self.coordinates["drawer_positions"]
        # top_pos = drawer_positions["drawer_top"] #top does not open
        bottom_pos = drawer_positions["drawer_bottom"]
        left_pos = drawer_positions["drawer_left"]
        self.pull_out_trofast(
            left_pos["x"], left_pos["y"], left_pos["z"], -90, 100, 0
        )  # drawer left
        self.goto_initial_place()
        self.pull_out_trofast(
            bottom_pos["x"], bottom_pos["y"], bottom_pos["z"], -90, 100, 0
        )  # drawer right(top and bottom)

    def execute_task1(self):
        """
        task1を実行する
        """
        rospy.loginfo("#### start Task 1 ####")
        hsr_position = [  # Locations for robot to go around, and its poses
            ("initial_place", "look_at_near_floor"),
            ("tall_table", "look_at_tall_table"),
            ("near_long_table_l", "look_at_near_floor"),
            ("long_table_r", "look_at_long_table"),
        ]

        for plc, pose in hsr_position:
            while True:  # Loop until there are no objects in each of the places
                # Movements and Vision Navigations
                self.goto_name(plc)
                self.change_pose(pose)
                gripper.command(0)

                # Check if any graspable objects exist
                detected_objs = self.get_latest_detection()

                graspable_obj = self.get_most_graspable_obj(detected_objs.bboxes)

                if graspable_obj is None:
                    rospy.logwarn(
                        "Cannot determine object to grasp. Grasping is aborted."
                    )
                    break  # if there are no objects, escape the loop and move to the next location

                label = graspable_obj["label"]
                grasp_bbox = graspable_obj["bbox"]
                rospy.loginfo("grasp the " + label)

                place_obj = PLM.get_putIn_positionLabel(self.positionLabels, label)
                place = place_obj["place"]
                deposit = place_obj["deposit"]
                grasp_method = place_obj["grasp"]

                # If there exists any graspable objects, execute the grasping funciton
                grasp_pos = self.get_grasp_coordinate(grasp_bbox)
                self.change_pose("grasp_on_table")
                self.exec_graspable_method(grasp_pos, grasp_method, label)
                self.change_pose("all_neutral")

 
                self.put_in_place(deposit, "put_in_bin")

    def execute_task2a(self):
        """
        task2aを実行する
        障害物を避けながらroom1からroom2へ移動する
        """
        rospy.loginfo("#### start Task 2a ####")
        self.change_pose("look_at_near_floor")  # 下を見ないと物体検知できない
        gripper.command(0)  # close the hand
        self.change_pose("look_at_near_floor")
        self.goto_name("standby_2a")

        # Move Avoiding the Obstacles
        self.execute_avoid_blocks()

        self.goto_name("go_throw_2a")
        whole_body.move_to_go()

    def execute_task2b(self):
        """
        task2bを実行する
        """
        rospy.loginfo("#### start Task 2b ####")

        # Get the instruction
        if self.instruction_list:
            latest_instruction = self.instruction_list[-1]
            rospy.loginfo("recieved instruction: %s", latest_instruction)
        else:
            rospy.logwarn("instruction_list is None")
            return

        # Interpret the instrurction
        target_obj, target_person = self.extract_target_obj_and_person(
            latest_instruction
        )

        # Move the target object to target location
        if target_obj and target_person:
            self.deliver_to_target(target_obj, target_person)

    def run(self):
        """
        Execue All Tasks
        """
        self.goto_initial_place()
        # self.open_drawer()
        self.execute_task1()
        # self.execute_task2a()
        # self.execute_task2b()


def main():
    """
    Activate the Main Node to Execute Tasks in the WRS Environment
    """
    rospy.init_node("main_controller")
    try:
        ctrl = WrsMainController()
        rospy.loginfo("node initialized [%s]", rospy.get_name())

        # Check the task execution mode
        if rospy.get_param("~test_mode", default=False) is True:
            rospy.loginfo("#### start with TEST mode. ####")
        else:
            rospy.loginfo("#### start with NORMAL mode. ####")
            ctrl.run()

    except rospy.ROSInterruptException:
        pass


if __name__ == "__main__":
    main()
