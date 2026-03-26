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

# a(x) = m(x)*x^r + c(x)
def encode(m, g):
    r = len(g) - 1
    padded = m + [0]*r
    remainder = mod2div(padded, g)
    return m + remainder

def count_Pe(g, k, p, eps):
    Ne = 0 # счетчик ошибок декодирования

    r = len(g) - 1 # deg(g(x))
    n = k + r # вычисление длины кодового слова
    
    N = int(9/(4*eps**2)) # количество экспериментов

    for _ in range(N):
        # генерация случайного сообщения
        m = [random.randint(0,1) for _ in range(k)]

        # формирование кодового слова 
        a = encode(m, g)

        # генерация случайного вектора ошибок. P(1) = p. P(0) = 1 - p. 
        e = []
        for _ in range(n):
            if random.random() < p:
                e.append(1)
            else:
                e.append(0)

        # вычисление выхода канала b
        b = xor(a, e)

        # вычисление синдрома
        s = mod2div(b, g)

        if sum(s) == 0 and sum(e) != 0:
            Ne += 1

    Pe = Ne / N
    return Pe

g = [1, 0, 1, 1]  # g(x)=x^3+x+1
k = 4             # длина кодируемой последовательности
p = 0.05          # вероятность ошибки в канале
eps = 0.01        # требуемая точность результатов

Pe = count_Pe(g, k, p, eps)

print("Pe:", Pe)

# print(mod2div([1, 0, 1, 0, 0, 0, 0], [1, 0, 1, 1]))