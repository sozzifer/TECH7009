import numpy as np
import random


def generate_tickets(total, num):
    my_tickets = random.sample(range(1, int(total) + 1), int(num))
    tickets_string = [str(x) for x in my_tickets]
    my_tickets_string = ", ".join(tickets_string)
    winning_ticket = np.random.randint(1, int(total) + 1, size=(1))
    return my_tickets, my_tickets_string, winning_ticket
