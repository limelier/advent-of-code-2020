from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
from typing import List, Tuple, Optional

import numpy as np


def i8s_to_i10(bits) -> int:
    return bits @ (1 << np.arange(bits.size)[::-1])


def rotate_left(list_, steps=1):
    return list_[steps:] + list_[:steps]


class Dir(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


@dataclass
class Tile:
    id: int
    data: np.ndarray
    edges: List[Optional[int]]

    def __init__(self, id_, data):
        self.id = id_
        self.data = data
        # edges, clockwise from the top
        self.edges = [
            min(
                self.get_edge(row, col, rev)
                for rev in [True, False]
            )
            for row, col in [
                (0, None),  # up
                (None, -1),  # right
                (-1, None),  # down
                (None, 0),  # left
            ]
        ]

    def __hash__(self):
        return self.id

    def get_edge(self, row: int = None, col: int = None, reverse: bool = False):
        if row is not None:
            bits = self.data[row, :]
        else:
            assert col is not None
            bits = self.data[:, col]

        if reverse:
            bits = bits[::-1]

        return i8s_to_i10(bits)

    def rotate_ccw(self, steps=1):
        self.data = np.rot90(self.data, steps)
        self.edges = rotate_left(self.edges, steps)

    def flip_horizontal(self):
        self.data = np.fliplr(self.data)
        self.edges[Dir.LEFT.value], self.edges[Dir.RIGHT.value] = \
            self.edges[Dir.RIGHT.value], self.edges[Dir.LEFT.value]


def get_input():
    tiles = []
    with open('input.txt') as file:
        while True:
            line = file.readline()
            if line == '\n':
                break
            tile_id = int(line[5:9])
            tile_data = np.empty((10, 10), np.int8)
            for row in range(10):
                line = file.readline().strip()
                for col, ch in enumerate(line):
                    tile_data[row, col] = 1 if ch == '#' else 0
            tiles.append(Tile(tile_id, tile_data))
            file.readline()

    return tiles


def clean_up_tiles(tiles):
    """Remove lonely edges."""
    edge_occurences = defaultdict(int)
    for tile in tiles:
        for edge in tile.edges:
            edge_occurences[edge] += 1
            assert edge_occurences[edge] <= 2  # if this fails, the entire solution is wrong

    for tile in tiles:
        for idx, edge in enumerate(tile.edges):
            if edge_occurences[edge] == 1:
                # this edge is at the border of the map
                tile.edges[idx] = None
    return tiles


def product(nums):
    prod = 1
    for num in nums:
        prod *= num
    return prod


def part_1():
    tiles = get_input()
    tiles = set(clean_up_tiles(tiles))

    rows = cols = int(len(tiles) ** (1 / 2))

    tile_square = [
        [None for _ in range(rows)]
        for _ in range(cols)
    ]

    corners = [tile for tile in tiles if tile.edges.count(None) == 2]
    print(product(corner.id for corner in corners))

    image = np.empty((rows * 8, cols * 8))

    for row in range(rows):
        for col in range(cols):
            edge_left = None if col == 0 else tile_square[row][col - 1].edges[Dir.RIGHT.value]
            edge_top = None if row == 0 else tile_square[row - 1][col].edges[Dir.DOWN.value]

            ok = False
            if edge_left is None and edge_top is None:
                tile = corners.pop()
                ok = True
            else:
                for tile in tiles:
                    if edge_left in tile.edges and edge_top in tile.edges:
                        ok = True
                        break
            assert ok

            tiles.discard(tile)

            tile.rotate_ccw(tile.edges.index(edge_top))
            if tile.edges[Dir.LEFT.value] != edge_left:
                tile.flip_horizontal()

            tile_square[row][col] = tile
            image[row * 8:(row + 1) * 8, col * 8:(col + 1) * 8] = tile.data[1:-1, 1:-1]
            # print(f'Placed {tile.id} at {row}, {col}')

    with open('map.txt', 'w+') as file:
        for row in image:
            line = ''.join('#' if x == 1 else '.' for x in row) + '\n'
            file.write(line)

    return image


def get_sea_monster_mask():
    return np.array([
        [
            1 if x == '#' else 0
            for x in line
        ] for line in [
            '                  # ',
            '#    ##    ##    ###',
            ' #  #  #  #  #  #   ',
        ]
    ])


def masking(mask, image, add_mask=False):
    scan = image.copy()
    i_w, i_h = image.shape
    m_w, m_h = mask.shape

    ok = False
    for off_w in range(0, i_w - m_w + 1):
        for off_h in range(0, i_h - m_h + 1):
            window = image[off_w:off_w + m_w, off_h:off_h + m_h]
            result = window + 2 * mask  # 3s are hits, 2s are misses
            res = not np.any(result == 2)
            if res:
                ok = True
                if not add_mask:
                    return True, scan
                else:
                    scan[off_w:off_w + m_w, off_h:off_h + m_h] += mask
    return ok, scan


def part_2(image):
    sea_monster = get_sea_monster_mask()
    m_width, m_height = sea_monster.shape

    ok = False
    for _ in range(4):
        ok, _ = masking(sea_monster, image)
        if ok:
            break
        image = np.rot90(image)
    if not ok:
        image = np.fliplr(image)
        for _ in range(4):
            ok, _ = masking(sea_monster, image)
            if ok:
                break
            image = np.rot90(image)
    with open('image.txt', 'w+') as file:
        for row in image:
            line = ''.join('#' if x == 1 else '.' for x in row) + '\n'
            file.write(line)
    _, scan = masking(sea_monster, image, add_mask=True)
    with open('scan.txt', 'w+') as file:
        for row in scan:
            line = ''.join(
                'O' if x > 1
                else '~' if x == 1
                else '.'
                for x in row
            ) + '\n'
            file.write(line)
    print(np.count_nonzero(scan == 1))



if __name__ == '__main__':
    img = part_1()
    part_2(img)
