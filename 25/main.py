n = 7
i = 0
while n != 335121:
    i += 1
    n *= 7
    n %= 20201227

print(i)

m = 363891
while i > 0:
    m *= 363891
    m %= 20201227
    i -= 1

print(m)
