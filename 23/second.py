class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

    def nth_next(self, n):
        node = self
        for _ in range(n):
            node = node.next
        return node

    def next_n(self, n):
        nodes = [self.next]
        for _ in range(n - 1):
            nodes.append(nodes[-1].next)
        return nodes


def wrap(x):
    """Wrap x to between 1 and 1_000_000"""
    if not 0 <= x <= 1_000_000:
        x %= 1_000_000
    if x == 0:
        x = 1_000_000
    return x


def main():
    puzzle_input = '538914762'
    cups = [int(x) for x in puzzle_input] + [x for x in range(10, 1_000_001)]

    nodes = [Node(cup) for cup in cups]
    for idx in range(len(nodes) - 1):
        nodes[idx].next = nodes[idx + 1]

    nodes[-1].next = nodes[0]
    selected = nodes[0]

    nodes = sorted(nodes[0:9], key=lambda n: n.val) + nodes[9:]

    for step in range(10_000_000):
        # if step % 100_000 == 0:
        #     print(f'round {step}')
        #     node = selected
        #     for _ in range(10):
        #         print(node.val, end=' -> ')
        #         node = node.next
        #     print('\n')

        removed = selected.next_n(3)
        selected.next = removed[-1].next

        dest_val = wrap(selected.val - 1)
        removed_vals = {node.val for node in removed}
        while dest_val in removed_vals:
            dest_val = wrap(dest_val - 1)

        dest = nodes[dest_val - 1]
        removed[-1].next = dest.next
        dest.next = removed[0]

        selected = selected.next

    node_one = nodes[0]

    print(node_one.next.val * node_one.next.next.val)


if __name__ == '__main__':
    main()
