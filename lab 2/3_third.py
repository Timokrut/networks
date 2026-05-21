import random

p = 0.2     
p_back = 0.1

messages = 1000

total_transmissions = 0

for _ in range(messages):
    attempts = 0
    
    while True:
        attempts += 1
        
        data_ok = random.random() > p
        ack_ok = random.random() > p_back

        if data_ok and ack_ok:
            break

    total_transmissions += attempts

average = total_transmissions / messages
theory = 1 / ((1 - p) * (1 - p_back))

print(f"p = {p}")
print(f"p_обр = {p_back}")
print(f"Имитация = {average:.2f}")
print(f"Теория = {theory:.2f}")