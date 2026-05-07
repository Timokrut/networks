import random


p = 0.3
messages = 1000

total_transmissions = 0

for _ in range(messages):
    attempts = 0

    while True:
        attempts += 1
        r = random.random()

        # успешная передача
        if r > p:
            break

    total_transmissions += attempts

# среднее число передач
average = total_transmissions / messages

# теоретическое значение
theory = 1 / (1 - p)

print("Вероятность ошибки p =", p)
print("Имитационное среднее =", average)
print("Теоретическое значение =", theory)