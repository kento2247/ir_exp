import heapq
import math

mesh_resolution = 0.1
mesh_begin = {"x": 2.0, "y": 1.85}
mesh_end = {"x": 3.3, "y": 3.5}

begin_point = {"x": 2.5, "y": 1.85, "theta": 90}
end_point = {"x": 2.0, "y": 3.5, "theta": 90}

x_length = abs(mesh_begin["x"] - mesh_end["x"])
y_length = abs(mesh_begin["y"] - mesh_end["y"])

x_time = int(x_length // mesh_resolution)
y_time = int(y_length // mesh_resolution)

colision_width = 0.2

obstacle_coordinates = [
    {"x": 2.56485074506, "y": 2.43516755659, "z": 0.040733772599},
    {"x": 2.98526708458, "y": 2.77542427319, "z": 0.0266928948159},
    {"x": 2.98471341612, "y": 2.77432731505, "z": 0.0278568250358},
]


def heuristic_cost_estimate(start, goal):
    return math.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def a_star_search(start, goal, obstacle_checker, mesh_resolution):
    open_set = []
    closed_set = set()
    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristic_cost_estimate(start, goal)}

    heapq.heappush(open_set, (f_score[start], start))

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        closed_set.add(current)

        for neighbor in get_neighbors(current, mesh_resolution):
            if neighbor in closed_set or obstacle_checker(*neighbor):
                continue

            tentative_g_score = g_score[current] + heuristic_cost_estimate(
                current, neighbor
            )

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(
                    neighbor, goal
                )
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found


def get_neighbors(point, mesh_resolution):
    x, y, _ = point
    neighbors = [
        (x + mesh_resolution, y, 0),
        (x - mesh_resolution, y, 0),
        (x, y + mesh_resolution, 0),
        (x, y - mesh_resolution, 0),
        (x + mesh_resolution, y + mesh_resolution, 0),
        (x - mesh_resolution, y - mesh_resolution, 0),
        (x + mesh_resolution, y - mesh_resolution, 0),
        (x - mesh_resolution, y + mesh_resolution, 0),
    ]
    return neighbors


# 障害物が存在するかどうかを判定する関数
def is_obstacle(x, y):
    for obstacle in obstacle_coordinates:
        if (
            abs(x - obstacle["x"]) < colision_width
            and abs(y - obstacle["y"]) < colision_width
        ):
            return True
    return False


# ゴール地点を指定
goal_point = (end_point["x"], end_point["y"], 0)

# A*アルゴリズムで最短経路を求める
shortest_path = a_star_search(
    (begin_point["x"], begin_point["y"], 0), goal_point, is_obstacle, mesh_resolution
)

print("Shortest Path:", shortest_path)
