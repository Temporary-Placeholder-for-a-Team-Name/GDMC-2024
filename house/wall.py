import itertools as it

class Wall:
    def __init__(self, editor, grid3d, coordinates_min, skeleton, wall, direction):
        self.direction = direction
        self.editor = editor
        self.grid3d = grid3d
        self.coordinates_min = coordinates_min
        self.skeleton = skeleton
        self.wall = wall

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
