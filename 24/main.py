from collections import defaultdict


def get_coords():
    with open('input.txt') as file:
        return [
            follow_steps(line.strip())
            for line in file
        ]


def follow_steps(line, start=(0, 0)):
    # uses odd-r horizontal layout
    # odd rows offset right
    e, s = start
    idx = 0
    while idx < len(line):
        ch = line[idx]
        idx += 1

        if ch == 'e':
            e += 1
        elif ch == 'w':
            e -= 1
        else:
            ch_2 = line[idx]
            idx += 1

            if ch_2 == 'e':
                # on odd rows, NE/SE goes east by one
                e += s % 2
            else:
                # on even rows, NW/SW goes west by one
                e -= (s + 1) % 2

            if ch == 's':
                s += 1
            else:
                s -= 1
    return e, s


def part_1():
    coord_list = get_coords()
    black_tiles = set()

    for coord in coord_list:
        black_tiles.symmetric_difference_update({coord})

    print(f'After flipping everything, there are {len(black_tiles)} black tiles.')
    return black_tiles


def part_2(black_tiles):
    offsets = {'e', 'ne', 'se', 'w', 'sw', 'nw'}

    for day in range(100):
        adjacent_black = defaultdict(int)

        for black_tile in black_tiles:
            for offset in offsets:
                adjacent_position = follow_steps(offset, black_tile)
                adjacent_black[adjacent_position] += 1

        new_black_tiles = set()
        for position, adjacent in adjacent_black.items():
            if adjacent == 2 or (position in black_tiles and adjacent == 1):
                new_black_tiles.add(position)

        black_tiles = new_black_tiles

    print(f'After 100 days, there are {len(black_tiles)} black tiles.')


if __name__ == '__main__':
    start_tiles = part_1()
    part_2(start_tiles)
