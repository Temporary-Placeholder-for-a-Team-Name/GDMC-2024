from typing import Union

import numpy as np
from gdpc      import Editor, Block, geometry, lookup
from PIL       import Image as img
from PIL.Image import Image
from skimage   import morphology

from world_maker.data_analysis import handle_import_image

from itertools import product


def remove_trees(heightmap: Union[str, Image], treesmap: Union[str, Image], mask: Union[str, Image]):
    print("[Remove tree] Starting...")
    editor = Editor(buffering=True)
    build_area = editor.getBuildArea()
    build_rectangle = build_area.toRect()

    start = build_rectangle.begin

    distance = (max(build_rectangle.end[0], build_rectangle.begin[0]) - min(build_rectangle.end[0], build_rectangle.begin[0]),
                max(build_rectangle.end[1], build_rectangle.begin[1]) - min(build_rectangle.end[1], build_rectangle.begin[1]))

    heightmap = handle_import_image(heightmap).convert('L')
    treesmap  = handle_import_image(treesmap).convert('L')
    mask      = handle_import_image(mask)

    removed_treesmap = img.new("L", distance, 0)

    for (x, z) in product(range(distance[0]), range(distance[1])) :

        if mask.getpixel((x, z)) != 0 and treesmap.getpixel((x, z)) > 0:

            tree_area = morphology.flood(treesmap, (z, x), tolerance=1)
            removed_treesmap = img.fromarray(np.where(tree_area, treesmap, 0).astype(np.uint8))

            y     = heightmap.getpixel((x, z))
            y_top = removed_treesmap.getpixel((x, z))
            geometry.placeLine(editor, (start[0] + x, y+1, start[1] + z), (start[0] + x, y_top, start[1] + z), Block('air'))

    removed_treesmap.save('./world_maker/data/removed_treesmap.png')
    print("[Remove tree] Done.")


def smooth_terrain(heightmap: Union[str, Image], heightmap_smooth: Union[str, Image], mask: Union[str, Image]):

    print("[Smooth terrain] Starting...")
    editor = Editor(buffering=True)
    build_area = editor.getBuildArea()
    build_rectangle = build_area.toRect()

    start = build_rectangle.begin

    distance = (max(build_rectangle.end[0], build_rectangle.begin[0]) - min(build_rectangle.end[0], build_rectangle.begin[0]),
                max(build_rectangle.end[1], build_rectangle.begin[1]) - min(build_rectangle.end[1], build_rectangle.begin[1]))

    heightmap        = handle_import_image(heightmap).convert('L')
    heightmap_smooth = handle_import_image(heightmap_smooth).convert('L')
    mask             = handle_import_image(mask).convert('L')

    smooth_terrain_delta = img.new("RGB", distance, 0)

    slice = editor.loadWorldSlice(build_rectangle)
    smoothable_blocks = lookup.OVERWORLD_SOILS | lookup.OVERWORLD_STONES | lookup.SNOWS

    for (x, z) in [(x, z) for x in range(distance[0]) for z in range(distance[1])] :

        if mask.getpixel((x, z)) == 0:
            continue
        y        = heightmap.getpixel((x, z))
        y_smooth = heightmap_smooth.getpixel((x, z))
        delta = y - y_smooth
        smooth_terrain_delta.putpixel((x, z), delta)

        if delta == 0:
            continue
        block = slice.getBlock((x, y, z))

        if block.id not in smoothable_blocks:
            continue
        if delta > 0:
            geometry.placeLine(editor, (start[0] + x, y, start[1] + z), (start[0] + x, y_smooth, start[1] + z), Block('air'))
            editor.placeBlock((start[0] + x, y_smooth, start[1] + z), block)

        else:
            geometry.placeLine(editor, (start[0] + x, y, start[1] + z), (start[0] + x, y_smooth, start[1] + z), block)

    smooth_terrain_delta.save('./world_maker/data/smooth_terrain_delta.png')
    print("[Smooth terrain] Done.")
