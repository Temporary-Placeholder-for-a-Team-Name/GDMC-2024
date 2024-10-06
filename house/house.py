from gdpc import Editor, Block, geometry
import numpy as np
import math

import itertools as it


def generate_new_coordinate_component(new_length_component, length_component, coordinate_component,
                                      max_coordinate_component, min_coordinate_component):
    if max(min_coordinate_component + 1, coordinate_component - new_length_component) > min(
            max_coordinate_component - new_length_component, coordinate_component + length_component):
        new_x = np.random.randint(
            min(max_coordinate_component - new_length_component, coordinate_component + length_component),
            max(min_coordinate_component + 1, coordinate_component - new_length_component))
    else:
        new_x = np.random.randint(max(min_coordinate_component + 1, coordinate_component - new_length_component),
                                  min(max_coordinate_component - new_length_component,
                                      coordinate_component + length_component))
    return new_x


def generate_new_length_component(length_component):
    if length_component > 7:
        new_width = np.random.randint(5, length_component - 2)
    elif length_component == 7:
        new_width = 5
    else:
        new_width = np.random.randint(length_component - 2, 5)
    return new_width


def calcul_height_roof(length):
    if length <= 5:
        n = 1
    elif length <= 10:
        n = 2
    else:
        n = 3
    return n


