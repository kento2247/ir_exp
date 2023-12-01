class PositionLabelManager:
    def __init__(self):
        self.positions = {}
        self.foodCount = 0
        self.init_putIn_positionLabel()

    def init_putIn_positionLabel(self):
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
         
        itemGrasp_labels = {
            "credit_card_blank":"ignore",
            "mini_soccer_ball":"above",
            "softball":"above",
            "baseball":"above",
            "tennis_ball":"above",
            "racquetball":"above",
            "golf_ball":"above",
            "marble":"above",
            "cup":"above",
            "foam_brick":"above",
            "dice":"above",
            "rope":"above",
            "chain":"above",
            "cracker_box":"side",
            "sugar_box":"above",
            "pudding_box":"above",
            "gelatin_box":"above",
            "potted_meat_can":"above",
            "master_chef_can":"above",
            "tuna_fish_can":"above",
            "chips_can":"above",
            "mustard_bottle":"above",
            "tomato_soup_can":"above",
            "banana":"above",
            "strawberry":"above",
            "apple":"above",
            "lemon":"above",
            "peach":"above",
            "pear":"above",
            "orange":"above",
            "plum":"above",
            "windex_bottle":"above",
            "bleach_cleanser":"above",
            "sponge":"above",
            "pitcher_base":"above",
            "pitcher_lid":"above",
            "plate":"above",
            "bowl":"above",
            "fork":"above",
            "spoon":"above",
            "spatula":"above",
            "wine_glass":"above",
            "mug":"above",
            "large_marker":"above",
            "small_marker":"above",
            "padlock":"above",
            "bolt_and_nut":"above",
            "clamp":"above",
            "rubiks_cube":"above",
            "colored_wood_block":"above",
            "nine_hole_peg_test":"above",
            "toy_airplane":"above",
            "lego_duplo":"above",
            "magazine":"above",
            "black_t_shirt":"above",
            "timer":"above"
        }

        for obj in shapeItems_labels:
            self.positions[obj] = {"place": "Drawer", "deposit": "Drawer_left"}

        for obj in food_labels:
            self.positions[obj] = {"place": "Long_Table_A", "deposit": ""}

        for obj in kitchenItems_labels:
            self.positions[obj] = {"place": "Long_Table_A", "deposit": "Container_A"}

        for obj in orientationBasedItems_labels:
            self.positions[obj] = {"place": "Long_Table_A", "deposit": "Container_B"}

        for obj in taskItems_labels:
            self.positions[obj] = {"place": "Bin_A", "deposit": "Bin_A"}

    def get(self, label):
        if self.positions[label]["deposit"] == "":
            self.positions[label]["deposit"] = (
                "Tray_A" if self.foodCount % 2 == 0 else "Tray_B"
            )
            self.foodCount += 1
        return self.positions[label]
