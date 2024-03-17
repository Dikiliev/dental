
def calculte(a):
    for b in range(1, 11):
        print(f'{a} x {b} = {a * b}')


for a in range(1, 10):
    print(f'Таблица {a}')
    calculte(a)
    print()

