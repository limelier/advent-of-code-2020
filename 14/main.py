import re
from collections import defaultdict


def apply_bitmask(mask: str, num: int):
    bits = [char for char in format(num, '036b')]
    for i in range(36):
        if mask[i] != 'X':
            bits[i] = mask[i]
    return int(''.join(bits), 2)


def read_input(filename):
    mask_re = re.compile(r'mask = ([01X]{36})\n')
    mem_re = re.compile(r'mem\[(\d+)] = (\d+)\n')

    with open(filename) as file:
        for line in file:
            mask_match = mask_re.fullmatch(line)
            if mask_match:
                yield mask_match[1]
            else:
                mem_match = mem_re.fullmatch(line)
                yield int(mem_match[1]), int(mem_match[2])


def part_1():
    memory = defaultdict(int)
    mask = None

    for instruction in read_input('input.txt'):
        if isinstance(instruction, str):
            mask = instruction
        else:
            address, value = instruction
            memory[address] = apply_bitmask(mask, value)
    print(f'Memory sum is {sum(memory.values())}')


def apply_floatmask(mask: str, target: int):
    bits = format(target, '036b')
    nums = [0]

    for idx in range(36):
        pow2 = 35 - idx
        if mask[idx] == '0':
            if bits[idx] == '1':
                vals = [1]
            else:
                continue
        elif mask[idx] == '1':
            vals = [1]
        else:
            vals = [0, 1]
        nums = [
            num + val * 2**pow2
            for num in nums
            for val in vals
        ]
    return nums


def part_2():
    memory = defaultdict(int)
    mask = None

    for instruction in read_input('input.txt'):
        if isinstance(instruction, str):
            mask = instruction
        else:
            address, value = instruction
            all_addresses = apply_floatmask(mask, address)
            for addr in all_addresses:
                memory[addr] = value

    print(f'Memory sum is {sum(memory.values())}')


if __name__ == '__main__':
    part_1()
    part_2()

