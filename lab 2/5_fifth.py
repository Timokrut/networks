import random

def simulate(p, tau, packets=10000):
    total_time = 0
    successful_packets = 0

    for _ in range(packets):
        while True:
            # время передачи пакета = 1
            total_time += 1

            # проверка ошибки
            if random.random() > p:
                # пакет доставлен успешно
                total_time += tau  # ожидание квитанции
                successful_packets += 1
                break
            # иначе повторная передача (ничего не добавляем кроме времени передачи)

    return successful_packets / total_time


def theoretical_eta(p, tau):
    return (1 - p) / (1 + p * tau)


# пример запуска
p = 0.2
tau = 3

sim_eta = simulate(p, tau)
theory_eta = theoretical_eta(p, tau)

print("Моделирование η =", sim_eta)
print("Теория        η =", theory_eta)

# ЛОГИ
def simulate_with_log(p, tau, packets=3):
    time = 0

    for i in range(packets):
        print(f"\nПакет {i+1}:")

        while True:
            time += 1
            print(f"  t={time}: передача пакета")

            if random.random() > p:
                print(f"  t={time}: пакет принят успешно")
                time += tau
                print(f"  t={time}: ожидание квитанции τ={tau}")
                print(f"  t={time}: квитанция получена")
                break
            else:
                print(f"  t={time}: ошибка, повтор")

    return time