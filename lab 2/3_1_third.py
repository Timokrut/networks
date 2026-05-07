import random

p = 0.2
p_back = 0.1

n = 3

messages = 1000

total_transmissions = 0
lost = 0

for msg_id in range(messages):
    attempts = 0

    for _ in range(n):
        attempts += 1

        data_ok = random.random() > p
        ack_ok = random.random() > p_back

        if data_ok and ack_ok:
            break

    total_transmissions += attempts

average = total_transmissions / messages

a = (1 - p) * (1 - p_back)
theory = (1 - (1 - a)**n) / a

print("Имитация среднего =", average)
print("Теория =", theory)