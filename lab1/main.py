import random

def xor(a, b):
    return [i ^ j for i, j in zip(a, b)]

def mod2div(dividend, divisor):
    dividend = dividend[:]
    n = len(divisor)

    for i in range(len(dividend) - n + 1):
        if dividend[i] == 1:
            for j in range(n):
                dividend[i+j] ^= divisor[j]

    return dividend[-(n-1):]

def encode_crc(m, g):
    r = len(g) - 1
    padded = m + [0]*r
    remainder = mod2div(padded, g)
    return m + remainder

def simulate(g, k, p, eps):
    r = len(g) - 1
    n = k + r

    N = int(9/(4*eps**2))
    Ne = 0

    for _ in range(N):
        # сообщение
        m = [random.randint(0,1) for _ in range(k)]

        # кодирование
        a = encode_crc(m, g)

        # ошибки
        e = []
        for _ in range(n):
            if random.random() < p:
                e.append(1)
            else:
                e.append(0)

        # канал
        b = xor(a, e)

        # синдром
        s = mod2div(b, g)

        if all(x == 0 for x in s) and any(x == 1 for x in e):
            Ne += 1

    Pe = Ne / N
    return Pe

# пример
g = [1,0,1,1]     # g(x)=x^3+x+1
k = 8
p = 0.05
eps = 0.01

Pe = simulate(g, k, p, eps)

print("Вероятность ошибки декодирования:", Pe)