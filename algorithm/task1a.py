"""
3.5x4.0 area Living room
"""


def execute_task1(self):
    """
    task1を実行する
    """
    rospy.loginfo("#### start Task 1 ####")
    hsr_position = [  # 移動してほしい場所, ロボットの姿勢
        ("tall_table", "look_at_tall_table"),
        ("near_long_table_l", "look_at_near_floor"),
        ("long_table_r", "look_at_long_table"),
    ]

    for plc, pose in hsr_position:
        while True:  # 各場所で物体がなくなるまでループ
            # 移動と視線指示
            self.goto_name(plc)
            self.change_pose(pose)
            gripper.command(0)

            # 把持対象の有無チェック
            detected_objs = self.get_latest_detection()

            graspable_obj = self.get_most_graspable_obj(detected_objs.bboxes)

            if graspable_obj is None:
                rospy.logwarn("Cannot determine object to grasp. Grasping is aborted.")
                break  # 物体がなければループを抜けて次の場所へ移動

            label = graspable_obj["label"]
            grasp_bbox = graspable_obj["bbox"]
            rospy.loginfo("grasp the " + label)

            # 把持対象がある場合は把持関数実施
            grasp_pos = self.get_grasp_coordinate(grasp_bbox)
            self.change_pose("grasp_on_table")
            self.exec_graspable_method(grasp_pos, label)
            self.change_pose("all_neutral")

            place_obj = PLM.get_putIn_positionLabel(self.positionLabels, label)
            place = place_obj["place"]
            deposit = place_obj["deposit"]
            self.put_in_place(deposit, "put_in_bin")
