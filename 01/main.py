import itertools

def product(tup):
    prod = 1
    for num in tup:
        prod *= num
    return prod


def sum_prod(nums, n):
    """
    Find a n-uple of numbers in nums that sums to 2020, and return its product.
    """
    for tup in itertools.permutations(nums, n):
        if sum(tup) == 2020:
            print(product(tup))
            break


def main():
    nums = [int(s) for s in open('input.txt', 'r').readlines()]
    # part 1
    sum_prod(nums, 2)
    # part 2
    sum_prod(nums, 3)


if __name__ == "__main__":
    main()
