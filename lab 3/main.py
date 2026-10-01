import random
import matplotlib.pyplot as plt
import math

random.seed(4)

N_MESSAGES = 50_000
lambdas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

# Генерация моментов появления сообщений
def generate_arrivals(lmbd, n):
    arrivals = []
    time = 0.0

    for _ in range(n):
        # Интервалы между сообщениями имеют экспоненциальное распределение
        time += random.expovariate(lmbd)
        arrivals.append(time)

    return arrivals


# Имитация асинхронной СМО
def simulate_async(arrivals):
    departures = []
    delays = []

    next_free_time = 0.0

    for arrival in arrivals:
        start = max(arrival, next_free_time)
        departure = start + 1.0

        delays.append(departure - arrival)
        departures.append(departure)

        next_free_time = departure

    return delays, departures


# Имитация синхронной CMO
def simulate_sync(arrivals):
    departures = []
    delays = []

    next_free_window = 0.0

    for arrival in arrivals:
        # Передавать можно только в начале следующего окна
        window_start = math.ceil(arrival)

        start = max(window_start, next_free_window)
        departure = start + 1.0

        delays.append(departure - arrival)
        departures.append(departure)

        next_free_window = departure

    return delays, departures


# Среднее число сообщений в системе.
def average_number(arrivals, departures):
    events = []

    for arrival in arrivals:
        events.append((arrival, 1))

    for departure in departures:
        events.append((departure, -1))

    events.sort()

    current_n = 0 # сколько сообщений в системе прямо сейчас
    area = 0.0
    previous_time = 0.0

    for time, change in events:
        area += current_n * (time - previous_time)
        current_n += change
        previous_time = time

    return area / previous_time


# Результаты моделирования
sync_d = []
async_d = []

sync_n = []
async_n = []

theory_d_sync = []
theory_d_async = []
theory_n = []


for lmbd in lambdas:
    arrivals = generate_arrivals(lmbd, N_MESSAGES)

    # Асинхронная система
    delays, departures = simulate_async(arrivals)

    async_d.append(sum(delays) / len(delays))
    async_n.append(average_number(arrivals, departures))

    # Синхронная система
    delays, departures = simulate_sync(arrivals)

    sync_d.append(sum(delays) / len(delays))
    sync_n.append(average_number(arrivals, departures))

    # Теория
    n = lmbd * (2 - lmbd) / (2 * (1 - lmbd))

    theory_n.append(n)
    theory_d_async.append(n / lmbd)
    theory_d_sync.append(n / lmbd + 0.5)

# Резултаты
print("lambda | d_sync | d_async | N_sync | N_async")

for i, lmbd in enumerate(lambdas):
    print(
        f"{lmbd:5.1f} | "
        f"{sync_d[i]:7.3f} | "
        f"{async_d[i]:7.3f} | "
        f"{sync_n[i]:7.3f} | "
        f"{async_n[i]:7.3f}"
    )


# График средней задержки
plt.figure()

plt.plot(lambdas, sync_d, "o-", label="Синхронная, моделирование")
plt.plot(lambdas, async_d, "o-", label="Асинхронная, моделирование")

plt.plot(lambdas, theory_d_sync, "--", label="Синхронная, теория")
plt.plot(lambdas, theory_d_async, "--", label="Асинхронная, теория")

plt.xlabel("λ")
plt.ylabel("Средняя задержка d(λ)")
plt.title("Средняя задержка")
plt.grid()
plt.legend()

plt.show()


# График среднего числа сообщений
plt.figure()

plt.plot(lambdas, sync_n, "o-", label="Синхронная, моделирование")
plt.plot(lambdas, async_n, "o-", label="Асинхронная, моделирование")
plt.plot(lambdas, theory_n, "--", label="Теория")

plt.xlabel("λ")
plt.ylabel("Среднее число сообщений N(λ)")
plt.title("Среднее число сообщений в системе")
plt.grid()
plt.legend()

plt.show()