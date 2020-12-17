def get_input(dimensions):
    """
    Read problem input, generating a set of an n-dimensional point for each '#' in the input file.

    The created points are placed on the two-dimensional slice {(x, y, z1, z2, ...) | zk = 0}.
    """
    assert dimensions >= 2
    space = set()

    with open('input.txt') as file:
        for x, line in enumerate(file):
            for y, cell in enumerate(line.strip()):
                if cell == '#':
                    space.add((x, y) + (0,) * (dimensions - 2))

    return space


def generate_points(low, high):
    """
    Generate all possible points in the hyperrectangle with low and high as opposite corners, and the layer outside.

    For example, if low is (0, 0, 0) and high is (2, 2, 2), generate all points from (-1, -1, -1) to (3, 3, 3)
    inclusive.
    """
    if len(low) == 0:
        return [()]

    return [
        (i,) + subpoint
        for i in range(low[0] - 1, high[0] + 2)
        for subpoint in generate_points(low[1:], high[1:])
    ]


def neighbors(point):
    """
    Generate all neighbors of a given point.
    """
    dims = len(point)
    return [
        other_point
        for other_point in generate_points(
            point,
            point
        )
        if other_point != point
    ]


def update_bounds(low, high, point):
    """
    If the point is outside the hyperrectangle defined by the given bounds, expand the hyperrectangle to fill it.
    """
    low = list(low)
    high = list(high)
    point = list(point)

    for i in range(len(low)):
        if point[i] <= low[i]:
            low[i] = point[i]
        if high[i] <= point[i]:
            high[i] = point[i]

    return tuple(low), tuple(high)


def step(space, low, high, dimensions):
    """
    Simulate one step of the n-dimensional cell automata.

    Cells are born for 3 neighbors, and live for 2 or 3 neighbors.
    """
    new_space = set()
    new_low = (0,) * dimensions
    new_high = (0,) * dimensions
    for point in generate_points(low, high):
        active_neighbors = sum(
            1
            for neighbor in neighbors(point)
            if neighbor in space
        )
        if point in space and active_neighbors == 2 \
                or active_neighbors == 3:
            new_space.add(point)
            new_low, new_high = update_bounds(new_low, new_high, point)

    return new_space, new_low, new_high


def simulate(space, dimensions, steps):
    """
    Simulate several steps of an n-dimensional cell automata, and return the number of living cells at the end.

    Cells are born for 3 neighbors, and live for 2 or 3 neighbors.
    """
    low = (0,) * dimensions
    high = (7, 7) + (0,) * (dimensions - 2)

    for _ in range(steps):
        space, low, high = step(space, low, high, dimensions)

    print(len(space))


def main():
    print(neighbors((0, 0)))
    # treat input as 2d slice of 3d space, simulate automata to 6 steps
    simulate(get_input(3), 3, 6)
    # treat input as 2d slice of 4d space, simulate automata to 6 steps
    simulate(get_input(4), 4, 6)


if __name__ == '__main__':
    main()
