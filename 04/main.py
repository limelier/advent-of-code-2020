from typing import Dict
import re


def get_attr(line):
    pairs = [pair.split(':') for pair in line.strip().split(' ')]
    return [(pair[0], pair[1]) for pair in pairs]


def gen_passports():
    passport = {}
    with open('input.txt') as file:
        for line in file:
            if line == '\n':
                yield passport
                passport = {}
            else:
                tuples = get_attr(line)
                for key, value in tuples:
                    passport[key] = value


def valid_1(passport):
    """Passport has all required fields."""
    return all(
        attr in passport.keys()
        for attr in {
            'byr',
            'iyr',
            'eyr',
            'hgt',
            'hcl',
            'ecl',
            'pid',
            # 'cid',
        }
    )


year_re = re.compile(r'\d{4}')
hgt_re = re.compile(r'(\d+)(cm|in)')
hcl_re = re.compile(r'#[0-9a-f]{6}')
pid_re = re.compile(r'\d{9}')


def valid_year(passport, key, least, most):
    return key in passport.keys() \
           and year_re.fullmatch(passport[key]) \
           and least <= int(passport[key]) <= most


def valid_hgt(passport):
    if 'hgt' not in passport.keys():
        return False
    hgt = passport['hgt']
    match = hgt_re.fullmatch(hgt)
    if not match:
        return False
    if match[2] == 'cm':
        return 150 <= int(match[1]) <= 193
    else:
        return 59 <= int(match[1]) <= 76


def valid_hcl(passport):
    return 'hcl' in passport.keys() and hcl_re.fullmatch(passport['hcl'])


def valid_ecl(passport):
    return 'ecl' in passport.keys()\
           and passport['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def valid_pid(passport):
    return 'pid' in passport.keys() and pid_re.fullmatch(passport['pid'])


def valid_2(passport: Dict[str, str]):
    """Passport has all required fields, with valid values for each."""
    return all([
        valid_year(passport, 'byr', 1920, 2002),
        valid_year(passport, 'iyr', 2010, 2020),
        valid_year(passport, 'eyr', 2020, 2030),
        valid_hgt(passport),
        valid_hcl(passport),
        valid_ecl(passport),
        valid_pid(passport),
    ])


def main():
    print(sum(
        1
        for passport in gen_passports()
        if valid_2(passport)
    ))


if __name__ == '__main__':
    main()
