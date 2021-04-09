def dec1(fn):
    x = {}
    def wrapper(n):
        nonlocal x
        if n in x:
            print(f'Возвращаем результат функции с аргументом {n} из словаря: {x[n]}')
        else:
            print(f'Добавляем результат функции с аргументом {n} в словарь')
            result = fn(n)
            x[n] = result
            print(f'Результат работы функции с аргументом {n} = {x[n]}')
        print(f' кэш {x}')
        return x[n]
    #print(x)
    return wrapper
#print(f"{c} функция wrapper перед {fn.__name__}({args},{kwargs})")
@dec1
def f(n):
    print(f"{f} функция {f.__closure__}()")
    return n * 123456789

f(2)
f(4)
f(2)