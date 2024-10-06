from gdpc import Block

class Door:
    def __init__(self, editor, coordinates_min, coordinates_max, direction, blocks, nb_etage, walls, skeleton):
        self.editor = editor
        self.coordinates_min = coordinates_min
        self.coordinates_max = coordinates_max
        self.direction = direction
        self.blocks = blocks
        self.nb_etage = nb_etage
        self.walls = walls
        self.skeleton = skeleton

    def place_door(self):
        for wall in self.walls:
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

                    return (
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

                    return (
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

                    return (wall[0] + (wall[2] - wall[0]) // 2, wall[0] + (wall[2] - wall[0]) // 2 + 2,
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

                    return (wall[0] + (wall[2] - wall[0]) // 2, wall[0] + (wall[2] - wall[0]) // 2 + 1,
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

                    return (
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

                    return (
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

                    return (wall[0] + (wall[2] - wall[0]) // 2, wall[0] + (wall[2] - wall[0]) // 2 + 2,
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

                    return (wall[0] + (wall[2] - wall[0]) // 2, wall[0] + (wall[2] - wall[0]) // 2 + 1,
                                       wall[0] + (wall[2] - wall[0]) // 2 + 1, wall[0] + (wall[2] - wall[0]) // 2 - 1)
            case _:
                pass