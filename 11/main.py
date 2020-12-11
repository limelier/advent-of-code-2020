from copy import deepcopy

with open('input.txt') as file:
    start_state = [list(line.strip()) for line in file]

height = len(start_state)
width = len(start_state[0])

deltas = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

# pad state with empty space to simplify neighbor checking
start_state = [
    ['.'] * (width + 2),
    *[['.'] + line + ['.'] for line in start_state],
    ['.'] * (width + 2),
]


def simulate(state, fill_below, empty_above, far_sight=False):
    next_state = [['#' if pos == 'L' else '.' for pos in line] for line in state]

    while next_state != state:
        # for line in state:
        #     print(''.join(line))
        # print()

        state = next_state

        next_state = deepcopy(state)
        for i in range(1, height + 1):
            for j in range(1, width + 1):
                if state[i][j] == '.':
                    continue

                adjacencies = 0
                for di, dj in deltas:
                    ai, aj = i + di, j + dj
                    if far_sight:
                        while state[ai][aj] == '.' and \
                                0 < ai < height + 1 and \
                                0 < aj < width + 1:
                            ai += di
                            aj += dj

                    if state[ai][aj] == '#':
                        adjacencies += 1

                if state[i][j] == '#' and adjacencies >= empty_above:
                    next_state[i][j] = 'L'
                elif state[i][j] == 'L' and adjacencies <= fill_below:
                    next_state[i][j] = '#'

    occupied = sum(line.count('#') for line in state)
    print('Occupied seats:', occupied)


if __name__ == '__main__':
    simulate(deepcopy(start_state), 0, 4)
    simulate(deepcopy(start_state), 0, 5, far_sight=True)
