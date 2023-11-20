food_labels_call_count = 0


def get_putIn_positionLabel(positionLabels_dict, label):
    global food_labels_call_count
    target_position = positionLabels_dict[label]
    if target_position["deposit"] == "":
        target_position["deposit"] = (
            "Tray_A" if food_labels_call_count % 2 == 0 else "Tray_B"
        )
        food_labels_call_count += 1
    return target_position
