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
RED    = "\033[91m"
GREEN  = "\033[92m"

p = 0.3
tau = 2
messages = 1000

t = 0
i = 1

# packet_id, time_sent, success
in_flight = []

while i <= messages or len(in_flight) != 0:
    if i <= messages:
        r = random.random()
        in_flight.append((i, t, r > p))
        logging.info(f"[t={t}] {BLUE}SEND{RESET} packet {i}")
        i += 1

    ready = [pkt for pkt in in_flight if pkt[1] + tau <= t]

    for pkt in ready:
        pid, send_time, success = pkt

        if success:
            logging.info(f"[t={t + 1}] {GREEN}SUCCESS{RESET} packet {pid}")
            in_flight.remove(pkt)

        else:
            logging.info(f"[t={t + 1}] {RED}ERROR{RESET} packet {pid}")
            in_flight.clear()
            i = pid
    
    t += 1

n_sim = messages / t
n_theory = (1 - p) / (1 + p * tau)

print("p =", p)
print("tau =", tau)
print(f"Имитация η = {n_sim}")
print(f"Теория η = {n_theory}")