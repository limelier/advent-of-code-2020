import re
from typing import List


def get_input():
    rules = {}

    with open('input.txt') as file:
        for line in file:
            line = line.strip()
            if line:
                index, contents = line.split(':')
                index = int(index)
                contents = contents.strip()
                if '"' in contents:
                    # if literal, extract letter
                    contents = contents[1]
                else:
                    if '|' not in contents:
                        contents = [int(num) for num in contents.split(' ')]
                    else:
                        cont1, cont2 = contents.split(' | ')
                        cont1 = [int(num) for num in cont1.split(' ')]
                        cont2 = [int(num) for num in cont2.split(' ')]
                        contents = cont1, cont2
                rules[index] = contents
            else:
                break

        strings = [line.strip() for line in file]
    return rules, strings


def collapse_rules(rules, root=0):
    rule = rules[root]

    if isinstance(rule, str):
        return rule
    elif isinstance(rule, List):
        return ''.join(collapse_rules(rules, idx) for idx in rule)
    else:
        left, right = rule
        left = ''.join(collapse_rules(rules, idx) for idx in left)
        right = ''.join(collapse_rules(rules, idx) for idx in right)
        return f'({left}|{right})'


def part_1():
    rules, strings = get_input()
    pattern = collapse_rules(rules)
    regex = re.compile(r'^' + pattern + r'$')
    print(sum(1 for string in strings if regex.fullmatch(string)))


def part_2():
    rules, strings = get_input()
    # rule 0: (8)(11) = (42){n}(42){m}(31){m} = (42){m+n}(31){m}
    # a{m+n}b{m} is not possible with pure regex, so we will test for different values of m up to 50
    rule_31 = collapse_rules(rules, 31)
    rule_42 = collapse_rules(rules, 42)
    regexes = [
        re.compile('^' + rule_42 + '+' + rule_42 + '{' + str(i) + '}' + rule_31 + '{' + str(i) + '}$')
        for i in range(1, 51)
    ]
    print(sum(1 for string in strings if any(regex.fullmatch(string) for regex in regexes)))


if __name__ == '__main__':
    part_1()
    part_2()
