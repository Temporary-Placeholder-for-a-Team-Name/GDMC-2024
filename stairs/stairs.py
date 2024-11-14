from gdpc import Box, Editor, Block

from geometry.Point import Point
import time

from stairs.stairs_cube_approximation import stairs

global start_time
global elapsed_fill_time
global elapsed_pre_skeleton_time

import json

def json_to_list(file_path: str) -> list:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return [Point(value['x'], value['y'], value['z']) for value in data]
    except:
        print("error")
        return []

def export_to_json(points: list[Point], file_path: str):
    points_dict = [point.to_dict() for point in points]
    with open(file_path, 'w') as file:
        json.dump(points_dict, file, indent=4)

"""
Gets all the adjacent points separated to n block distance from a point
diagonal points are separated by sqrt(2)*n blocks but are not considered here
"""
def get_viable_adjacent_points_24_direction(point : Point, previous_point : Point, n : int) -> list['Point']:
    possible_values = [
        # extreme case not included for now
        #Point(0, n, 0),
        #Point(0, -n, 0),
        Point(n, 0, 0),
        Point(-n, 0, 0),
        Point(0, 0, n),
        Point(0, 0, -n),
        Point(n, n, 0),
        Point(n, -n, 0),
        Point(-n, n, 0),
        Point(-n, -n, 0),
        Point(n, 0, n),
        Point(n, 0, -n),
        Point(-n, 0, n),
        Point(-n, 0, -n),
        Point(0, n, n),
        Point(0, n, -n),
        Point(0, -n, n),
        Point(0, -n, -n),
        Point(n, n, n),
        Point(n, n, -n),
        Point(n, -n, n),
        Point(n, -n, -n),
        Point(-n, n, n),
        Point(-n, n, -n),
        Point(-n, -n, n),
        Point(-n, -n, -n),
    ]
    if previous_point is None:
        return [point + value for value in possible_values]

    direction = point - previous_point
    viable_adjacent_point = []

    for i in range(len(possible_values)):
        if direction.scalaire2D(possible_values[i]) >= 0:
            viable_adjacent_point.append(point + possible_values[i])

    return viable_adjacent_point

def get_viable_adjacent_points_6_direction(point : Point, previous_point : Point, n : int) -> list['Point']:
    possible_values = [
        # extreme case not included for now
        Point(0, n, 0),
        Point(0, -n, 0),
        Point(n, 0, 0),
        Point(-n, 0, 0),
        Point(0, 0, n),
        Point(0, 0, -n),
    ]
    return [point + value for value in possible_values]

def is_viable_adjacent_point(start_point, end_point, length_between_block):
    direction = (end_point - start_point) // length_between_block
    for i in range(1, length_between_block):
        selected_point = (start_point + direction * i)
        if any([editor.getBlock(selected_point.to_Vec2iLike(Point(0, i, 0))) != Block('minecraft:air') for i in range(4)]):
            return False
    return True

def box_contains_point(box: Box, point: Point) -> bool:
    return box.begin.x <= point.x <= box.last.x and box.begin.y <= point.y <= box.last.y and box.begin.z <= point.z <= box.last.z

