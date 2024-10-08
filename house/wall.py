import itertools as it

def is_inside_all(big_wall, small_wall):
    bw_x_start, bw_z_start, bw_x_end, bw_z_end = big_wall
    sw_x_start, sw_z_start, sw_x_end, sw_z_end = small_wall
    if bw_x_start == bw_x_end == sw_x_start == sw_x_end:
        return bw_x_start == sw_x_start and bw_z_start <= sw_z_start and sw_z_end <= bw_z_end
    elif bw_z_start == bw_z_end == sw_z_start == sw_z_end:
        return bw_z_start == sw_z_start and bw_x_start <= sw_x_start and sw_x_end <= bw_x_end

class Wall:
    def __init__(self, editor, grid3d, coordinates_min, skeleton, style, direction):
        self.direction = direction
        self.editor = editor
        self.grid3d = grid3d
        self.coordinates_min = coordinates_min
        self.skeleton = skeleton
        self.wall_style = style

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
                    self.editor.placeBlock((x + i, self.coordinates_min[1] + y, z + j), self.wall_style)
                    self.grid3d[x_plan3d + i, y, z_plan3d + j] = True

    def wall_facing_direction(self):
        if self.direction == "N":
            closest_wall = min(self.skeleton, key=lambda wall: wall[1])
            wall = (closest_wall[0],
                    closest_wall[1],
                    closest_wall[0] + closest_wall[2],
                    closest_wall[1])
        elif self.direction == "S":
            closest_wall = max(self.skeleton, key=lambda wall: wall[1] + wall[3])
            wall = (closest_wall[0],
                    closest_wall[1] + closest_wall[3],
                    closest_wall[0] + closest_wall[2],
                    closest_wall[1] + closest_wall[3])
        elif self.direction == "E":
            closest_wall = max(self.skeleton, key=lambda wall: wall[0] + wall[2])
            wall = (closest_wall[0] + closest_wall[2],
                    closest_wall[1],
                    closest_wall[0] + closest_wall[2],
                    closest_wall[1] + closest_wall[3])
        elif self.direction == "W":
            closest_wall = min(self.skeleton, key=lambda wall: wall[0])
            wall = (closest_wall[0],
                    closest_wall[1],
                    closest_wall[0],
                    closest_wall[1] + closest_wall[3])
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
                if is_inside_all(wall, adj_wall):
                    remove_wall = True
                    break
            if not remove_wall:
                walls_to_keep.append(wall)

        return walls_to_keep