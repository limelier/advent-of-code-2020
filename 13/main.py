def process_id(id_str: str):
    if id_str.isnumeric():
        return int(id_str)
    return None


def earliest_time(timestamp, bus_id):
    if bus_id is None:
        return None

    earliest = bus_id * (timestamp // bus_id + 1)
    return earliest


def part_1():
    with open('input.txt') as file:
        timestamp = int(file.readline().rstrip())
        bus_ids = [process_id(id_str) for id_str in file.readline().rstrip().split(',')]

    best_bus, best_time = None, 2 * timestamp
    for bus_id in bus_ids:
        earliest = earliest_time(timestamp, bus_id)
        if earliest is not None and earliest < best_time:
            best_bus = bus_id
            best_time = earliest

    delta = best_time - timestamp
    print(f'Earliest bus is {best_bus}, {delta} minutes from now. Product is {best_bus * delta}.')


def product(nums):
    prod = 1
    for num in nums:
        prod *= num
    return prod


def extended_euclid(a, b):
    """
    Given two numbers a and b, find their greatest common denominator x, and alpha, beta s.t. x = alpha*a + beta*b.
    """
    v0 = (1, 0)
    v1 = (0, 1)

    while b != 0:
        q = a // b
        a, b = b, a % b
        v0, v1 = v1, (v0[0] - q * v1[0], v0[1] - q * v1[1])

    gcd = abs(a)
    alpha, beta = v0
    return gcd, alpha, beta


def chinese_remainder_theorem(bs, ms):
    """
    Given a set of equations x = bi mod mi, find x solving all.
    """

    m = product(ms)
    sol_sum = 0

    for i in range(len(ms)):
        mi, bi = ms[i], bs[i]
        ci = m // mi
        # partial equation: ci*xi = bi mod mi
        _, alpha, _ = extended_euclid(ci, mi)
        xi = alpha * bi
        sol_sum += xi * ci

    return sol_sum % m


def part_2():
    with open('input.txt') as file:
        _ = file.readline()
        bus_ids = [process_id(id_str) for id_str in file.readline().rstrip().split(',')]

    # observation: all bus ids are prime numbers (and therefore, pairwise co-prime) - so there is only one solution
    #   modulo product(bus_ids)
    crt_eqs = [(bus_id - (idx % bus_id), bus_id) for idx, bus_id in enumerate(bus_ids) if bus_id is not None]
    # the timestamp is b minutes before a multiple of bus_id, so the equation is timestamp = bus_id - b mod bus_id
    remainders, primes = [list(l) for l in zip(*crt_eqs)]
    solution = chinese_remainder_theorem(remainders, primes)
    print(solution)


if __name__ == '__main__':
    part_1()
    part_2()
