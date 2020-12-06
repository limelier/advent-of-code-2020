def generate_input():
    lines = []
    with open('input.txt') as file:
        for line in file:
            if line != '\n':
                lines.append(line.strip())
            else:
                yield lines
                lines = []
        if lines:
            yield lines


def process(part=1):
    count = 0
    for group in generate_input():
        if part == 1:
            positive_answers = set()
            for line in group:
                positive_answers.update(set(line))
        else:
            positive_answers = set(group[0])
            for line in group[1:]:
                positive_answers.intersection_update(set(line))
        count += len(positive_answers)
    return count


if __name__ == '__main__':
    print('Part 1:', process(1))
    print('Part 2:', process(2))
