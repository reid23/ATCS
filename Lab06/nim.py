def nim(n):
    l = 0, 1
    for i in range(n): l = l[1], int(not(l[0] or l[1]))
    return l[0]

print(*[nim(i) for i in range(100)], sep = '\n')

'''
[0, 1] -> [1, 1]

[0, 1]
[1, -1]

'''