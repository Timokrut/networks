import random

def simulate(p, tau, T_total=100000):
    time = 0
    useful_time = 0
    successful = 0

    while time < T_total:
        # передача кадра
        time += 1
        
        if random.random() < p:
            # ошибка → повтор
            time += tau
        else:
            # успех
            time += tau
            useful_time += 1
            successful += 1

    eta = useful_time / time
    return eta

# тест
p = 0.2
tau = 2

eta_sim = simulate(p, tau)
eta_theory = (1 - p) / (1 + tau)

print("Моделирование:", eta_sim)
print("Теория:", eta_theory)


# import random

# def simulate(p, tau, N=5):
#     time = 0

#     for frame in range(1, N+1):
#         print(f"\nt={time}: отправка кадра #{frame}")
#         time += 1

#         while True:
#             if random.random() < p:
#                 print(f"t={time}: ошибка (кадр #{frame})")
#                 time += tau
#                 print(f"t={time}: повтор кадра #{frame}")
#                 time += 1
#             else:
#                 print(f"t={time}: успех, ACK получен")
#                 time += tau
#                 break

#     print("\nИтоговое время:", time)

# simulate(p=0.3, tau=2)