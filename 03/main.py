from typing import Tuple, List


def go_down(hillside: List[str], down, right):
    pos_vert, pos_horiz = 0, 0
    wrap = len(hillside[0])
    trees = 0
    while pos_vert < len(hillside):
        if hillside[pos_vert][pos_horiz] == '#':
            trees += 1
        pos_vert += down
        pos_horiz = (pos_horiz + right) % wrap
    return trees


def product(nums):
    prod = 1
    for num in nums:
        prod *= num
    return prod


def main():
    with open('input.txt') as file:
        hillside = [line.strip() for line in file.readlines()]
    res = product(go_down(hillside, down, right) for (down, right) in [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1),
    ])
    print(res)


if __name__ == '__main__':
    main()
