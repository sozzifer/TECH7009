import numpy as np
import random
import plotly.graph_objects as go


def generate_draws(num, total, draws):
    draws = list(range(1, draws + 1))
    probability = round((num/total), 2)
    my_tickets_list = []
    tickets_string_list = []
    my_tickets_string_list = []
    winning_ticket_list = []
    win_list = [0]
    draw_list = [0]
    prob_list = [0]
    win_rate = 0
    for draw in draws:
        winner = False

        my_tickets = random.sample(range(1, int(total) + 1), int(num))
        my_tickets_list.append(my_tickets)

        tickets_string = [str(x) for x in my_tickets]
        tickets_string_list.append(tickets_string)

        my_tickets_string = ", ".join(tickets_string)
        my_tickets_string_list.append(my_tickets_string)

        winning_ticket = np.random.randint(1, int(total) + 1)
        winning_ticket_list.append(winning_ticket)

        for ticket in my_tickets:
            if ticket == winning_ticket:
                winner = True

        if winner == True:
            win_list.append(win_list[-1] + 1)
        else:
            win_list.append(win_list[-1])

        prob_list.append(prob_list[-1] + probability)
        draw_list.append(draw)
        win_rate = win_list[-1]/draw_list[-1]
    return my_tickets_list, my_tickets_string_list, winning_ticket_list, draw_list, win_list, prob_list, win_rate


# print(f"My tickets: {my_tickets_list}")
# print(f"My tickets (strings): {my_tickets_string_list}")
# print(f"Winning tickets: {winning_ticket_list}")
# print(f"draw_list: {draw_list}")
# print(f"win_list: {win_list}")
# print(f"prob_list: {prob_list}")
# print(f"win_rate: {win_rate}\n")