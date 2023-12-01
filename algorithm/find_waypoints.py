import heapq
from collections import deque

import matplotlib.pyplot as plt


class PathPlanning:
    result_waypoints = []

    def __init__(self, obstacle_coordinates):
        self.mesh_begin = {"x": 2.0, "y": 1.8}
        self.mesh_end = {"x": 3.2, "y": 3.5}
        self.mesh_resolution = 0.1
        self.obstacle_coordinates = obstacle_coordinates
        self.colision_width = 0.15
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

    def reconstruct_path(self, came_from, start, goal, waypoints):
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
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self, waypoints, start, goal):
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
                next = (current[0] + dx, current[1] + dy)
                if (
                    0 <= next[0] < self.x_time
                    and 0 <= next[1] < self.y_time
                    and waypoints[next[0]][next[1]][2] != 0
                ):
                    new_cost = cost_so_far[current] + 1
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + self.heuristic(goal, next)
                        heapq.heappush(frontier, (priority, next))
                        came_from[next] = current

        return came_from, cost_so_far


def get_waypoints(obstacle_coordinates):
    print(obstacle_coordinates)
    if obstacle_coordinates is None:
        return None
    # obstacle_coordinates = [
    #     {"x": 2.56485074506, "y": 2.43516755659, "z": 0.040733772599},
    #     {"x": 2.98526708458, "y": 2.77542427319, "z": 0.0266928948159},
    #     {"x": 2.98471341612, "y": 2.77432731505, "z": 0.0278568250358},
    # ]
    obstacle_list = [{"x": 2.1, "y": 2.1, "z": 0.0}]
    for i in obstacle_coordinates:
        print(i)
        obstacle_list.append({"x": i.x, "y": i.y, "z": 0.0})
    path_planning = PathPlanning(obstacle_list)

    filtered_waypoints = path_planning.get_waypoints()
    begin = (path_planning.begin_index["x"], path_planning.begin_index["y"])
    end = (path_planning.end_index["x"], path_planning.end_index["y"])

    came_from, cost_so_far = path_planning.a_star_search(filtered_waypoints, begin, end)

    filtered_waypoints = path_planning.reconstruct_path(
        came_from, begin, end, filtered_waypoints
    )

    # for i in range(path_planning.x_time):
    #     for j in range(path_planning.y_time):
    #         print(filtered_waypoints[i][j][2], end=",")
    #     print()

    # path_planning.plot_points_2d(filtered_waypoints)
    return (path_planning.result_waypoints)[::-1]
