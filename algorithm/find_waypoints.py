import heapq
import math
from collections import deque

import matplotlib.pyplot as plt


class PathPlanning:
    """62112607 戸倉健登"""

    result_waypoints = []

    def __init__(self, obstacle_coordinates):
        self.mesh_begin = {"x": 1.9, "y": 1.8}
        self.mesh_end = {"x": 3.2, "y": 3.5}
        self.mesh_resolution = 0.04
        self.obstacle_coordinates = obstacle_coordinates
        self.obstacle_coordinates.append({"x": 1.9, "y": 2.1, "z": 0.0})
        # self.obstacle_coordinates.append({"x": 2.3, "y": 2.1, "z": 0.0})
        self.colision_width = 0.22
        self.begin_point = {"x": 2.5, "y": 1.85, "theta": 90}
        self.end_point = {"x": 2.0, "y": 3.5, "theta": 90}
        self.begin_index = {"x": 0, "y": 0}
        self.end_index = {"x": 0, "y": 0}

        self.x_length = abs(
            self.mesh_end["x"] - self.mesh_begin["x"] - self.colision_width * 1
        )
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

    def add_angle(self, waypoints):
        if waypoints is None:
            return None
        for i, point in enumerate(waypoints):
            if i < len(waypoints) - 1:
                next_point = waypoints[i + 1]
                angle = math.degrees(
                    math.atan2(next_point[0] - point[0], next_point[1] - point[1])
                )
                waypoints[i][2] = float(angle)

        # for i in waypoints:
        #     print(i)
        #     i[2] = float(90)

        return waypoints

    def plot_points_2d(self, waypoints):
        for i in range(self.x_time):
            for j in range(self.y_time):
                if waypoints[i][j][2] == 1:
                    plt.scatter(
                        j * self.mesh_resolution + self.mesh_begin["y"],
                        i * self.mesh_resolution + self.mesh_begin["x"],
                        c="blue",
                        marker="o",
                    )
                elif waypoints[i][j][2] == 4:
                    plt.scatter(
                        j * self.mesh_resolution + self.mesh_begin["y"],
                        i * self.mesh_resolution + self.mesh_begin["x"],
                        c="orange",
                        marker="o",
                    )

        obstacle_x, obstacle_y = zip(
            *[(point["x"], point["y"]) for point in self.obstacle_coordinates]
        )
        plt.scatter(obstacle_y, obstacle_x, c="red", marker="x")

        plt.scatter(
            self.begin_point["y"],
            self.begin_point["x"],
            c="green",
            marker="s",
        )

        plt.scatter(
            self.end_point["y"],
            self.end_point["x"],
            c="purple",
            marker="s",
        )

        plt.xlabel("Y")
        plt.ylabel("X")

        plt.gca().invert_yaxis()

        plt.grid(True)
        plt.show()

    def find_path(self, waypoints, old_x, old_y, move_x=0, move_y=0):
        """Find the path from the start to the end"""
        x = old_x + move_x
        y = old_y + move_y
        if waypoints[x][y][2] == 3:
            return waypoints
        else:
            if x - 1 >= 0 and waypoints[x - 1][y][2] == 1:
                waypoints[x][y][2] = 4
                return self.find_path(waypoints, x - 1, y, move_x, move_y)
            elif y - 1 >= 0 and waypoints[x][y - 1][2] == 1:
                waypoints[x][y][2] = 4
                return self.find_path(waypoints, x, y - 1, move_x, move_y)
            elif x + 1 < self.x_time and waypoints[x + 1][y][2] == 1:
                waypoints[x][y][2] = 4
                return self.find_path(waypoints, x + 1, y, move_x, move_y)
            elif y + 1 < self.y_time and waypoints[x][y + 1][2] == 1:
                waypoints[x][y][2] = 4
                return self.find_path(waypoints, x, y + 1, move_x, move_y)
            else:
                waypoints[x][y][2] = 0
                return waypoints

    def reconstruct_path(self, came_from, start, goal, waypoints):
        """Reconstruct the path from the start to the end"""
        current = goal
        start_value = waypoints[start[0]][start[1]][2]
        goal_value = waypoints[goal[0]][goal[1]][2]
        while current != start:
            waypoints[current[0]][current[1]][2] = 4
            self.result_waypoints.append(waypoints[current[0]][current[1]])
            current = came_from[current]
        waypoints[start[0]][start[1]][2] = start_value
        waypoints[goal[0]][goal[1]][2] = goal_value
        return waypoints

    def heuristic(self, a, b):
        """Calculate the heuristic for the A* algorithm"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self, waypoints, start, goal):
        """Perform the A* search algorithm"""
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_value = (current[0] + dx, current[1] + dy)
                if (
                    0 <= next_value[0] < self.x_time
                    and 0 <= next_value[1] < self.y_time
                    and waypoints[next_value[0]][next_value[1]][2] != 0
                ):
                    new_cost = cost_so_far[current] + 1
                    if (
                        next_value not in cost_so_far
                        or new_cost < cost_so_far[next_value]
                    ):
                        cost_so_far[next_value] = new_cost
                        priority = new_cost + self.heuristic(goal, next_value)
                        heapq.heappush(frontier, (priority, next_value))
                        came_from[next_value] = current
        return came_from, cost_so_far
