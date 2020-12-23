from collections import deque
from itertools import islice


def get_input():
    with open('input.txt') as file:
        deck_1, deck_2 = (
            deque(
                int(num)
                for num in deck.split('\n')[1:]
            )
            for deck in file.read().split('\n\n')
        )
    return deck_1, deck_2


def combat(deck_1, deck_2, recurse=False):
    previous_rounds = set()
    while deck_1 and deck_2:
        hash_1 = tuple(deck_1)
        hash_2 = tuple(deck_2)
        if (hash_1, hash_2) in previous_rounds:
            deck_2 = deque()
            break
        previous_rounds.add((hash_1, hash_2))

        draw_1 = deck_1.popleft()
        draw_2 = deck_2.popleft()



        if recurse and draw_1 <= len(deck_1) and draw_2 <= len(deck_2):
            rec_deck_1 = deque(islice(deck_1, 0, draw_1))
            rec_deck_2 = deque(islice(deck_2, 0, draw_2))
            hand_winner, _ = combat(rec_deck_1, rec_deck_2, recurse)
        else:
            hand_winner = 1 if draw_1 > draw_2 else 2

        if hand_winner == 1:
            deck_1.append(draw_1)
            deck_1.append(draw_2)
        else:
            deck_2.append(draw_2)
            deck_2.append(draw_1)

    winning_deck = deck_1 or deck_2
    score = sum((idx + 1) * card for (idx, card) in enumerate(reversed(winning_deck)))
    winner = 1 if deck_1 else 2
    return winner, score


def main():
    deck_1, deck_2 = get_input()

    # part 1
    winner, score = combat(deck_1.copy(), deck_2.copy())
    print(f'Player {winner} wins normal combat with {score} points!')

    # part 2
    winner, score = combat(deck_1.copy(), deck_2.copy(), recurse=True)
    print(f'Player {winner} wins recursive combat with {score} points!')


if __name__ == '__main__':
    main()

