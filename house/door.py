from gdpc import Block

class Door:
    def __init__(self, editor, coordinates_min, coordinates_max, direction, nb_etage, wall_object, skeleton):
        self.editor = editor
        self.coordinates_min = coordinates_min
        self.coordinates_max = coordinates_max
        self.direction = direction
        self.blocks = "quartz_stairs"
        self.nb_etage = nb_etage
        self.walls = wall_object
        self.skeleton = skeleton

    def place_door(self):
        all_walls = self.walls.get_adjacent_walls()

        for wall in all_walls:
            for i in range(self.nb_etage):
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
                        # self.editor.placeBlock((x_min, self.coordinates_min[1] + 1 + i * 4, z_min + door_pos), self.door)
                        # self.editor.placeBlock((x_min, self.coordinates_min[1] + 1 + i * 4, z_min + door_pos + 1), self.door)
                    else:
                        door_pos = width // 2
                        for y in range(self.coordinates_min[1] + 1 + i * 4, self.coordinates_min[1] + 3 + i * 4):
                            self.editor.placeBlock((x_min, y, z_min + door_pos), Block("air"))
                        # self.editor.placeBlock((x_min, self.coordinates_min[1] + 1 + i * 4, z_min + door_pos), self.door)
                else:
                    width = x_max - x_min
                    if width % 2 != 0:
                        door_pos = width // 2
                        for y in range(self.coordinates_min[1] + 1 + i * 4, self.coordinates_min[1] + 3 + i * 4):
                            self.editor.placeBlock(
                                (x_min + door_pos, y, z_min), Block("air"))
                            self.editor.placeBlock(
                                (x_min + door_pos + 1, y, z_min), Block("air"))
                       # self.editor.placeBlock((x_min + door_pos, self.coordinates_min[1] + 1 + i * 4, z_min), self.door)

                    else:
                        door_pos = width // 2
                        for y in range(self.coordinates_min[1] + 1 + i * 4, self.coordinates_min[1] + 3 + i * 4):
                            self.editor.placeBlock(
                                (x_min + door_pos, y, z_min), Block("air"))
                        # self.editor.placeBlock((x_min + door_pos, self.coordinates_min[1] + 1 + i * 4, z_min), self.door)

    def place_entrance(self):
        wall = self.walls.wall_facing_direction()

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
                                           Block(self.blocks, {"facing": "east"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks, {"facing": "east"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks, {"facing": "south"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 2),
                                           Block(self.blocks, {"facing": "north"}))

                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2),
                                           Block(self.blocks, {"facing": "east", "half": "top"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks, {"facing": "east", "half": "top"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks, {"facing": "south", "half": "top"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 2),
                                           Block(self.blocks, {"facing": "north", "half": "top"}))

                    return (
                        (wall[1] + wall[3]) // 2,
                        (wall[1] + wall[3]) // 2 + 2,
                        (wall[1] + wall[3]) // 2 + 1,
                        (wall[1] + wall[3]) // 2 - 1
                    )

                else:
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 1, (wall[1] + wall[3]) // 2),
                                           Block("air"))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 2, (wall[1] + wall[3]) // 2),
                                           Block("air"))

                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2),
                                           Block(self.blocks, {"facing": "east"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks, {"facing": "north"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1], (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks, {"facing": "south"}))

                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2),
                                           Block(self.blocks, {"facing": "east", "half": "top"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks, {"facing": "north", "half": "top"}))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks, {"facing": "south", "half": "top"}))

                    return (
                        (wall[1] + wall[3]) // 2,
                        (wall[1] + wall[3]) // 2 + 1,
                        (wall[1] + wall[3]) // 2 + 1,
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
                                           Block(self.blocks, {"facing": "south"}))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2 + 1, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks, {"facing": "south"}))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2 - 1, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks, {"facing": "east"}))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2 + 2, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks, {"facing": "west"}))

                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 3, wall[1]),
                                           Block(self.blocks, {"facing": "south", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1] + 3, wall[1]),
                        Block(self.blocks, {"facing": "south", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1] + 3, wall[1]),
                        Block(self.blocks, {"facing": "east", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 2,
                         self.coordinates_min[1] + 3, wall[1]),
                        Block(self.blocks, {"facing": "west", "half": "top"}))

                    return (
                        wall[0] + (wall[2] - wall[0]) // 2,
                        wall[0] + (wall[2] - wall[0]) // 2 + 2,
                        wall[0] + (wall[2] - wall[0]) // 2 + 1,
                        wall[0] + (wall[2] - wall[0]) // 2 - 1)

                else:
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 1, wall[1] + 1), Block("air"))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 2, wall[1] + 1), Block("air"))

                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks, {"facing": "south"}))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2 + 1, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks, {"facing": "west"}))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2 - 1, self.coordinates_min[1], wall[1]),
                                           Block(self.blocks, {"facing": "east"}))

                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 3, wall[1]),
                                           Block(self.blocks, {"facing": "south", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1] + 3, wall[1]),
                        Block(self.blocks, {"facing": "west", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1] + 3, wall[1]),
                        Block(self.blocks, {"facing": "east", "half": "top"}))

                    return (
                        wall[0] + (wall[2] - wall[0]) // 2,
                        wall[0] + (wall[2] - wall[0]) // 2 + 1,
                        wall[0] + (wall[2] - wall[0]) // 2 + 1,
                        wall[0] + (wall[2] - wall[0]) // 2 - 1
                    )

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
                                           Block(self.blocks, {"facing": "west"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks, {"facing": "west"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks, {"facing": "south"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 2),
                                           Block(self.blocks, {"facing": "north"}))

                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2),
                                           Block(self.blocks, {"facing": "west", "half": "top"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks, {"facing": "west", "half": "top"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks, {"facing": "south", "half": "top"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 2),
                                           Block(self.blocks, {"facing": "north", "half": "top"}))

                    return (
                        (wall[1] + wall[3]) // 2,
                        (wall[1] + wall[3]) // 2 + 2,
                        (wall[1] + wall[3]) // 2 + 1,
                        (wall[1] + wall[3]) // 2 - 1
                    )
                else:
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 1, (wall[1] + wall[3]) // 2),
                                           Block("air"))
                    self.editor.placeBlock((wall[0], self.coordinates_min[1] + 2, (wall[1] + wall[3]) // 2),
                                           Block("air"))

                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2),
                                           Block(self.blocks, {"facing": "west"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks, {"facing": "north"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1], (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks, {"facing": "south"}))

                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2),
                                           Block(self.blocks, {"facing": "west", "half": "top"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 + 1),
                                           Block(self.blocks, {"facing": "north", "half": "top"}))
                    self.editor.placeBlock((wall[0] + 1, self.coordinates_min[1] + 3, (wall[1] + wall[3]) // 2 - 1),
                                           Block(self.blocks, {"facing": "south", "half": "top"}))

                    return (
                        (wall[1] + wall[3]) // 2,
                        (wall[1] + wall[3]) // 2 + 1,
                        (wall[1] + wall[3]) // 2 + 1,
                        (wall[1] + wall[3]) // 2 - 1
                    )

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
                                           Block(self.blocks, {"facing": "north"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1], wall[1] + 1),
                        Block(self.blocks, {"facing": "north"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1], wall[1] + 1),
                        Block(self.blocks, {"facing": "east"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 2,
                         self.coordinates_min[1], wall[1] + 1),
                        Block(self.blocks, {"facing": "west"}))

                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks, {"facing": "north", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks, {"facing": "north", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks, {"facing": "east", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 2,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks, {"facing": "west", "half": "top"}))

                    return (
                        wall[0] + (wall[2] - wall[0]) // 2,
                        wall[0] + (wall[2] - wall[0]) // 2 + 2,
                        wall[0] + (wall[2] - wall[0]) // 2 + 1,
                        wall[0] + (wall[2] - wall[0]) // 2 - 1
                    )
                else:
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 1, wall[1]),
                                           Block("air"))
                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1] + 2, wall[1]),
                                           Block("air"))

                    self.editor.placeBlock((wall[0] + (wall[2] - wall[0]) // 2, self.coordinates_min[1], wall[1] + 1),
                                           Block(self.blocks, {"facing": "north"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1], wall[1] + 1),
                        Block(self.blocks, {"facing": "west"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1], wall[1] + 1),
                        Block(self.blocks, {"facing": "east"}))

                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks, {"facing": "north", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 + 1,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks, {"facing": "west", "half": "top"}))
                    self.editor.placeBlock(
                        (wall[0] + (wall[2] - wall[0]) // 2 - 1,
                         self.coordinates_min[1] + 3, wall[1] + 1),
                        Block(self.blocks, {"facing": "east", "half": "top"}))

                    return (
                        wall[0] + (wall[2] - wall[0]) // 2,
                        wall[0] + (wall[2] - wall[0]) // 2 + 1,
                        wall[0] + (wall[2] - wall[0]) // 2 + 1,
                        wall[0] + (wall[2] - wall[0]) // 2 - 1
                    )
            case _:
                pass