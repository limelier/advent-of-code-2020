from time import time

def mem_game(starting_nums, stopping_turn):
    last_turn_spoken = {}
    for idx, num in enumerate(starting_nums):
        last_turn_spoken[num] = idx + 1
    turn = len(starting_nums) + 1
    last_num = starting_nums[-1]

    while turn <= stopping_turn:
        num = turn - 1 - last_turn_spoken[last_num] if last_num in last_turn_spoken.keys() else 0
        last_turn_spoken[last_num] = turn - 1
        last_num = num
        turn += 1

    print(f'The number spoken on turn {stopping_turn} is {last_num}.')


def main():
    starting_nums = [1, 2, 16, 19, 18, 0]

    start = time()
    mem_game(starting_nums, 2020)
    print(f'Took {time() - start}s.')

    start = time()
    mem_game(starting_nums, 30000000)
    print(f'Took {time() - start}s.')


if __name__ == '__main__':
    main()
