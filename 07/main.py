import re

bag_re = re.compile(r'(\d*) ?(\w+ \w+) bags?')


def get_rules():
    child_map = {}
    parent_map = {}
    with open('input.txt') as file:
        for line in file:
            all_bags = [(qty, bag) for (qty, bag) in bag_re.findall(line) if bag != 'no other']
            outer = all_bags[0][1]
            inner_tuples = [(int(qty), bag) for (qty, bag) in all_bags[1:]]
            inner_unique = [entry[1] for entry in inner_tuples]

            child_map[outer] = inner_tuples
            for bag in inner_unique:
                parent_map[bag] = parent_map.setdefault(bag, []) + [outer]

    return child_map, parent_map


def part_1():
    _, parent_map = get_rules()

    bags = set(parent_map['shiny gold'])
    done = False
    while not done:
        # add potential containers to bag list
        new_bags = bags.union({
            container
            for bag in bags
            for container in parent_map.get(bag, [])
        })
        # keep going until the bag list no longer grows
        if bags == new_bags:
            done = True
        bags = new_bags

    print(len(bags), 'bags can eventually contain a shiny gold one')


def must_contain(container, child_map):
    num = 0
    for qty, bag in child_map[container]:
        num += qty * (must_contain(bag, child_map) + 1)
    return num


def part_2():
    child_map, _ = get_rules()
    print(
        must_contain('shiny gold', child_map),
        'bags in total inside a shiny gold bag'
    )


if __name__ == '__main__':
    part_1()
    part_2()
