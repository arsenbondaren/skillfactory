

c = 0
def list_min(a):
    global c
    c += 1
    print(f'{c}: {a}')
    count = len(a)
    if count == 1:
        return a[0]
    #return a[0] if a[0] < list_min(a[1:]) else list_min(a[1:])
    return list_min(a[1:]) if a[0] > a[count-1] else list_min(a[:count-1])

s = [-4, 56, -30, 10, -3, -100, 12, -2]
print(list_min(s))