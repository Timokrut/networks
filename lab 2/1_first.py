import random

def simulate(p, trials=100000):
    total_transmissions = 0
    
    for _ in range(trials):
        count = 0
        while True:
            count += 1
            if random.random() > p:  # успех
                break
        total_transmissions += count
    
    return total_transmissions / trials

# пример
p = 0.3
print("Имитация:", simulate(p))
print("Теория:", 1/(1-p))