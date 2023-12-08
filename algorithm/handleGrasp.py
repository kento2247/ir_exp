def exec_graspable_method(self, target_obj, detected_objs):
    """
    Module for handling grasping motions based on target object and surrounding objects.
    """
    graspable_y = 1.85
    desk_y = 1.5
    desk_z = 0.35

    if graspable_y < target_obj.y and desk_z > target_obj.z:
        return False
    obstacles = self.analyze_surroundings(target_obj, detected_objs)

    if obstacles['left']:
        method = self.grasp_from_right_side
    elif obstacles['right']:
        method = self.grasp_from_left_side
    elif obstacles['front']:
        method = self.grasp_from_upper_side
    else:
        method = self.grasp_from_front_side

    return method

def analyze_surroundings(self, target_obj, detected_objs):
    """
    Analyzes the surroundings of the target object to identify obstacles.
    """
    obstacles = {'left': False, 'right': False, 'front': False}
    for obj in detected_objs:
        if obj is not target_obj:
            # Check for obstacles on each side of the target object
            if obj.x < target_obj.x:  # Object is on the left
                obstacles['left'] = True
            elif obj.x > target_obj.x:  # Object is on the right
                obstacles['right'] = True
            if obj.y > target_obj.y:  # Object is in front
                obstacles['front'] = True

    return obstacles