def generate_path(current_point: Point, end_point: Point, area: Box, skeleton_path: list[Point], length_between_block: int) -> list[Point]:
    def heuristic(point1: Point, point2: Point) -> float:
        return point1.distance(point2)

    open_set = [(0, current_point)]
    g_scores = {current_point.position: 0}
    f_scores = {current_point.position: heuristic(current_point, end_point)}
    came_from = {current_point.position: None}
    visited = set()

    while open_set:
        # Find the point in open_set with the lowest f_score
        current_index = 0
        for i in range(len(open_set)):
            if f_scores[open_set[i][1].position] < f_scores[open_set[current_index][1].position]:
                current_index = i

        _, current_point = open_set.pop(current_index)

        if current_point.distance(end_point) <= length_between_block:
            path = []
            while current_point:
                path.append(current_point)
                current_point = came_from[current_point.position]
            return path[::-1]

        visited.add(current_point.position)
        for adjacent_point in get_viable_adjacent_points_24_direction(current_point, came_from[current_point.position], length_between_block):
            if not box_contains_point(area, adjacent_point) or adjacent_point.position in visited or adjacent_point in skeleton_path:
                continue

            # Here the place to add the different checks to see if the block is viable
            if not is_viable_adjacent_point(adjacent_point, current_point, length_between_block):
                continue

            tentative_g_score = g_scores[current_point.position] + 1
            if adjacent_point.position not in g_scores or tentative_g_score < g_scores[adjacent_point.position]:
                g_scores[adjacent_point.position] = tentative_g_score
                f_scores[adjacent_point.position] = tentative_g_score + heuristic(adjacent_point, end_point)
                open_set.append((f_scores[adjacent_point.position], adjacent_point))
                came_from[adjacent_point.position] = current_point

    print("No path found")
    return []

def generate_stairs_skeleton(starting_point: Point, end_point: Point, area: Box, length_between_block : int) -> list[Point]:
    #TODO fix box contains point
    #assert box_contains_point(area, starting_point), "The starting point is not in the area"
    #assert box_contains_point(area, end_point), "The end point is not in the area"

    #We prefer to have the starting point at the top of the stairs
    if starting_point.y < end_point.y:
        starting_point, end_point = end_point, starting_point

    skeleton_path = []
    current_point = starting_point
    pre_skeleton = generate_path(current_point, end_point, area, skeleton_path, length_between_block) # We have now a list of points to reach the end point

    global elapsed_pre_skeleton_time
    global start_time
    global elapsed_fill_time
    elapsed_pre_skeleton_time = time.time() - (start_time + elapsed_fill_time)
    print("pre_skeleton done in",  elapsed_pre_skeleton_time, "s")
    #We have to fill the pre_skeleton with block between
    for i in range(len(pre_skeleton) - 1):
        current_point = pre_skeleton[i]
        next_point = pre_skeleton[i + 1]
        direction = (next_point - current_point) // length_between_block
        for j in range (0, length_between_block):
            skeleton_path.append(current_point + direction * j)

    export_to_json(skeleton_path, "skeleton_path.json")
    return skeleton_path

if __name__ == "__main__":
    global start_time
    global elapsed_fill_time
    start_time = time.time()
    editor = Editor(buffering=True)
    buildArea = editor.getBuildArea()
    coordinates_min = [min(buildArea.begin[i], buildArea.last[i]) for i in range(3)]
    coordinates_max = [max(buildArea.begin[i], buildArea.last[i]) for i in range(3)]

    start = Point(327, 85, 75)
    end = Point(334, 110, 61)
    blocks = {
        "wall": "blackstone",
        "roof": "blackstone",
        "roof_slab": "blackstone_slab",
        "door": "oak_door",
        "window": "glass_pane",
        "entrance": "oak_door",
        "stairs": "quartz_stairs",
        "stairs_slab": "quartz_slab",
        "celling": "quartz_block",
        "floor": "quartz_block",
        "celling_slab": "quartz_slab",
        "garden_outline": "oak_leaves",
        "garden_floor": "grass_block"
    }
    length = Point(abs(coordinates_max[0] - coordinates_min[0]), abs(coordinates_max[1] - coordinates_min[1]), abs(coordinates_max[2] - coordinates_min[2]))

    to_delete = json_to_list("skeleton_path.json")
    print(to_delete)
    for a in to_delete:
        editor.placeBlock((a.x, a.y, a.z), Block('air'))

    elapsed_fill_time = time.time() - start_time
    print("fill with air in :", elapsed_fill_time, "s")

    p = generate_stairs_skeleton(start, end, buildArea, 3)
    print("skeleton_finition made in :", time.time() - (start_time + elapsed_fill_time + elapsed_pre_skeleton_time), "s")

    for a in p:
        editor.placeBlock(a.to_Vec2iLike(), Block('redstone_block'))
    editor.flushBuffer()
