import math
from gdpc import Block

def calcul_height_roof(length):
    if length <= 5:
        n = 1
    elif length <= 10:
        n = 2
    else:
        n = 3
    return n

class Roof:
    def __init__(self, editor, blocks, skeleton, coordinates_min, coordinates_max, grid3d):
        self.editor = editor
        self.blocks = blocks
        self.skeleton = skeleton
        self.coordinates_min = coordinates_min
        self.coordinates_max = coordinates_max
        self.grid3d = grid3d
        self.roof = Block(self.blocks["roof"], {})
        self.celling = Block(self.blocks["celling_slab"], {"type": "bottom"})

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
