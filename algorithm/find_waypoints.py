from collections import deque

import matplotlib.pyplot as plt


class PathPlanning:
    def __init__(self):
        # パラメータ設定
        self.mesh_begin = {"x": 2.0, "y": 1.8}
        self.mesh_end = {"x": 3.2, "y": 3.5}
        self.mesh_resolution = 0.1
        self.obstacle_coordinates = [
            {"x": 2.56485074506, "y": 2.43516755659, "z": 0.040733772599},
            {"x": 2.98526708458, "y": 2.77542427319, "z": 0.0266928948159},
            {"x": 2.98471341612, "y": 2.77432731505, "z": 0.0278568250358},
        ]
        self.obstacle_coordinates.append({"x": 2.1, "y": 2.1, "z": 0.0})  # 壁
        self.colision_width = 0.15
        self.begin_point = {"x": 2.5, "y": 1.85, "theta": 90}
        self.end_point = {"x": 2.0, "y": 3.5, "theta": 90}
        self.begin_index = {"x": 0, "y": 0}
        self.end_index = {"x": 0, "y": 0}

        self.x_length = abs(
            self.mesh_end["x"] - self.mesh_begin["x"] - self.colision_width * 1
        )  # 上下は壁があるため、colision_widthを1回引く
        self.y_length = abs(self.mesh_end["y"] - self.mesh_begin["y"])

        self.x_time = int(self.x_length // self.mesh_resolution) + 2
        self.y_time = int(self.y_length // self.mesh_resolution) + 2

    def is_obstacle(self, x, y):
        for obstacle in self.obstacle_coordinates:
            if (
                abs(x - obstacle["x"]) < self.colision_width
                and abs(y - obstacle["y"]) < self.colision_width
            ):
                return True
        return False

    def is_begin_point(self, x, y):
        if (
            abs(x - self.begin_point["x"]) < self.colision_width
            and abs(y - self.begin_point["y"]) < self.colision_width
        ):
            return True
        return False

    def is_end_point(self, x, y):
        if (
            abs(x - self.end_point["x"]) < self.colision_width
            and abs(y - self.end_point["y"]) < self.colision_width
        ):
            return True
        return False

    def get_waypoints(self):
        waypoints = []
        for i in range(self.x_time):
            new_row = []
            for j in range(self.y_time):
                x = self.mesh_begin["x"] + i * self.mesh_resolution
                y = self.mesh_begin["y"] + j * self.mesh_resolution

                if not self.is_obstacle(x, y):
                    new_row.append([x, y, 1])
                else:
                    new_row.append([x, y, 0])
                if self.is_begin_point(x, y):
                    self.begin_index["x"] = i - 1
                    self.begin_index["y"] = j - 1
                elif self.is_end_point(x, y):
                    self.end_index["x"] = i - 1
                    self.end_index["y"] = j - 1

            waypoints.append(new_row)
        waypoints[self.begin_index["x"]][self.begin_index["y"]][2] = 2
        waypoints[self.end_index["x"]][self.end_index["y"]][2] = 3
        return waypoints

    def plot_points_2d(self, waypoints):
        # waypoints をプロット
        waypoint_coords = [
            (point[1], point[0]) for row in waypoints for point in row if point[2] == 1
        ]
        waypoint_y, waypoint_x = zip(*waypoint_coords)
        plt.scatter(
            waypoint_y, waypoint_x, c="blue", marker="o", label="Waypoints"
        )  # XとYを入れ替え

        # obstacle_points をプロット
        obstacle_x, obstacle_y = zip(
            *[(point["x"], point["y"]) for point in self.obstacle_coordinates]
        )
        plt.scatter(
            obstacle_y, obstacle_x, c="red", marker="x", label="Obstacle Points"
        )  # XとYを入れ替え

        # begin_point をプロット
        plt.scatter(
            self.begin_point["y"],
            self.begin_point["x"],
            c="green",
            marker="s",
            label="Begin Point",
        )  # XとYを入れ替え

        # end_point をプロット
        plt.scatter(
            self.end_point["y"],
            self.end_point["x"],
            c="purple",
            marker="s",
            label="End Point",
        )  # XとYを入れ替え

        plt.xlabel("Y")  # XとYを入れ替えたのでラベルも変更
        plt.ylabel("X")

        plt.gca().invert_yaxis()  # X軸を反転させる

        plt.legend()
        plt.grid(True)
        plt.show()

        # 移動が妥当かどうかを判断するロジック
        x1, y1 = current
        x2, y2 = neighbor
        return (
            0 <= x2 < self.x_time
            and 0 <= y2 < self.y_time
            and waypoints[x2][y2][2] == 1
        )

    def find_path(self, waypoints, old_x, old_y, move_x, move_y):
        x = old_x + move_x
        y = old_y + move_y
        if waypoints[x][y][2] == 3:
            return waypoints
        else:
            if x - 1 >= 0 and waypoints[x - 1][y][2] == 1:
                waypoints[x][y][2] = 4
                return self.find_path(waypoints, x - 1, y)
            elif y - 1 >= 0 and waypoints[x][y - 1][2] == 1:
                waypoints[x][y][2] = 4
                return self.find_path(waypoints, x, y - 1)
            elif x + 1 < self.x_time and waypoints[x + 1][y][2] == 1:
                waypoints[x][y][2] = 4
                return self.find_path(waypoints, x + 1, y)
            elif y + 1 < self.y_time and waypoints[x][y + 1][2] == 1:
                waypoints[x][y][2] = 4
                return self.find_path(waypoints, x, y + 1)
            else:
                waypoints[x][y][2] = 0
                return waypoints


# クラスのインスタンス化
path_planning = PathPlanning()

# waypoints 取得
filtered_waypoints = path_planning.get_waypoints()
begin_x = path_planning.begin_index["x"]
begin_y = path_planning.begin_index["y"]
filtered_waypoints = path_planning.find_path(
    filtered_waypoints, begin_x, begin_y, -1, 0
)
for i in range(path_planning.x_time):
    for j in range(path_planning.y_time):
        print(filtered_waypoints[i][j][2], end=" ")
    print()


# 描画
# path_planning.plot_points_2d(filtered_waypoints)
