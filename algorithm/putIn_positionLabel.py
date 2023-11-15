foodCount = 0
positions = {}
# test comment

def init_putIn_positionLabel():
    global positions
    shapeItems_labels = [
        "credit_card_blank",
        "mini_soccer_ball",
        "softball",
        "baseball",
        "tennis_ball",
        "racquetball",
        "golf_ball",
        "marble",
        "cup",
        "foam_brick",
        "dice",
        "rope",
        "chain",
    ]

    food_labels = [
        "cracker_box",
        "sugar_box",
        "pudding_box",
        "gelatin_box",
        "potted_meat_can",
        "master_chef_can",
        "tuna_fish_can",
        "chips_can",
        "mustard_bottle",
        "tomato_soup_can",
        "banana",
        "strawberry",
        "apple",
        "lemon",
        "peach",
        "pear",
        "orange",
        "plum",
    ]

    kitchenItems_labels = [
        "windex_bottle",
        "bleach_cleanser",
        "sponge",
        "pitcher_base",
        "pitcher_lid",
        "plate",
        "bowl",
        "fork",
        "spoon",
        "spatula",
        "wine_glass",
        "mug",
    ]

    orientationBasedItems_labels = [
        "large_marker",
        "small_marker",
        "padlock",
        "bolt_and_nut",
        "clamp",
    ]

    taskItems_labels = [
        "rubiks_cube",
        "colored_wood_block",
        "nine_hole_peg_test",
        "toy_airplane",
        "lego_duplo",
        "magazine",
        "black_t_shirt",
        "timer",
    ]

    for obj in shapeItems_labels:
        positions[obj] = {"place": "Drawer", "deposit": "Drawer_left"}

    for obj in food_labels:
        positions[obj] = {"place": "Long_Table_A", "deposit": ""}

    for obj in kitchenItems_labels:
        positions[obj] = {"place": "Long_Table_A", "deposit": "Container_A"}

    for obj in orientationBasedItems_labels:
        positions[obj] = {"place": "Long_Table_A", "deposit": "Container_B"}

    for obj in taskItems_labels:
        positions[obj] = {"place": "Bin_A", "deposit": "Bin_A"}
    return positions


def get_putIn_positionLabel(positions, label):
    global foodCount
    if positions[label]["deposit"] == "":
        positions[label]["deposit"] = "Tray_A" if foodCount % 2 == 0 else "Tray_B"
        foodCount += 1
    return positions[label]
