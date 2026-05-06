import random
import numpy as np


def simulate_once(p, p_back, n_max=None):
    """
    Моделирует передачу одного сообщения
    p       — ошибка в прямом канале
    p_back  — ошибка в обратном канале
    n_max   — максимум попыток (None = без ограничения)
    """
    attempts = 0

    while True:
        attempts += 1

        # ошибка в прямом канале
        forward_error = random.random() < p

        # ошибка в обратном канале
        back_error = random.random() < p_back

        # успех
        if not forward_error and not back_error:
            return attempts

        # ограничение
        if n_max is not None and attempts >= n_max:
            return attempts


def simulate(p, p_back, n_max=None, trials=100000):
    results = [simulate_once(p, p_back, n_max) for _ in range(trials)]
    return np.mean(results)


# ====== ТЕОРИЯ ======

def theoretical_mean(p, p_back, n_max=None):
    q = 1 - (1 - p) * (1 - p_back)

    if n_max is None:
        return 1 / (1 - q)
    else:
        return (1 - (1 - q)**n_max) / q


# ====== ЗАПУСК ======

p = 0.2
p_back = 0.1
n = 5

sim_unlim = simulate(p, p_back)
sim_lim = simulate(p, p_back, n_max=n)

th_unlim = theoretical_mean(p, p_back)
th_lim = theoretical_mean(p, p_back, n_max=n)

print("=== Без ограничения ===")
print("Имитация:", sim_unlim)
print("Теория:  ", th_unlim)

print("\n=== С ограничением ===")
print("Имитация:", sim_lim)
print("Теория:  ", th_lim)