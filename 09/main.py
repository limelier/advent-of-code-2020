from collections import deque
from itertools import permutations


def part_1():
    last_25 = deque()

    with open('input.txt') as file:
        for i in range(25):
            num = int(file.readline().strip())
            last_25.append(num)
        for line in file:
            num = int(line.strip())
            okay = False
            for a, b in permutations(last_25, 2):
                if a + b == num:
                    okay = True
                    break
            if not okay:
                print('Found %d, not a sum of any pair in the last 25 numbers' % num)
                return num
            last_25.append(num)
            last_25.popleft()


def part_2(wrong_num):
    summed = deque()

    with open('input.txt') as file:
        for i in range(2):
            num = int(file.readline().strip())
            summed.append(num)
        sum_ = sum(summed)

        while sum_ != wrong_num:
            if sum_ > wrong_num:
                sum_ -= summed.popleft()
            else:
                num = int(file.readline().strip())
                sum_ += num
                summed.append(num)

    smallest = min(summed)
    largest = max(summed)
    print('The weakness is %d' % (smallest + largest))


if __name__ == '__main__':
    wrong_num = part_1()
    part_2(wrong_num)

