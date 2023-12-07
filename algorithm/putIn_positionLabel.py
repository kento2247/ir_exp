"""62114872 Amu Hata"""
FOOD_LABELS_CALL_COUNT = 0

def get_put_in_position_label(position_labels_dict, label):
    """
    62112607 戸倉健登
    get put in position label for struct
    """
    global FOOD_LABELS_CALL_COUNT
    target_position = {}
    if label in position_labels_dict:
        target_position = position_labels_dict[label]
        if target_position["deposit"] == "":
            target_position["deposit"] = (
                "Tray_A" if FOOD_LABELS_CALL_COUNT % 2 == 0 else "Tray_B"
            )
            FOOD_LABELS_CALL_COUNT += 1
    else:
        print("position manager:\n  label: ", label, " is not found.")
        target_position = {"place": "Bin_B", "deposit": "Bin_B", "grasp": "above"}
    print("position manager:\n  target_position: ", target_position)
    return target_position
