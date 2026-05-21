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

print(f"Вероятность ошибки p = {p}")
print(f"Имитационное среднее = {average:.2f}")
print(f"Теоретическое значение ={theory:.2f}")