class House:
    def __init__(self, editor, coordinates_min, coordinates_max, direction, list_block):
        self.editor = editor
        self.coordinates_min = coordinates_min
        self.coordinates_max = coordinates_max
        self.skeleton = []

        size = [(coordinates_max[i] - coordinates_min[i]) + 10 for i in range(3)]

        self.grid3d = np.zeros(size, dtype=[('bool', bool), ('int', int)])

        self.nbEtage = (coordinates_max[1] - coordinates_min[1]) // 5

        self.direction = direction

        self.entranceWall = None

        self.blocks = list_block

        self.entranceCo = None

        self.wall = Block(list_block["wall"])
        self.roof = Block(list_block["roof"])
        self.roof_slab = Block(list_block["roof_slab"])
        self.door = Block(list_block["door"])
        self.window = Block(list_block["window"])
        self.entrance = Block(list_block["entrance"])
        self.stairs = Block(list_block["stairs"])
        self.celling = Block(list_block["celling"])
        self.floor = Block(list_block["floor"])
        self.celling_slab = Block(list_block["celling_slab"])
        self.gardenOutline = Block(list_block["garden_outline"])
        self.garden_floor = Block(list_block["garden_floor"])

    def create_house_skeleton(self):
        self.delete()
        x_min, y_min, z_min = self.coordinates_min
        x_max, y_max, z_max = self.coordinates_max

        perimeter_width = x_max - x_min
        perimeter_depth = z_max - z_min

        x_min += 1
        z_min += 1
        x_max -= 2
        z_max -= 2
        if x_min + 1 > x_max:
            x = np.random.randint(x_max, x_min + 1)
        else:
            x = np.random.randint(x_min + 1, x_max)

        if z_min + 1 > z_max:
            z = np.random.randint(z_max, z_min + 1)
        else:
            z = np.random.randint(z_min + 1, z_max)

        width = perimeter_width // 2
        depth = perimeter_depth // 2
        height = y_max - y_min

        if x + width - 1 > x_max:
            x = x_max - width
        if z + depth - 1 > z_max:
            z = z_max - depth

        x_plan3d = x - x_min
        z_plan3d = z - z_min

        geometry.placeCuboid(self.editor, (x, y_min, z), (x + width - 1, y_min, z + depth - 1), self.floor)
        x_range = slice(x_plan3d, x_plan3d + width - 1)
        z_range = slice(z_plan3d, z_plan3d + depth - 1)
        self.grid3d[x_range, 0, z_range] = True, 1

        self.skeleton.append((x, z, width - 1, depth - 1, height))
        print("Coordinates of the corners: ", (x, z), (x, z + depth - 1),
              (x + width - 1, z), (x + width - 1, z + depth - 1))

        x_min -= 1
        x_max -= 1
        z_min += 1
        z_max += 1

        for _ in range(3):
            print("Rectangle n°", _ + 1, "en cours de création")

            for a in range(10000):
                new_width = generate_new_length_component(width)
                new_x = generate_new_coordinate_component(new_width, width, x, x_max, x_min)
                new_x_plan3d = new_x - x_min - 1

                new_depth = generate_new_length_component(depth)
                new_z = generate_new_coordinate_component(new_depth, depth, z, z_max, z_min)
                new_z_plan3d = new_z - z_min + 1

                adjacent_blocks = 0
                for i in range(new_x_plan3d, new_x_plan3d + new_width):
                    for j in range(new_z_plan3d, new_z_plan3d + new_depth):
                        if self.grid3d[i - 1, 0, j]['bool'] and self.grid3d[i - 1, 0, j]['int'] == 1 or \
                                self.grid3d[i + 1, 0, j]['bool'] and self.grid3d[i + 1, 0, j]['int'] == 1 or \
                                self.grid3d[i, 0, j - 1]['bool'] and self.grid3d[i, 0, j - 1]['int'] == 1 or \
                                self.grid3d[i, 0, j + 1]['bool'] and self.grid3d[i, 0, j + 1]['int'] == 1:
                            adjacent_blocks += 1

                new_x_range = slice(new_x_plan3d, new_x_plan3d + new_width)
                new_z_range = slice(new_z_plan3d, new_z_plan3d + new_depth)
                if adjacent_blocks < 3 or np.any(self.grid3d[new_x_range, 0, new_z_range]['bool']):
                    continue

                geometry.placeCuboid(self.editor, (new_x, y_min, new_z),
                                     (new_x + new_width - 1, y_min, new_z + new_depth - 1), self.floor)
                new_x_plan3d += 1
                new_z_plan3d -= 1
                new_x_range = slice(new_x_plan3d, new_x_plan3d + new_width)
                new_z_range = slice(new_z_plan3d, new_z_plan3d + new_depth)
                self.grid3d[new_x_range, 0, new_z_range] = True, 2

                self.skeleton.append((new_x, new_z, new_width, new_depth, height))
                break

            else:
                print("Failed to place rectangle after 100000 attempts.")

    def delete(self):
        geometry.placeCuboid(self.editor, self.coordinates_min,
                             self.coordinates_max, Block("air"))

    def put_wall_on_skeleton(self):
        for k in range(len(self.skeleton)):
            x, z, width, depth, height = self.skeleton[k]

            if k > 0:
                x += 1
                z += 1
                width -= 2
                depth -= 2
            x_plan3d = x - self.coordinates_min[0]
            z_plan3d = z - self.coordinates_min[2]
            for i, j, y in it.product(range(-1, width + 1), range(-1, depth + 1), range(height)):
                if i == -1 or i == width or j == -1 or j == depth and \
                        (not (self.grid3d[x_plan3d + i, y, z_plan3d + j]['bool']) and
                         not (self.grid3d[x_plan3d + i, y, z_plan3d + j]['int'] == 1) or
                         (self.grid3d[x_plan3d + i, y, z_plan3d + j]['bool'] and
                          self.grid3d[x_plan3d + i, y, z_plan3d + j]['int'] == 2) or
                         y == 0):
                    self.editor.placeBlock((x + i, self.coordinates_min[1] + y, z + j), self.wall)
                    self.grid3d[x_plan3d + i, y, z_plan3d + j] = True

    def get_adjacent_walls(self):

        main_rect = self.skeleton[0]
        x_main, z_main, width_main, depth_main, heigt_main = main_rect
        adjacent_walls = []
        width_main -= 1
        depth_main -= 1

        for k in range(1, len(self.skeleton)):
            x, z, width, depth, heigt = self.skeleton[k]

            walls = [(x, z, x + width - 1, z), (x, z, x, z + depth - 1),
                     (x, z + depth - 1, x + width - 1, z + depth - 1), (x + width - 1, z, x + width - 1, z + depth - 1)]
            for wall in walls:
                x1, z1, x2, z2 = wall
                if (x_main <= x1 <= x_main + width_main or x_main <= x2 <= x_main + width_main) and (
                        z_main - 1 == z1 or z_main + depth_main + 1 == z1):
                    x1 = max(x1, x_main - 1)
                    x2 = min(x2, x_main + width_main + 1)
                    if abs(x2 - x1) > 1:
                        adjacent_walls.append((x1, z1, x2, z2))
                elif (z_main <= z1 <= z_main + depth_main or z_main <= z2 <= z_main + depth_main) and (
                        x_main - 1 == x1 or x_main + width_main + 1 == x1):
                    z1 = max(z1, z_main - 1)
                    z2 = min(z2, z_main + depth_main + 1)
                    if abs(z2 - z1) > 1:
                        adjacent_walls.append((x1, z1, x2, z2))

        return adjacent_walls

    def place_door(self):
        walls = self.get_adjacent_walls()
        for wall in walls:
            for i in range(self.nbEtage):
                x_min, z_min, x_max, z_max = wall
                if x_min == x_max:
                    width = z_max - z_min
                    if width % 2 != 0:
                        door_pos = width // 2
                        for y in range(self.coordinates_min[1] + 1 + i * 4, self.coordinates_min[1] + 3 + i * 4):
                            self.editor.placeBlock(
                                (x_min, y, z_min + door_pos), Block("air"))
                            self.editor.placeBlock(
                                (x_min, y, z_min + door_pos + 1), Block("air"))
                    else:
                        door_pos = width // 2
                        for y in range(self.coordinates_min[1] + 1 + i * 4, self.coordinates_min[1] + 3 + i * 4):
                            self.editor.placeBlock(
                                (x_min, y, z_min + door_pos), Block("air"))
                else:
                    width = x_max - x_min
                    if width % 2 != 0:
                        door_pos = width // 2
                        for y in range(self.coordinates_min[1] + 1 + i * 4, self.coordinates_min[1] + 3 + i * 4):
                            self.editor.placeBlock(
                                (x_min + door_pos, y, z_min), Block("air"))
                            self.editor.placeBlock(
                                (x_min + door_pos + 1, y, z_min), Block("air"))

                    else:
                        door_pos = width // 2
                        for y in range(self.coordinates_min[1] + 1 + i * 4, self.coordinates_min[1] + 3 + i * 4):
                            self.editor.placeBlock(
                                (x_min + door_pos, y, z_min), Block("air"))

    def place_roof(self):
        for k in range(len(self.skeleton) - 1, -1, -1):
            x, z, width, depth, height = self.skeleton[k]

            if k != 0:
                x += 1
                z += 1
                width -= 2
                depth -= 2
                n = calcul_height_roof(width if width < depth else depth)

            else:
                n = width // 4 if width > depth else depth // 4

            x_plan3d = x - self.coordinates_min[0]
            z_plan3d = z - self.coordinates_min[2]

            print(width, depth, n)

            if width < depth:
                self.create_middle_upper_roof_line(width, n, depth, x, z)
            else:
                self.create_middle_upper_roof_line(depth, n, width, x, z)

            print('-----------------------------------')

            for i in range(-1, width + 1):
                for j in range(-1, depth + 1):
                    if width < depth:
                        if (width % 2 != 0) & (i == width // 2):
                                self.editor.placeBlock((x + i, self.coordinates_max[1] + n, z + j),
                                                       Block(self.blocks["roof_slab"], {"type": "bottom"}))
                                self.grid3d[x_plan3d + i,height + n, z_plan3d + j] = True
                                if j == -1:
                                    self.create_roof_block(height, i, j, n, x, x_plan3d, z, z_plan3d)

                                elif j == depth:
                                    self.create_roof_block(height, i, j, n, x, x_plan3d, z, z_plan3d)
                    else:
                        if (depth % 2 != 0) and (j == depth // 2):
                                self.editor.placeBlock((x + i, self.coordinates_max[1] + n, z + j),
                                                       Block(self.blocks["roof_slab"], {"type": "bottom"}))
                                self.grid3d[x_plan3d + i,height + n, z_plan3d + j] = True
                                if i == -1:
                                    self.create_roof_block(height, i - 1, j + 1, n, x, x_plan3d, z, z_plan3d)

                                elif i == width:
                                    self.create_roof_block(height, i + 1, j + 1, n, x, x_plan3d, z, z_plan3d)

            if width < depth:

                h = 0
                for i in range(-1, width // 2):
                    for j in range(-1, depth + 1):
                        if i != -1:
                            if h % 1 == 0:
                                self.editor.placeBlock((x + i, math.ceil(self.coordinates_max[1] + h), z + j),
                                                       Block(self.blocks["roof_slab"], {"type": "top"}))
                                self.editor.placeBlock(
                                    (x + width - 1 - i, math.ceil(self.coordinates_max[1] + h), z + j),
                                    Block(self.blocks["roof_slab"], {"type": "top"}))
                                self.grid3d[x_plan3d + i,
                                round(height + h), z_plan3d + j] = True
                                self.grid3d[x_plan3d + width - 1 - i,
                                round(height + h), z_plan3d + j] = True

                                if j == -1:

                                    self.editor.placeBlock((x + i, math.ceil(self.coordinates_max[1] + h), z + j - 1),
                                                           self.celling)
                                    self.editor.placeBlock(
                                        (x + width - 1 - i, math.ceil(self.coordinates_max[1] + h), z + j - 1),
                                        self.celling)
                                    self.grid3d[x_plan3d + i,
                                    round(height + h), z_plan3d + j - 1] = True
                                    self.grid3d[x_plan3d + width - 1 - i,
                                    round(height + h), z_plan3d + j - 1] = True
                                elif j == depth:
                                    self.editor.placeBlock((x + i, math.ceil(self.coordinates_max[1] + h), z + j + 1),
                                                           self.celling)
                                    self.editor.placeBlock(
                                        (x + width - 1 - i, math.ceil(self.coordinates_max[1] + h), z + j + 1),
                                        self.celling)
                                    self.grid3d[x_plan3d + i,
                                    round(height + h), z_plan3d + j + 1] = True
                                    self.grid3d[x_plan3d + width - 1 - i,
                                    round(height + h), z_plan3d + j + 1] = True
                            else:
                                self.editor.placeBlock((x + i, math.ceil(self.coordinates_max[1] + h), z + j),
                                                       Block(self.blocks["roof_slab"], {"type": "bottom"}))
                                self.editor.placeBlock(
                                    (x + width - 1 - i, math.ceil(self.coordinates_max[1] + h), z + j),
                                    Block(self.blocks["roof_slab"], {"type": "bottom"}))
                                self.editor.placeBlock(
                                    (x + i, math.ceil(self.coordinates_max[1] + h - 0.5), z + j), self.roof)
                                self.editor.placeBlock(
                                    (x + width - 1 - i, math.ceil(self.coordinates_max[1] + h - 0.5), z + j),
                                    self.roof)

                                self.grid3d[x_plan3d + i,
                                round(height + h + 0.5), z_plan3d + j] = True
                                self.grid3d[x_plan3d + width - 1 - i,
                                round(height + h + 0.5), z_plan3d + j] = True
                                self.grid3d[x_plan3d + i,
                                round(height + h - 0.5), z_plan3d + j] = True
                                self.grid3d[x_plan3d + width - 1 - i,
                                round(height + h - 0.5), z_plan3d + j] = True

                                if j == -1:
                                    self.editor.placeBlock((x + i, math.ceil(self.coordinates_max[1] + h), z + j - 1),
                                                           Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                    self.editor.placeBlock(
                                        (x + width - 1 - i, math.ceil(self.coordinates_max[1] + h), z + j - 1),
                                        Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                    self.editor.placeBlock(
                                        (x + i, math.ceil(self.coordinates_max[1] + h - 1), z + j - 1),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.editor.placeBlock(
                                        (x + width - 1 - i,
                                         math.ceil(self.coordinates_max[1] + h - 1), z + j - 1),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))

                                    self.grid3d[x_plan3d + i,
                                    round(height + h - 1), z_plan3d + j - 1] = True
                                    self.grid3d[
                                        x_plan3d + width - 1 - i, round(height + h - 1), z_plan3d + j - 1] = True
                                    self.grid3d[x_plan3d + i,
                                    round(height + h), z_plan3d + j - 1] = True
                                    self.grid3d[x_plan3d + width - 1 - i,
                                    round(height + h), z_plan3d + j - 1] = True
                                elif j == depth:
                                    self.editor.placeBlock((x + i, math.ceil(self.coordinates_max[1] + h), z + j + 1),
                                                           Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                    self.editor.placeBlock(
                                        (x + width - 1 - i, math.ceil(self.coordinates_max[1] + h), z + j + 1),
                                        Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                    self.editor.placeBlock(
                                        (x + i, math.ceil(self.coordinates_max[1] + h - 1), z + j + 1),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.editor.placeBlock(
                                        (x + width - 1 - i,
                                         math.ceil(self.coordinates_max[1] + h - 1), z + j + 1),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))

                                    self.grid3d[x_plan3d + i,
                                    round(height + h - 1), z_plan3d + j + 1] = True
                                    self.grid3d[
                                        x_plan3d + width - 1 - i, round(height + h - 1), z_plan3d + j + 1] = True
                                    self.grid3d[x_plan3d + i,
                                    round(height + h), z_plan3d + j + 1] = True
                                    self.grid3d[x_plan3d + width - 1 - i,
                                    round(height + h), z_plan3d + j + 1] = True
                        else:
                            self.editor.placeBlock((x + i, math.ceil(self.coordinates_max[1] + h), z + j),
                                                   Block(self.blocks["roof_slab"], {"type": "bottom"}))
                            self.editor.placeBlock((x + width - 1 - i, math.ceil(self.coordinates_max[1] + h), z + j),
                                                   Block(self.blocks["roof_slab"], {"type": "bottom"}))

                            self.grid3d[x_plan3d + i,
                            round(height + h), z_plan3d + j] = True
                            self.grid3d[x_plan3d + width - 1 - i,
                            round(height + h), z_plan3d + j] = True

                            if j == -1:
                                self.editor.placeBlock((x + i, math.ceil(self.coordinates_max[1] + h), z + j - 1),
                                                       Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                self.editor.placeBlock(
                                    (x + width - 1 - i, math.ceil(self.coordinates_max[1] + h), z + j - 1),
                                    Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                if not self.grid3d[x_plan3d + i, height + h - 1, z_plan3d + j - 1]:
                                    self.editor.placeBlock(
                                        (x + i, math.ceil(self.coordinates_max[1] + h - 1), z + j - 1),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.grid3d[x_plan3d + i, height +
                                                h - 1, z_plan3d + j - 1] = True
                                if not self.grid3d[x_plan3d + width - 1 - i, height + h - 1, z_plan3d + j - 1]:
                                    self.editor.placeBlock(
                                        (x + width - 1 - i,
                                         math.ceil(self.coordinates_max[1] + h - 1), z + j - 1),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.grid3d[x_plan3d + width - 1 - i,
                                                height + h - 1, z_plan3d + j - 1] = True

                                self.grid3d[x_plan3d + i,
                                round(height + h - 1), z_plan3d + j - 1] = True
                                self.grid3d[x_plan3d + width - 1 - i,
                                round(height + h - 1), z_plan3d + j - 1] = True
                            elif j == depth:
                                self.editor.placeBlock((x + i, math.ceil(self.coordinates_max[1] + h), z + j + 1),
                                                       Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                self.editor.placeBlock(
                                    (x + width - 1 - i, math.ceil(self.coordinates_max[1] + h), z + j + 1),
                                    Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                if not self.grid3d[x_plan3d + i, height + h - 1, z_plan3d + j + 1]:
                                    self.editor.placeBlock(
                                        (x + i, math.ceil(self.coordinates_max[1] + h - 1), z + j + 1),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.grid3d[x_plan3d + i, height +
                                                h - 1, z_plan3d + j + 1] = True
                                if not self.grid3d[x_plan3d + width - 1 - i, height + h - 1, z_plan3d + j + 1]:
                                    self.editor.placeBlock(
                                        (x + width - 1 - i,
                                         math.ceil(self.coordinates_max[1] + h - 1), z + j + 1),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.grid3d[x_plan3d + width - 1 - i,
                                                height + h - 1, z_plan3d + j + 1] = True

                                self.grid3d[x_plan3d + i,
                                round(height + h - 1), z_plan3d + j + 1] = True
                                self.grid3d[x_plan3d + width - 1 - i,
                                round(height + h - 1), z_plan3d + j + 1] = True
                    if i != -1:
                        h += 0.5
            else:

                h = 0
                for i in range(-1, depth // 2):
                    for j in range(-1, width + 1):
                        if i != -1:
                            if h % 1 == 0:
                                self.editor.placeBlock((x + j, math.ceil(self.coordinates_max[1] + h), z + i),
                                                       Block(self.blocks["roof_slab"], {"type": "top"}))
                                self.editor.placeBlock(
                                    (x + j, math.ceil(self.coordinates_max[1] + h), z + depth - 1 - i),
                                    Block(self.blocks["roof_slab"], {"type": "top"}))

                                self.grid3d[x_plan3d + j,
                                round(height + h), z_plan3d + i] = True
                                self.grid3d[x_plan3d + j,
                                round(height + h), z_plan3d + depth - 1 - i] = True

                                if j == -1:
                                    self.editor.placeBlock((x + j - 1, math.ceil(self.coordinates_max[1] + h), z + i),
                                                           self.celling)
                                    self.editor.placeBlock(
                                        (x + j - 1, math.ceil(self.coordinates_max[1] + h), z + depth - 1 - i),
                                        self.celling)

                                    self.grid3d[x_plan3d + j - 1,
                                    round(height + h), z_plan3d + i] = True
                                    self.grid3d[x_plan3d + j - 1,
                                    round(height + h), z_plan3d + depth - 1 - i] = True
                                elif j == width:
                                    self.editor.placeBlock((x + j + 1, math.ceil(self.coordinates_max[1] + h), z + i),
                                                           self.celling)
                                    self.editor.placeBlock(
                                        (x + j + 1, math.ceil(self.coordinates_max[1] + h), z + depth - 1 - i),
                                        self.celling)

                                    self.grid3d[x_plan3d + j + 1,
                                    round(height + h), z_plan3d + i] = True
                                    self.grid3d[x_plan3d + j + 1,
                                    round(height + h), z_plan3d + depth - 1 - i] = True

                            else:
                                self.editor.placeBlock((x + j, math.ceil(self.coordinates_max[1] + h), z + i),
                                                       Block(self.blocks["roof_slab"], {"type": "bottom"}))
                                self.editor.placeBlock(
                                    (x + j, math.ceil(self.coordinates_max[1] + h), z + depth - 1 - i),
                                    Block(self.blocks["roof_slab"], {"type": "bottom"}))
                                self.editor.placeBlock(
                                    (x + j, math.ceil(self.coordinates_max[1] + h - 0.5), z + i), self.roof)
                                self.editor.placeBlock(
                                    (x + j, math.ceil(self.coordinates_max[1] + h - 0.5), z + depth - 1 - i),
                                    self.roof)

                                self.grid3d[x_plan3d + j,
                                round(height + h + 0.5), z_plan3d + i] = True
                                self.grid3d[x_plan3d + j, round(
                                    height + h + 0.5), z_plan3d + depth - 1 - i] = True
                                self.grid3d[x_plan3d + j,
                                round(height + h - 0.5), z_plan3d + i] = True
                                self.grid3d[x_plan3d + j,
                                round(height + h - 0.5), z_plan3d + depth - 1 - i] = True

                                if j == -1:
                                    self.editor.placeBlock((x + j - 1, math.ceil(self.coordinates_max[1] + h), z + i),
                                                           Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                    self.editor.placeBlock(
                                        (x + j - 1, math.ceil(self.coordinates_max[1] + h), z + depth - 1 - i),
                                        Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                    self.editor.placeBlock(
                                        (x + j - 1, math.ceil(self.coordinates_max[1] + h - 1), z + i),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.editor.placeBlock(
                                        (x + j - 1, math.ceil(
                                            self.coordinates_max[1] + h - 1), z + depth - 1 - i),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))

                                    self.grid3d[x_plan3d + j - 1,
                                    round(height + h), z_plan3d + i] = True
                                    self.grid3d[x_plan3d + j - 1,
                                    round(height + h), z_plan3d + depth - 1 - i] = True
                                    self.grid3d[x_plan3d + j - 1,
                                    round(height + h - 1), z_plan3d + i] = True
                                    self.grid3d[x_plan3d + j - 1, round(
                                        height + h - 1), z_plan3d + depth - 1 - i] = True
                                elif j == width:
                                    self.editor.placeBlock((x + j + 1, math.ceil(self.coordinates_max[1] + h), z + i),
                                                           Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                    self.editor.placeBlock(
                                        (x + j + 1, math.ceil(self.coordinates_max[1] + h), z + depth - 1 - i),
                                        Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                    self.editor.placeBlock(
                                        (x + j + 1, math.ceil(self.coordinates_max[1] + h - 1), z + i),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.editor.placeBlock(
                                        (x + j + 1, math.ceil(
                                            self.coordinates_max[1] + h - 1), z + depth - 1 - i),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))

                                    self.grid3d[x_plan3d + j + 1,
                                    round(height + h), z_plan3d + i] = True
                                    self.grid3d[x_plan3d + j + 1,
                                    round(height + h), z_plan3d + depth - 1 - i] = True
                                    self.grid3d[x_plan3d + j + 1,
                                    round(height + h - 1), z_plan3d + i] = True
                                    self.grid3d[x_plan3d + j + 1, round(
                                        height + h - 1), z_plan3d + depth - 1 - i] = True
                        else:
                            self.editor.placeBlock((x + j, math.ceil(self.coordinates_max[1] + h), z + i),
                                                   Block(self.blocks["roof_slab"], {"type": "bottom"}))
                            self.editor.placeBlock((x + j, math.ceil(self.coordinates_max[1] + h), z + depth - 1 - i),
                                                   Block(self.blocks["roof_slab"], {"type": "bottom"}))

                            self.grid3d[x_plan3d + j,
                            round(height + h), z_plan3d + i] = True
                            self.grid3d[x_plan3d + j,
                            round(height + h), z_plan3d + depth - 1 - i] = True

                            if j == -1:
                                self.editor.placeBlock((x + j - 1, math.ceil(self.coordinates_max[1] + h), z + i),
                                                       Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                self.editor.placeBlock(
                                    (x + j - 1, math.ceil(self.coordinates_max[1] + h), z + depth - 1 - i),
                                    Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                if not self.grid3d[x_plan3d + j - 1, height + h - 1, z_plan3d + i]:
                                    self.editor.placeBlock(
                                        (x + j - 1, math.ceil(self.coordinates_max[1] + h - 1), z + i),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.grid3d[x_plan3d + j - 1,
                                                height + h - 1, z_plan3d + i] = True
                                if not self.grid3d[x_plan3d + j - 1, height + h - 1, z_plan3d + depth - 1 - i]:
                                    self.editor.placeBlock(
                                        (x + j - 1, math.ceil(
                                            self.coordinates_max[1] + h - 1), z + depth - 1 - i),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.grid3d[x_plan3d + j - 1, height +
                                                h - 1, z_plan3d + depth - 1 - i] = True

                                self.grid3d[x_plan3d + j - 1,
                                round(height + h), z_plan3d + i] = True
                                self.grid3d[x_plan3d + j - 1,
                                round(height + h), z_plan3d + depth - 1 - i] = True
                            elif j == width:
                                self.editor.placeBlock((x + j + 1, math.ceil(self.coordinates_max[1] + h), z + i),
                                                       Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                self.editor.placeBlock(
                                    (x + j + 1, math.ceil(self.coordinates_max[1] + h), z + depth - 1 - i),
                                    Block(self.blocks["celling_slab"], {"type": "bottom"}))
                                if not self.grid3d[x_plan3d + j + 1, height + h - 1, z_plan3d + i]:
                                    self.editor.placeBlock(
                                        (x + j + 1, math.ceil(self.coordinates_max[1] + h - 1), z + i),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.grid3d[x_plan3d + j + 1,
                                                height + h - 1, z_plan3d + i] = True
                                if not self.grid3d[x_plan3d + j + 1, height + h - 1, z_plan3d + depth - 1 - i]:
                                    self.editor.placeBlock(
                                        (x + j + 1, math.ceil(
                                            self.coordinates_max[1] + h - 1), z + depth - 1 - i),
                                        Block(self.blocks["celling_slab"], {"type": "top"}))
                                    self.grid3d[x_plan3d + j + 1, height + h -
                                                1, z_plan3d + depth - 1 - i] = True

                                self.grid3d[x_plan3d + j + 1,
                                round(height + h), z_plan3d + i] = True
                                self.grid3d[x_plan3d + j + 1,
                                round(height + h), z_plan3d + depth - 1 - i] = True

                            self.grid3d[x_plan3d + j,
                            round(height + h), z_plan3d + i] = True
                            self.grid3d[x_plan3d + j,
                            round(height + h), z_plan3d + depth - 1 - i] = True

                    if i != -1:
                        h += 0.5

            QUARTZ_SLAB = Block(self.blocks["celling_slab"], {"type": "top"})

            for i in range(-2, width + 2):
                for j in range(-2, depth + 2):
                    if i == -2 or i == width + 1 or j == -2 or j == depth + 1:
                        if not self.grid3d[x_plan3d + i, height - 1, z_plan3d + j]['bool']:
                            if width < depth:
                                if i == -2 or i == width + 1:
                                    self.editor.placeBlock((x + i, self.coordinates_max[1] - 1, z + j), QUARTZ_SLAB)

                            else:
                                if j == -2 or j == depth + 1:
                                    self.editor.placeBlock((x + i, self.coordinates_max[1] - 1, z + j), QUARTZ_SLAB)

    def create_middle_upper_roof_line(self, depth, n, width, x, z):
        if n > 1:
            for k in range(n):
                for i in range(-1, width + 1):
                    for y in range(-1, depth // 2 + 1 - k):
                        self.editor.placeBlock(
                            (x + i, self.coordinates_max[1] + k, z + y + k + 2), self.roof)
                        self.editor.placeBlock(
                            (x + i, self.coordinates_max[1] + k, z + depth - y - 1 - k - 2), self.roof)
        else:
            if depth % 2 == 0:
                for i in range(-1, width + 1):
                    for y in range(2):
                        self.editor.placeBlock(
                            (x + i, self.coordinates_max[1] + n - 1, z + depth // 2 - 1 + y), self.roof)
            else:
                for i in range(-1, width + 1):
                    self.editor.placeBlock(
                        (x + i, self.coordinates_max[1] + n - 1, z + depth // 2), self.roof)

    def create_roof_block(self, height, i, j, n, x, x_plan3d, z, z_plan3d):
        if not self.grid3d[x_plan3d + i, height + n, z_plan3d + j - 1]:
            self.editor.placeBlock((x + i, self.coordinates_max[1] + n, z + j - 1),
                                   Block(self.blocks["celling_slab"], {"type": "bottom"}))
            self.grid3d[x_plan3d + i, height +
                        n, z_plan3d + j - 1] = True
        if not self.grid3d[x_plan3d + i, height + n - 1, z_plan3d + j - 1]:
            self.editor.placeBlock((x + i, self.coordinates_max[1] + n - 1, z + j - 1),
                                   Block(self.blocks["celling_slab"], {"type": "top"}))
            self.grid3d[x_plan3d + i, height +
                        n - 1, z_plan3d + j - 1] = True

    def put_celling(self):
        for k in range(0, len(self.skeleton)):
            x, z, width, depth, height = self.skeleton[k]

            if k != 0:
                x += 1
                z += 1
                width -= 2
                depth -= 2
            x_plan3d = x - self.coordinates_min[0]
            z_plan3d = z - self.coordinates_min[2]
            for y in range(1, self.nbEtage + 1):
                for i in range(0, width):
                    for j in range(0, depth):
                        self.editor.placeBlock((x + i, self.coordinates_min[1] + 4 * y, z + j), self.celling)
                        self.grid3d[x_plan3d + i, 4 * y, z_plan3d + j] = True

    def get_all_extern_walls(self):
        walls = []
        adjacent_walls = self.get_adjacent_walls()
        for k in range(0, len(self.skeleton)):
            x, z, width, depth, height = self.skeleton[k]
            if k == 0:
                x -= 1
                z -= 1
                width += 2
                depth += 2

            walls.append((x, z, x + width - 1, z))
            walls.append((x, z, x, z + depth - 1))
            walls.append((x, z + depth - 1, x + width - 1, z + depth - 1))
            walls.append((x + width - 1, z, x + width - 1, z + depth - 1))

        walls_to_keep = []
        for wall in walls:
            remove_wall = False
            for adj_wall in adjacent_walls:
                if self.is_inside_all(wall, adj_wall):
                    remove_wall = True
                    break
            if not remove_wall:
                walls_to_keep.append(wall)

        return walls_to_keep

    def is_inside_all(self, big_wall, small_wall):
        x1, z1, x2, z2 = big_wall
        x3, z3, x4, z4 = small_wall
        if x1 == x2 == x3 == x4:
            return x1 == x3 and z1 <= z3 and z4 <= z2
        elif z1 == z2 == z3 == z4:
            return z1 == z3 and x1 <= x3 and x4 <= x2

    def place_window_on_wall(self, wall, axis, is_x):
        for l in range(self.nbEtage):
            y_offset = self.coordinates_min[1] + 2 + l * 4
            if axis % 2 == 0:
                if axis == 4:
                    positions = [(2, 0), (3, 0)] if is_x else [(0, 3), (0, 2)]
                else:
                    positions = [(1 + i * 4, 0) for i in range(math.ceil(axis / 4))] if is_x else [(0, 1 + i * 4) for i
                                                                                                   in range(
                            math.ceil(axis / 4))]
            else:
                positions = [(1 + i, 0) for i in range(axis)] if axis <= 5 else [(i * 2 + 1, 0) for i in
                                                                                 range(math.ceil(axis / 2))]

            for pos in positions:
                x_offset, z_offset = pos
                if is_x:
                    self.editor.placeBlock((wall[0] + x_offset, y_offset, wall[1]), self.window)
                else:
                    self.editor.placeBlock((wall[0], y_offset, wall[1] + x_offset), self.window)
                    
    def place_window(self):
        walls = self.get_all_extern_walls()
        for wall in walls:
            x1, z1, x2, z2 = wall
            x = abs(x2 - x1) - 1
            z = abs(z2 - z1) - 1
            if x1 == x2:
                self.place_window_on_wall(wall, z, False)
            elif z1 == z2:
                self.place_window_on_wall(wall, x, True)

    def place_stairs(self):
        x, z, width, depth, height = self.skeleton[0]
        x_moy = x + width // 2
        z_moy = z + depth // 2
        slab_up = Block(self.blocks["stairs_slab"], {"type": "top"})
        slab_down = Block(self.blocks["stairs_slab"], {"type": "bottom"})

        for i in range(self.nbEtage - 1):
            # Clear a 3x3 area for the stairs
            for k in range(3):
                for l in range(3):
                    self.editor.placeBlock((x_moy - 1 + k, self.coordinates_min[1] + 4 * (i + 1), z_moy - 1 + l),
                                           Block("air"))

            # Place the floor blocks
            for j in range(1, 5):
                self.editor.placeBlock((x_moy, self.coordinates_min[1] + 4 * i + j, z_moy), self.floor)

            # Place the stairs slabs
            self.editor.placeBlock((x_moy - 1, self.coordinates_min[1] + 1 + 4 * i, z_moy - 1), slab_down)
            self.editor.placeBlock((x_moy, self.coordinates_min[1] + 1 + 4 * i, z_moy - 1), slab_up)
            self.editor.placeBlock((x_moy + 1, self.coordinates_min[1] + 2 + 4 * i, z_moy - 1), slab_down)
            self.editor.placeBlock((x_moy + 1, self.coordinates_min[1] + 2 + 4 * i, z_moy), slab_up)
            self.editor.placeBlock((x_moy + 1, self.coordinates_min[1] + 3 + 4 * i, z_moy + 1), slab_down)
            self.editor.placeBlock((x_moy, self.coordinates_min[1] + 3 + 4 * i, z_moy + 1), slab_up)
            self.editor.placeBlock((x_moy - 1, self.coordinates_min[1] + 4 + 4 * i, z_moy + 1), slab_down)
            self.editor.placeBlock((x_moy - 1, self.coordinates_min[1] + 4 + 4 * i, z_moy), slab_up)

    def wall_facing_direction(self):

        if self.direction == "N":
            closest_wall = min(self.skeleton, key=lambda wall: wall[1])
            wall = (closest_wall[0], closest_wall[1],
                    closest_wall[0] + closest_wall[2], closest_wall[1])
        elif self.direction == "S":
            closest_wall = max(
                self.skeleton, key=lambda wall: wall[1] + wall[3])
            wall = (closest_wall[0], closest_wall[1] + closest_wall[3], closest_wall[0] + closest_wall[2],
                    closest_wall[1] + closest_wall[3])
        elif self.direction == "E":
            closest_wall = max(
                self.skeleton, key=lambda wall: wall[0] + wall[2])
            wall = (closest_wall[0] + closest_wall[2], closest_wall[1], closest_wall[0] + closest_wall[2],
                    closest_wall[1] + closest_wall[3])
        elif self.direction == "W":
            closest_wall = min(self.skeleton, key=lambda wall: wall[0])
            wall = (closest_wall[0], closest_wall[1],
                    closest_wall[0], closest_wall[1] + closest_wall[3])
        else:
            return []

        if closest_wall != self.skeleton[0]:
            if wall[0] == wall[2]:
                wall = (wall[0] - 1, wall[1] + 1, wall[2] - 1, wall[3] - 2)

            elif wall[1] == wall[3]:

                wall = (wall[0] + 1, wall[1] - 1, wall[2] - 2, wall[3] - 1)
        else:
            if wall[0] == wall[2]:
                if self.direction == "W":
                    wall = (wall[0] - 2, wall[1], wall[2] - 2, wall[3])
                else:
                    wall = (wall[0], wall[1] + 1, wall[2], wall[3] - 2)

            elif wall[1] == wall[3]:

                if self.direction == "N":
                    wall = (wall[0] + 1, wall[1] - 2, wall[2] - 2, wall[3] - 2)
                else:
                    wall = (wall[0] + 1, wall[1], wall[2] - 2, wall[3])

        return wall

    def place_entrance(self):
        wall = self.wall_facing_direction()

        self.entranceWall = wall
        match self.direction:
            case "W":
                if (wall[3] - wall[1]) % 2 != 0:
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 1, (wall[1] + wall[3]) // 2 + 1),
                                           Block("air"))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 2, (wall[1] + wall[3]) // 2 + 1),
                                           Block("air"))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 1, (wall[1] + wall[3]) // 2),
                                           Block("air"))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 2, (wall[1] + wall[3]) // 2),
                                           Block("air"))

                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2),
                                           Block(self.blocks["stairs"], {"facing": "east"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks["stairs"], {"facing": "east"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks["stairs"], {"facing": "south"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 2),
                                           Block(self.blocks["stairs"], {"facing": "north"}))

                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2),
                                           Block(self.blocks["stairs"], {"facing": "east", "half": "top"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks["stairs"], {"facing": "east", "half": "top"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks["stairs"], {"facing": "south", "half": "top"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 2),
                                           Block(self.blocks["stairs"], {"facing": "north", "half": "top"}))

                    self.entranceCo = (
                        (wall[1] + wall[3]) // 2, (wall[1] + wall[3]
                                                   ) // 2 + 2, (wall[1] + wall[3]) // 2 + 1,
                        (wall[1] + wall[3]) // 2 - 1)

                else:
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 1, (wall[1] + wall[3]) // 2),
                                           Block("air"))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 2, (wall[1] + wall[3]) // 2),
                                           Block("air"))

                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2),
                                           Block(self.blocks["stairs"], {"facing": "east"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks["stairs"], {"facing": "north"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks["stairs"], {"facing": "south"}))

                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2),
                                           Block(self.blocks["stairs"], {"facing": "east", "half": "top"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks["stairs"], {"facing": "north", "half": "top"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks["stairs"], {"facing": "south", "half": "top"}))

                    self.entranceCo = (
                        (wall[1] + wall[3]) // 2, (wall[1] + wall[3]
                                                   ) // 2 + 1, (wall[1] + wall[3]) // 2 + 1,
                        (wall[1] + wall[3]) // 2 - 1)

            case "N":
                if (wall[2] - wall[0]) % 2 != 0:
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1] + 1, wall[1] + 1),
                        Block("air"))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1] + 2, wall[1] + 1),
                        Block("air"))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 1, wall[1] + 1), Block("air"))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 2, wall[1] + 1), Block("air"))

                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks["stairs"], {"facing": "south"}))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2 + 1, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks["stairs"], {"facing": "south"}))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2 - 1, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks["stairs"], {"facing": "east"}))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2 + 2, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks["stairs"], {"facing": "west"}))

                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 3, wall[1]),
                                           Block(self.blocks["stairs"], {"facing": "south", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1] + 3, wall[1]),
                        Block(self.blocks["stairs"], {"facing": "south", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1] + 3, wall[1]),
                        Block(self.blocks["stairs"], {"facing": "east", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 2,
                         self.coordinates_min[1] + 3, wall[1]),
                        Block(self.blocks["stairs"], {"facing": "west", "half": "top"}))

                    self.entranceCo = (wall[0] + (wall[2] - wall[0]) // 2, wall[0] + (wall[2] - wall[0]) // 2 + 2,
                                       wall[0] + (wall[2] - wall[0]) // 2 + 1, wall[0] + (wall[2] - wall[0]) // 2 - 1)

                else:
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 1, wall[1] + 1), Block("air"))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 2, wall[1] + 1), Block("air"))

                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks["stairs"], {"facing": "south"}))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2 + 1, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks["stairs"], {"facing": "west"}))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2 - 1, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks["stairs"], {"facing": "east"}))

                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 3, wall[1]),
                                           Block(self.blocks["stairs"], {"facing": "south", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1] + 3, wall[1]),
                        Block(self.blocks["stairs"], {"facing": "west", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1] + 3, wall[1]),
                        Block(self.blocks["stairs"], {"facing": "east", "half": "top"}))

                    self.entranceCo = (wall[0] + (wall[2] - wall[0]) // 2, wall[0] + (wall[2] - wall[0]) // 2 + 1,
                                       wall[0] + (wall[2] - wall[0]) // 2 + 1, wall[0] + (wall[2] - wall[0]) // 2 - 1)

            case "E":
                if (wall[3] - wall[1]) % 2 != 0:
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 1, (wall[1] + wall[3]) // 2 + 1),
                                           Block("air"))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 2, (wall[1] + wall[3]) // 2 + 1),
                                           Block("air"))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 1, (wall[1] + wall[3]) // 2),
                                           Block("air"))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 2, (wall[1] + wall[3]) // 2),
                                           Block("air"))

                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2),
                                           Block(self.blocks["stairs"], {"facing": "west"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks["stairs"], {"facing": "west"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks["stairs"], {"facing": "south"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 2),
                                           Block(self.blocks["stairs"], {"facing": "north"}))

                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2),
                                           Block(self.blocks["stairs"], {"facing": "west", "half": "top"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks["stairs"], {"facing": "west", "half": "top"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks["stairs"], {"facing": "south", "half": "top"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 2),
                                           Block(self.blocks["stairs"], {"facing": "north", "half": "top"}))

                    self.entranceCo = (
                        (wall[1] + wall[3]) // 2, (wall[1] + wall[3]
                                                   ) // 2 + 2, (wall[1] + wall[3]) // 2 + 1,
                        (wall[1] + wall[3]) // 2 - 1)
                else:
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 1, (wall[1] + wall[3]) // 2),
                                           Block("air"))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 2, (wall[1] + wall[3]) // 2),
                                           Block("air"))

                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2),
                                           Block(self.blocks["stairs"], {"facing": "west"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks["stairs"], {"facing": "north"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks["stairs"], {"facing": "south"}))

                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2),
                                           Block(self.blocks["stairs"], {"facing": "west", "half": "top"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks["stairs"], {"facing": "north", "half": "top"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks["stairs"], {"facing": "south", "half": "top"}))

                    self.entranceCo = (
                        (wall[1] + wall[3]) // 2, (wall[1] + wall[3]
                                                   ) // 2 + 1, (wall[1] + wall[3]) // 2 + 1,
                        (wall[1] + wall[3]) // 2 - 1)

            case "S":
                print(wall)
                if (wall[2] - wall[0]) % 2 != 0:
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1, self.coordinates_min[1] + 1, wall[1]), Block("air"))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1, self.coordinates_min[1] + 2, wall[1]), Block("air"))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 1, wall[1]),
                                           Block("air"))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 2, wall[1]),
                                           Block("air"))

                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1], wall[1] + 1),
                                           Block(self.blocks["stairs"], {"facing": "north"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1], wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "north"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1], wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "east"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 2,
                         self.coordinates_min[1], wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "west"}))

                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "north", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "north", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "east", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 2,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "west", "half": "top"}))

                    self.entranceCo = (wall[0] + (wall[2] - wall[0]) // 2, wall[0] + (wall[2] - wall[0]) // 2 + 2,
                                       wall[0] + (wall[2] - wall[0]) // 2 + 1, wall[0] + (wall[2] - wall[0]) // 2 - 1)
                else:
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 1, wall[1]),
                                           Block("air"))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 2, wall[1]),
                                           Block("air"))

                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1], wall[1] + 1),
                                           Block(self.blocks["stairs"], {"facing": "north"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1], wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "west"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1], wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "east"}))

                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "north", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "west", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks["stairs"], {"facing": "east", "half": "top"}))

                    self.entranceCo = (wall[0] + (wall[2] - wall[0]) // 2, wall[0] + (wall[2] - wall[0]) // 2 + 1,
                                       wall[0] + (wall[2] - wall[0]) // 2 + 1, wall[0] + (wall[2] - wall[0]) // 2 - 1)
            case _:
                pass

    def place_garden_outline(self):
        x_min, y_min, z_min = self.coordinates_min
        x_max, y_max, z_max = self.coordinates_max
        for i in range(x_min, x_max):
            for y in range(z_min, z_max):
                if i == x_min or i == x_max - 1 or y == z_min or y == z_max - 1:
                    match self.direction:
                        case "N":
                            if not (i in self.entranceCo and y == z_min):
                                self.editor.placeBlock(
                                    (i, y_min - 1, y), Block("oak_log"))
                                self.editor.placeBlock(
                                    (i, y_min, y), self.gardenOutline)
                                self.editor.placeBlock(
                                    (i, y_min + 1, y), self.gardenOutline)
                                self.editor.placeBlock(
                                    (i, y_min + 2, y), self.gardenOutline)
                        case "S":
                            if not (i in self.entranceCo and y == z_max - 1):
                                self.editor.placeBlock(
                                    (i, y_min - 1, y), Block("oak_log"))
                                self.editor.placeBlock(
                                    (i, y_min, y), self.gardenOutline)
                                self.editor.placeBlock(
                                    (i, y_min + 1, y), self.gardenOutline)
                                self.editor.placeBlock(
                                    (i, y_min + 2, y), self.gardenOutline)
                        case "E":
                            if not (i == x_max - 1 and y in self.entranceCo):
                                self.editor.placeBlock(
                                    (i, y_min - 1, y), Block("oak_log"))
                                self.editor.placeBlock(
                                    (i, y_min, y), self.gardenOutline)
                                self.editor.placeBlock(
                                    (i, y_min + 1, y), self.gardenOutline)
                                self.editor.placeBlock(
                                    (i, y_min + 2, y), self.gardenOutline)

                        case "W":
                            if not (i == x_min and y in self.entranceCo):
                                self.editor.placeBlock(
                                    (i, y_min - 1, y), Block("oak_log"))
                                self.editor.placeBlock(
                                    (i, y_min, y), self.gardenOutline)
                                self.editor.placeBlock(
                                    (i, y_min + 1, y), self.gardenOutline)
                                self.editor.placeBlock(
                                    (i, y_min + 2, y), self.gardenOutline)

                        case _:
                            self.editor.placeBlock(
                                (i, y_min - 1, y), self.garden_floor)

                else:
                    self.editor.placeBlock(
                        (i, y_min - 1, y), self.garden_floor)

    def build(self):
        self.create_house_skeleton()
        self.put_wall_on_skeleton()
        self.place_door()
        self.place_roof()
        self.put_celling()
        self.place_window()
        self.place_entrance()
        self.place_garden_outline()
        if self.nbEtage > 1:
            self.place_stairs()


if __name__ == "__main__":
    editor = Editor(buffering=True)
    buildArea = editor.getBuildArea()
    coordinates_min = [min(buildArea.begin[i], buildArea.last[i])
                       for i in range(3)]
    coordinates_max = [max(buildArea.begin[i], buildArea.last[i])
                       for i in range(3)]

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

    for i in range(1):
        house = House(editor, coordinates_min, coordinates_max, "W", blocks)

        house.build()

        new_coordinates_min = (
            coordinates_max[0] + 20, coordinates_min[1], coordinates_min[2])
        new_coordinates_max = (
            coordinates_max[0] + 10 + 40, coordinates_max[1], coordinates_max[2])
        coordinates_min = new_coordinates_min
        coordinates_max = new_coordinates_max

    # delete(editor, coordinates_min, coordinates_max)
    editor.flushBuffer()
