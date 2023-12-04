food_labels_call_count = 0


def get_putIn_positionLabel(positionLabels_dict, label):
    global food_labels_call_count
    target_position = {}
    if label in positionLabels_dict:
        target_position = positionLabels_dict[label]
        if target_position["deposit"] == "":
            target_position["deposit"] = (
                "Tray_A" if food_labels_call_count % 2 == 0 else "Tray_B"
            )
            food_labels_call_count += 1
    else:
        print("position manager:\n  label: ", label, " is not found.")
        target_position = {"place": "Bin_B", "deposit": "Bin_B", "grasp": "above"}
    print("position manager:\n  target_position: ", target_position)
    return target_position
