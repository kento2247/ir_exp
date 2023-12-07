class PositionLabelManager:
    """62114872 Amu Hata"""
    def __init__(self):
        self.positions = {}
        self.food_count = 0
        self.init_putIn_positionLabel()

    def init_putIn_positionLabel(self):
        shapeitems_labels = [
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

        kitchenitems_labels = [
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

        orientationbaseditems_labels = [
            "large_marker",
            "small_marker",
            "padlock",
            "bolt_and_nut",
            "clamp",
        ]

        taskitems_labels = [
            "rubiks_cube",
            "colored_wood_block",
            "nine_hole_peg_test",
            "toy_airplane",
            "lego_duplo",
            "magazine",
            "black_t_shirt",
            "timer",
        ]

        for obj in shapeitems_labels:
            self.positions[obj] = {"place": "Drawer", "deposit": "Drawer_left"}

        for obj in food_labels:
            self.positions[obj] = {"place": "Long_Table_A", "deposit": ""}

        for obj in kitchenitems_labels:
            self.positions[obj] = {"place": "Long_Table_A", "deposit": "Container_A"}

        for obj in orientationbaseditems_labels:
            self.positions[obj] = {"place": "Long_Table_A", "deposit": "Container_B"}

        for obj in taskitems_labels:
            self.positions[obj] = {"place": "Bin_A", "deposit": "Bin_A"}

    def get(self, label):
        if self.positions[label]["deposit"] == "":
            self.positions[label]["deposit"] = (
                "Tray_A" if self.food_count % 2 == 0 else "Tray_B"
            )
            self.food_count += 1
        return self.positions[label]
