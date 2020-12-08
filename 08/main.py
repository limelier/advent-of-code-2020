def read_instructions():
    instructions = []
    with open('input.txt') as file:
        for line in file:
            instr, val = line.strip().split(' ')[:2]
            val = int(val)
            instructions.append((instr, val))
    return instructions


def execute(instructions, silent=False):
    acc = 0
    iptr = 0
    visited = [0 for _ in instructions]
    while 0 <= iptr < len(instructions):
        visited[iptr] += 1
        if visited[iptr] > 1:
            if not silent:
                print('Encountered instruction a second time, terminating.')
            break
        instr, val = instructions[iptr]
        if instr == 'acc':
            acc += val
        elif instr == 'jmp':
            iptr += val
            continue
        iptr += 1
    if not silent:
        print('Finished execution with acc value %d.' % acc)
    return acc, iptr


def modify_and_run(instructions):
    icnt = len(instructions)
    for iptr in range(icnt):
        instr, val = instructions[iptr]
        if instr == 'acc':
            continue

        new_instruction = (
            'jmp' if instr == 'nop' else 'nop',
            val,
        )

        new_instructions = instructions.copy()
        new_instructions[iptr] = new_instruction

        acc, end_iptr = execute(new_instructions, silent=True)
        if end_iptr == icnt:
            print('Modifying line %d worked!' % (iptr + 1))
            print('Finished running modified program, with acc value %d.' % acc)


if __name__ == '__main__':
    input_instructions = read_instructions()

    print('Part one:')
    execute(input_instructions)

    print('\nPart two:')
    modify_and_run(input_instructions)

