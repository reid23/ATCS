def nim(n):
    l = 0, 1
    for i in range(n): l = l[1], int(l[0]*l[1]==0)
    return l[0]

print(*[nim(i) for i in range(100)], sep = '\n')

'''
[0, 1] -> [1, 1]

[0, 1]
[1, -1]

'''