from typing import Tuple
import random


def build_walls(start: Tuple[int, int], width: int, height: int):
    non_walls = set()
    non_walls.add(start)
    open_set = _get_neighbours(start, width, height)
    while open_set:
        index = random.randrange(0, len(open_set))
        dest, source = open_set.pop(index)
        if dest not in non_walls:
            non_walls.add(dest)
            non_walls.add(_get_inbetween_cell(source, dest))
            open_set += _get_neighbours(dest, width, height)

    walls = set()
    for x in range(width):
        for y in range(height):
            if (x, y) not in non_walls:
                walls.add((x, y))
    return walls


def _get_inbetween_cell(a, b):
    return (a[0] + b[0]) // 2, (a[1] + b[1]) // 2


def _get_neighbours(cell: Tuple[int, int], width: int, height: int):
    nbrs = []
    for x, y in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        if 0 <= x+cell[0] < width and 0 <= y + cell[1] < height:
            nbrs.append([(x+cell[0], y+cell[1]), cell])

    return nbrs
