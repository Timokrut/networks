import random

def experiment(p, n):
    for i in range(1, n + 1):
        if random.random() > p:  # успех
            return i
    return n  # если все попытки неудачны

def simulate(p, n, trials=100000):
    total = 0
    for _ in range(trials):
        total += experiment(p, n)
    return total / trials

# пример
p = 0.3
n = 5
print("Теория:", (1 - p**n) / (1 - p))
print("Имитация:", simulate(p, n))