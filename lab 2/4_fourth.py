import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

# Сброс цвета
RESET = "\033[0m"

# Цвета
BLUE   = "\033[94m"
YELLOW = "\033[93m"
RED    = "\033[91m"
GREEN  = "\033[92m"

p = 0.3        # ошибка прямого канала
tau = 2        # задержка ACK
messages = 1000

t = 0

for i in range(1, messages + 1):
    attempts = 0

    while True:
        attempts += 1
        r = random.random()

        logging.info(f"[t={t}] {BLUE}SEND{RESET} packet {i}, attempt {attempts}")

        t += 1

        logging.info(f"[t={t}] {YELLOW}WAIT{RESET} for ACK tau={tau}")

        if r > p:
            t += tau
            logging.info(f"[t={t}] {GREEN}SUCCESS{RESET} packet {i}")
            break
        else:
            t += tau
            logging.info(f"[t={t}] {RED}ERROR{RESET} packet {i}")

n_sim = messages / t
n_theory = (1 - p) / (1 + tau)

print("p =", p)
print("tau =", tau)
print(f"Имитация η = {n_sim:.2f}")
print(f"Теория η = {n_theory:.2f}")