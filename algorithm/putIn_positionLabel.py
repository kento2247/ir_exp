import json

# positionLabels_DIR_PATH = "./"  # degug
# positionLabels_FILE_PATH = "config/positionLabels.json"  # debug

positionLabels_DIR_PATH = "py2_ws/src/wrs_algorithm21/config/"
positionLabels_FILE_PATH = "positionLabels.json"

food_labels_call_count = 0

# JSONファイルを読み込んでdict型に変換
with open(positionLabels_DIR_PATH + positionLabels_FILE_PATH, "r") as file:
    positionLabels_dict = json.load(file)


def get_putIn_positionLabel(label):
    global food_labels_call_count
    target_position = positionLabels_dict[label]
    if target_position["deposit"] == "":
        target_position["deposit"] = (
            "Tray_A" if food_labels_call_count % 2 == 0 else "Tray_B"
        )
        food_labels_call_count += 1
    return target_position
