import random

def simulate_stop_and_wait(
    num_messages=1000,
    p_forward=0.1,     
    p_backward=0.0,    
    max_retries=None,  
    tau=1             
):
    time = 0
    successful = 0
    total_sent = 0

    for msg_id in range(num_messages):
        retries = 0
        while True:
            total_sent += 1
            time += 1  # передача сообщения

            # ошибка в прямом канале
            if random.random() < p_forward:
                ack = False
            else:
                ack = True

            time += tau  # ожидание квитанции

            # ошибка в обратном канале
            if ack and random.random() < p_backward:
                ack = False

            if ack:
                successful += 1
                break
            else:
                retries += 1
                if max_retries is not None and retries >= max_retries:
                    break
    
    average_transmissions = total_sent / num_messages

    return {
        "successful_messages": successful,
        "total_sent": total_sent,
        "average_transmissions": average_transmissions,
        "total_time": time
    }



result = simulate_stop_and_wait(
    num_messages=1000,
    p_forward=0.2,
    p_backward=0.0,
    max_retries=None,
    tau=2
)

print(result)

