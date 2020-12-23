puzzle_input = '538914762'
cups = [int(x) for x in puzzle_input]


def wrap(x):
    """Wrap x to between 1 and 9"""
    if not 0 <= x <= 9:
        x %= 9
    if x == 0:
        x = 9
    return x


for _ in range(100):
    destination = wrap(cups[0] - 1)
    while True:
        dest_idx = cups.index(destination)
        if 1 <= dest_idx <= 3:
            destination = wrap(destination - 1)
        else:
            break
    # move picked up cups
    cups = cups[:1] + cups[4:dest_idx + 1] + cups[1:4] + cups[dest_idx + 1:]
    # move 'selection'
    cups = cups[1:] + cups[:1]

one_idx = cups.index(1)
cups = cups[one_idx+1:] + cups[:one_idx]

print(''.join(str(cup) for cup in cups))
