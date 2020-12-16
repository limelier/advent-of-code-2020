import re
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Rule:
    label: str
    lower_range: Tuple[int, int]
    upper_range: Tuple[int, int]


rule_re = re.compile(r'([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)')


# ticket_re = re.compile(r'(\d+,)+(\d+)')


def process_input():
    stage = 'rules'  # rules, own, nearby, done
    rules = []
    nearby_tickets = []

    with open('input.txt') as file:
        for line in file:
            line = line.strip()

            if stage == 'rules':
                if line == '':
                    stage = 'own'
                    file.readline()  # consume 'your ticket' header
                    continue

                result = rule_re.fullmatch(line)
                rule = Rule(
                    result[1],
                    (
                        int(result[2]),
                        int(result[3]),
                    ),
                    (
                        int(result[4]),
                        int(result[5]),
                    )
                )
                rules.append(rule)
            elif stage == 'own':
                own_ticket = [int(num) for num in line.split(',')]
                file.readline()  # consume blank line
                file.readline()  # consume 'nearby tickets' header
                stage = 'nearby'
            else:
                ticket = [int(num) for num in line.split(',')]
                nearby_tickets.append(ticket)

    return rules, own_ticket, nearby_tickets


def condense_intervals(intervals):
    intervals.sort(key=lambda interval: interval[0])
    stack = [intervals[0]]

    for lo, hi in intervals[1:]:
        top_lo, top_hi = stack[-1]
        if lo > top_hi:
            stack.append((lo, hi))
        elif hi > top_hi:
            stack[-1] = top_lo, hi

    return stack


def part_1(rules, nearby_tickets):
    valid_intervals = []
    for rule in rules:
        valid_intervals.append(rule.lower_range)
        valid_intervals.append(rule.upper_range)
    valid_intervals = condense_intervals(valid_intervals)

    error_rate = 0
    valid_tickets = []
    for ticket in nearby_tickets:
        ok = True
        for value in ticket:
            if not any(lo <= value <= hi for lo, hi in valid_intervals):
                error_rate += value
                ok = False
        if ok:
            valid_tickets.append(ticket)

    print(f'Error rate: {error_rate}')
    return valid_tickets


def part_2(labels, own_ticket, valid_tickets):
    possible_labels = [labels.copy() for _ in own_ticket]

    for ticket in valid_tickets:
        for idx, val in enumerate(ticket):
            possible_labels[idx] = [
                rule
                for rule in possible_labels[idx]
                if rule.lower_range[0] <= val <= rule.lower_range[1]
                or rule.upper_range[0] <= val <= rule.upper_range[1]
            ]

    # reduce rule sets to label lists, annotate lists with index to facilitate
    # order recovery after sorting
    possible_labels = sorted([
        ({rule.label for rule in labels}, idx)
        for (idx, labels) in enumerate(possible_labels)
    ], key=lambda x: len(x[0]))

    taken_labels = set()
    for idx, (labels, old_idx) in enumerate(possible_labels):
        labels.difference_update(taken_labels)
        possible_labels[idx] = labels, old_idx
        taken_labels.update(labels)

    assert all(len(labels) == 1 for (labels, _) in possible_labels)

    fields = [
        labels.pop()
        for (labels, _) in sorted(
            possible_labels,
            key=lambda x: x[1]
        )
    ]

    ticket = {k: v for k, v in zip(fields, own_ticket)}

    product = 1
    for key in fields:
        if key.startswith('departure'):
            value = ticket[key]
            print(f'{key}: {value}')
            product *= value
    print(f'The product is {product}')


def main():
    rules, own_ticket, nearby_tickets = process_input()
    valid_tickets = part_1(rules, nearby_tickets)
    part_2(rules, own_ticket, valid_tickets)


if __name__ == '__main__':
    main()
