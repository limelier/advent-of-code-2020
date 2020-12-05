from array import array


def binary(string, one):
    num = 0

    for char in string:
        if char is one:
            num += 1
        num *= 2
    num //= 2

    return num


def seat_id(seat_string):
    row = binary(seat_string[:7], 'B')
    column = binary(seat_string[7:], 'R')
    return row * 8 + column


def part_1():
    with open('input.txt') as file:
        print(max(map(lambda line: seat_id(line.strip()), file)))


def part_2():
    neighbors_found = [0] * (127 * 8 + 7)

    with open('input.txt') as file:
        for line in file:
            s_id = seat_id(line.strip())

            neighbors_found[s_id] = -2
            neighbors_found[s_id - 1] += 1
            neighbors_found[s_id + 1] += 1

    print(neighbors_found.index(2))


if __name__ == '__main__':
    part_2()
