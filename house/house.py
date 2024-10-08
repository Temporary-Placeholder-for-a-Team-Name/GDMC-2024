from gdpc import Editor, Block, geometry
import numpy as np

from garden import Garden
from stairs import Stairs
from windows import Windows
from wall import Wall
from door import Door
from roof import Roof

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



    def build(self):
        self.create_house_skeleton()
        wall = Wall(self.editor, self.grid3d, self.coordinates_min, self.skeleton, self.wall, self.direction)
        wall.put_wall_on_skeleton()

        door = Door(self.editor, self.coordinates_min, self.coordinates_max, self.direction, self.nbEtage, wall, self.skeleton)
        door.place_door()
        entrance_co = door.place_entrance()

        roof = Roof(self.editor, self.blocks, self.skeleton, self.coordinates_min, self.coordinates_max, self.grid3d)
        roof.place_roof()

        self.put_celling()

        windows = Windows(wall.get_all_extern_walls(), self.editor, self.coordinates_min, self.nbEtage, self.window)
        windows.place_windows()

        garden = Garden(self.editor, self.coordinates_min, self.coordinates_max, self.direction, entrance_co, self.gardenOutline, self.garden_floor)
        garden.place_garden_outline()

        if self.nbEtage > 1:
            stair = Stairs(self.editor, self.skeleton, self.blocks, self.coordinates_min, self.nbEtage, self.floor)
            stair.place_stairs()


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
