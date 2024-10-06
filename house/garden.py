from gdpc import Block


class Garden:
    def __init__(self, editor, coordinates_min, coordinates_max, direction, entranceCo, gardenOutline, garden_floor):
        self.editor = editor
        self.coordinates_min = coordinates_min
        self.coordinates_max = coordinates_max
        self.direction = direction
        self.entranceCo = entranceCo
        self.gardenOutline = gardenOutline
        self.garden_floor = garden_floor

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
