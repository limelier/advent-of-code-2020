import re
from dataclasses import dataclass
from typing import Set

line_re = re.compile(r'^(.+) \(contains (.+)\)\n$')


@dataclass
class Product:
    ingredients: Set[str]
    allergens: Set[str]


products = []
with open('input.txt') as file:
    for line in file:
        match = line_re.fullmatch(line)
        ingredients = set(match[1].split(' '))
        allergens = set(match[2].split(', '))
        products.append(Product(ingredients, allergens))

all_alergens = set.union(*[product.allergens for product in products])

possible_words = {}
for allergen in all_alergens:
    possible_words[allergen] = set.intersection(*[product.ingredients for product in products if allergen in product.allergens])
    print(f'{allergen} is one of {possible_words}')

allergen_translations = {}
while not set(possible_words.keys()).issubset(set(allergen_translations.keys())):
    certain_allergen = min(possible_words.keys(), key=lambda k: len(possible_words[k]))
    assert len(possible_words[certain_allergen]) == 1
    translation = possible_words.pop(certain_allergen).pop()
    allergen_translations[certain_allergen] = translation
    for key in possible_words.keys():
        possible_words[key].discard(translation)
    print(f'{certain_allergen} is definitely "{translation}"')

not_allergens = sum(
    1
    for product in products
    for ingredient in product.ingredients
    if ingredient not in allergen_translations.values()
)

print(f'{not_allergens} words are not allergens')

print('Dangerous ingredient list:')
print(','.join(allergen_translations[allergen] for allergen in sorted(all_alergens)))
