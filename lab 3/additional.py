import random
import matplotlib.pyplot as plt
from collections import deque
from mains import simulate_sync, average_number_slots


random.seed(4)


M = 4 # количество абонентов
p = 1 / M # вероятность передачи
SLOTS = 100000 # количество временных слотов
lambdas = [x / 20 for x in range(1, 19)] # список интенсивностей вх потока (0.05, 0.1, ..., 0.9)

# Генерируем пуассоновский входной поток сообщений для каждого абонента
def generate_arrivals(lmbd, m, slots):
    arrivals = []

    for user in range(m):
        user_arrivals = []
        time = 0.0

        while True:
            time += random.expovariate(lmbd / m)

            if time >= slots:
                break

            user_arrivals.append(time)
        arrivals.append(user_arrivals)

    return arrivals


# Симулируем ALOHA p и ALOHA 1 + p
def simulate_aloha(arrivals, p, slots, first_attempt_guaranteed=False):
    m = len(arrivals)
    queues = [deque() for _ in range(m)]
    next_arrival = [0] * m

    delays = []
    successful = 0
    total_messages = 0

    for slot in range(slots):
        # Среднее число сообщений в начале каждого окна
        total_messages += sum(len(queue) for queue in queues)

        # Определяем, какие пользователи пытаются передавать сообщение
        trying = []

        for user in range(m):
            if not queues[user]:
                continue

            first_try = not queues[user][0][1]

            if first_attempt_guaranteed and first_try:
                trying.append(user)
            
            elif random.random() < p:
                trying.append(user)

        # Один пользователь передает -> Успех
        if len(trying) == 1:
            user = trying[0]
            message = queues[user].popleft()

            delays.append(slot + 1 - message[0])
            successful += 1

        # Более одного пользователя передают -> Конфликт
        elif len(trying) > 1:
            if first_attempt_guaranteed:
                for user in trying:
                    queues[user][0][1] = True

        # Добавляем сообщения, пришедшие в течение этого слота.
        for user in range(m):
            while (next_arrival[user] < len(arrivals[user]) and
                   arrivals[user][next_arrival[user]] < slot + 1):
                arrival_time = arrivals[user][next_arrival[user]]
                queues[user].append([arrival_time, False])
                next_arrival[user] += 1

    average_delay = sum(delays) / len(delays) if delays else 0 # d(y) - средняя задержка
    average_number = total_messages / slots # N(y) - среднее число сообщений в системе
    output_rate = successful / slots #y_вых(y) - интенсивность выходного потока

    return average_delay, average_number, output_rate


# Проверка: M = 1, p = 1.
# Результаты должны быть близки к формулам синхронной M|D|1:
# N = lambda * (2 - lambda) / (2 * (1 - lambda))
# d = N / lambda + 0.5
def check():
    print("\nПроверка для M = 1, p = 1")
    print("lambda | N модель | N теория | d модель | d теория")

    check_slots = 100_000
    check_lambdas = [x/20 for x in range(1, 19)] # 0.05 ... 0.9

    aloha_d = []
    aloha_n = []

    sync_d = []
    sync_n = []

    theory_d = []
    theory_n = []
    
    for lmbd in check_lambdas:
        arrivals = generate_arrivals(lmbd, 1, check_slots)

        # ALOHA 
        d_aloha, n_aloha, output_aloha = simulate_aloha(
            arrivals, 1.0, check_slots, first_attempt_guaranteed=False
        )

        aloha_d.append(d_aloha)
        aloha_n.append(n_aloha)

        # Синхронная система
        delays, departures = simulate_sync(arrivals[0])
        
        sync_d.append(sum(delays) / len(delays))
        sync_n.append(average_number_slots(arrivals[0], departures, check_slots))

        n_theory = lmbd * (2 - lmbd) / (2 * (1 - lmbd))
        d_theory = n_theory / lmbd + 0.5

        theory_d.append(d_theory)
        theory_n.append(n_theory)

        print(f"{lmbd:5.1f} | {n_aloha:8.3f} | {n_theory:8.3f} | "
              f"{d_aloha:8.3f} | {d_theory:8.3f}")

    plot_check(
        check_lambdas,
        aloha_d,
        sync_d,
        theory_d,
        "Средняя задержка d(λ)",
        "Задержка"
    )

    plot_check(
        check_lambdas,
        aloha_n,
        sync_n,
        theory_n,
        "Среднее число сообщений N(λ)",
        "Количество сообщений"
    )

def plot_check(lambdas, aloha, sync, theory, title, ylabel):
    plt.figure(figsize=(10, 6))

    plt.plot(
        lambdas, aloha,
        "o-",
        markersize=8,
        label="ALOHA (M=1, p=1)",
    )

    plt.plot(
        lambdas, sync,
        "s-",
        markersize=5,
        label="Синхронная система",
    )

    plt.plot(
        lambdas, theory,
        "--",
        label="Теория"
    )

    plt.xlabel("Интенсивность входного потока λ")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    delay_p = []
    delay_1_p = []
    number_p = []
    number_1_p = []
    output_p = []
    output_1_p = []

    # Генерируем каждый поток
    all_arrivals = []
    for lmbd in lambdas:
        all_arrivals.append(generate_arrivals(lmbd, M, SLOTS))

    # ALOHA p
    for arrivals in all_arrivals:
        d, n, out = simulate_aloha(
            arrivals, p, SLOTS, first_attempt_guaranteed=False
        )
        delay_p.append(d)
        number_p.append(n)
        output_p.append(out)

    # ALOHA 1 + p
    for arrivals in all_arrivals:
        d, n, out = simulate_aloha(
            arrivals, p, SLOTS, first_attempt_guaranteed=True
        )
        delay_1_p.append(d)
        number_1_p.append(n)
        output_1_p.append(out)

    check()

    print("\nλ | λвых ALOHA p | λвых ALOHA 1+p")
    for i, lmbd in enumerate(lambdas):
        print(f"{lmbd:.2f} | {output_p[i]:.2f} | {output_1_p[i]:.2f}")

    # График средней задержки
    plt.figure()
    plt.plot(lambdas, delay_p, "o-", label="ALOHA p")
    plt.plot(lambdas, delay_1_p, "o-", label="ALOHA 1 + p")
    plt.xlabel("λ")
    plt.ylabel("Средняя задержка d(λ)")
    plt.title("Средняя задержка")
    plt.grid()
    plt.legend()

    # График среднего числа сообщений
    plt.figure()
    plt.plot(lambdas, number_p, "o-", label="ALOHA p")
    plt.plot(lambdas, number_1_p, "o-", label="ALOHA 1 + p")
    plt.xlabel("λ")
    plt.ylabel("Среднее число сообщений N(λ)")
    plt.title("Среднее число сообщений в системе")
    plt.grid()
    plt.legend()

    # График пропускной способности
    plt.figure()
    plt.plot(lambdas, output_p, "o-", label="ALOHA p")
    plt.plot(lambdas, output_1_p, "o-", label="ALOHA 1 + p")
    plt.plot(lambdas, lambdas, "--", label="Входная интенсивность λ")
    plt.xlabel("λ")
    plt.ylabel("Интенсивность успешных передач λ_out")
    plt.title("Пропускная способность")
    plt.grid()
    plt.legend()

    plt.show()


if __name__ == "__main__":
    main()
