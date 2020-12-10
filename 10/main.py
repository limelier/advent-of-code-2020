def get_adapters(filename):
    with open(filename) as file:
        return [int(line.strip()) for line in file]


def part_1():
    adapters = get_adapters('input.txt')
    adapters.sort()
    # add wall socket (0) and built-in adapter (always +3)
    adapters = [0] + adapters + [adapters[-1] + 3]

    diff_1 = 0
    diff_3 = 0

    for i in range(len(adapters) - 1):
        diff = adapters[i+1] - adapters[i]
        if diff == 1:
            diff_1 += 1
        elif diff == 3:
            diff_3 += 1

    print('It is', diff_1 * diff_3)


def get_diffs(adapters):
    return [adapters[i+1] - adapters[i] for i in range(len(adapters) - 1)]


def bruteforce(sequence):
    perms = {''.join(str(i) for i in sequence)}
    for i in range(len(sequence) - 1):
        diff_sum = sequence[i] + sequence[i+1]
        if diff_sum <= 3:
            perms = perms.union(bruteforce(sequence[:i] + [diff_sum] + sequence[i+2:]))
    return perms


def bruteforce_ones(seq_len):
    sequence = [1] * seq_len
    return len(bruteforce(sequence))


def permutation_search(diffs):
    seq_perms = {}

    perms = 1
    seq_start, current = None, 0

    # search for sequences of consecutive ones
    while current < len(diffs):
        if diffs[current] == 1:
            if seq_start is None:
                seq_start = current  # start sequence
            # else continue sequence
        else:
            if seq_start is not None:  # curr is 3, ending sequence
                seq_len = current - seq_start
                if seq_len in seq_perms.keys():
                    perms *= seq_perms[seq_len]
                else:
                    val = bruteforce_ones(seq_len)
                    seq_perms[seq_len] = val
                    perms *= val
            seq_start = None
        current += 1
    return perms


def part_2():
    adapters = get_adapters('input.txt')
    adapters.sort()
    # add wall socket (0) and built-in adapter (always +3)
    adapters = [0] + adapters + [adapters[-1] + 3]

    diffs = get_diffs(adapters)

    perms = permutation_search(diffs)
    print('Ways to arrange:', perms)


if __name__ == '__main__':
    part_1()
    part_2()

