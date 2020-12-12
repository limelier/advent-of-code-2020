from dataclasses import dataclass
from typing import Tuple


def generate_instructions():
    with open('input.txt') as file:
        for line in file:
            line = line.strip()
            action = line[0]
            amount = int(line[1:])
            yield action, amount


@dataclass
class CardinalDirection:
    delta: Tuple[int, int]
    left: str
    right: str


dirs = {
    'N': CardinalDirection((0, 1), 'W', 'E'),
    'E': CardinalDirection((1, 0), 'N', 'S'),
    'S': CardinalDirection((0, -1), 'E', 'W'),
    'W': CardinalDirection((-1, 0), 'S', 'N'),
}


def add_delta(pos, delta, times):
    x, y = pos
    dx, dy = delta
    return x + dx * times, y + dy * times


def manhattan_distance():
    pos = 0, 0
    facing = 'E'

    for action, amount in generate_instructions():
        if action in 'NESW':
            pos = add_delta(pos, dirs[action].delta, amount)
        elif action == 'F':
            pos = add_delta(pos, dirs[facing].delta, amount)
        elif action == 'L':
            for i in range(0, amount, 90):
                facing = dirs[facing].left
        else:
            for i in range(0, amount, 90):
                facing = dirs[facing].right

    x, y = pos
    print(f'We are at position {x}, {y}; {abs(x) + abs(y)} units away from 0, 0.')


def turn_around_origin(point, direction, times):
    x, y = point
    for _ in range(times):
        if direction == 'L':
            x, y = -y, x
        else:
            x, y = y, -x

    return x, y


def rtfm_distance():
    pos = 0, 0
    waypoint = 10, 1

    for action, amount in generate_instructions():
        if action in 'NESW':
            waypoint = add_delta(waypoint, dirs[action].delta, amount)
        elif action == 'F':
            pos = add_delta(pos, waypoint, amount)
        else:
            waypoint = turn_around_origin(waypoint, action, amount // 90)

    x, y = pos
    print(f'We are ACTUALLY at position {x}, {y}; {abs(x) + abs(y)} units away from 0, 0.')


if __name__ == '__main__':
    manhattan_distance()
    rtfm_distance()

