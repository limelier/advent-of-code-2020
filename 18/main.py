from collections import deque


def generate():
    with open('input.txt') as file:
        for line in file:
            yield line.strip().replace(' ', '')


def calc(line):
    i = 0
    accumulator = 0
    crt_num = 0
    crt_op = None
    while i < len(line):
        c = line[i]
        if c.isnumeric():
            crt_num = crt_num * 10 + int(c)
        elif c in '+*':
            if crt_op is None:
                accumulator = crt_num
            elif crt_op == '+':
                accumulator += crt_num
            elif crt_op == '*':
                accumulator *= crt_num
            crt_num = 0
            crt_op = c
        elif c == '(':
            crt_num, j = calc(line[i+1:])
            i += j + 1
        elif c == ')':
            break
        i += 1

    if crt_op is None:
        accumulator = crt_num
    elif crt_op == '+':
        accumulator += crt_num
    elif crt_op == '*':
        accumulator *= crt_num

    return accumulator, i


def part_1():
    print(sum(calc(line)[0] for line in generate()))


def parse_expression(expr):
    left, expr = parse_addition(expr)
    if expr and expr[0] == '*':
        right, expr = parse_expression(expr[1:])
        left *= right
    return left, expr


def parse_addition(expr):
    left, expr = parse_term(expr)
    if expr and expr[0] == '+':
        right, expr = parse_addition(expr[1:])
        left += right
    return left, expr


def parse_term(expr):
    val = 0
    if expr:
        if expr[0].isnumeric():
            val, expr = parse_number(expr)
        elif expr[0] == '(':
            val, expr = parse_expression(expr[1:])
            expr = expr[1:]
    return val, expr


def parse_number(expr: str):
    idx = 0
    while idx < len(expr) and expr[idx].isnumeric():
        idx += 1
    return int(expr[:idx]), expr[idx:]


def part_2():
    print(sum(parse_expression(line)[0] for line in generate()))


if __name__ == '__main__':
    part_1()
    part_2()
