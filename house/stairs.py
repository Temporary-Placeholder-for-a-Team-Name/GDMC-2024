from gdpc import Block


class Stairs:
    def __init__(self, editor, skeleton, blocks, coordinates_min, nbEtage, floor):
        self.editor = editor
        self.skeleton = skeleton
        self.blocks = blocks
        self.coordinates_min = coordinates_min
        self.nbEtage = nbEtage
        self.floor = floor

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