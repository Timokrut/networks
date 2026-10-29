import math

def average_number_slots(arrivals, departures, slots):
    diff = [0] * (slots + 1)

    for arrival, departure in zip(arrivals, departures):
        # Сообщение становится доступно на границе следующего окна
        start = math.ceil(arrival)

        # Считаем присутствие сообщения на началах слотов
        start = min(start, slots)
        end = min(int(departure), slots)

        if start < end:
            diff[start] += 1
            diff[end] -= 1

    current_n = 0
    total_n = 0

    for slot in range(slots):
        current_n += diff[slot]
        total_n += current_n

    return total_n / slots

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

