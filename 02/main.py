import re

alfa_numeric = re.compile(r'\w+')


def extract(line):
    substr = alfa_numeric.findall(line)
    lower = int(substr[0])
    upper = int(substr[1])
    what = substr[2]
    where = substr[3]
    return lower, upper, what, where


def part1():
    valid = 0
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            lower, upper, what, where = extract(line)
            if lower <= where.count(what) <= upper:
                valid += 1
    print(valid)


def part2():
    valid = 0
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            first, second, what, where = extract(line)
            if (where[first - 1] == what) ^ (where[second - 1] == what):
                valid += 1
    print(valid)


if __name__ == "__main__":
    part1()
    part2()
