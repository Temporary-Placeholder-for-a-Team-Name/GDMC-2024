import math

class Windows:
    def __init__(self, all_externs_walls, editor, coordinates_min, nbEtage, window):
        self.walls = all_externs_walls
        self.editor = editor
        self.coordinates_min = coordinates_min
        self.nbEtage = nbEtage
        self.window = window

    def place_windows(self):
        for wall in self.walls:
            x1, z1, x2, z2 = wall
            x = abs(x2 - x1) - 1
            z = abs(z2 - z1) - 1
            if x1 == x2:
                self.place_window_on_wall(wall, z, False)
            elif z1 == z2:
                self.place_window_on_wall(wall, x, True)

    def place_window_on_wall(self, wall, axis, is_x):
        for l in range(self.nbEtage + 1):
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