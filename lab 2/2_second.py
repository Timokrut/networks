import random

p = 0.3
n = 3

messages = 1000

total_transmissions = 0

for _ in range(messages):
    attempts = 0

    for _ in range(n):
        attempts += 1
        r = random.random()

        # успешная передача
        if r > p:
            break

    total_transmissions += attempts

average = total_transmissions / messages

theory = (1 - p**n) / (1 - p)

print("p =", p)
print("n =", n)

print("Имитационное среднее =", average)
print("Теоретическое значение =", theory)
