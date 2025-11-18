 
from random import choice, choices
from strategies.repeat import detect_repeat
from strategies.cycle import detect_cycle
from strategies.reaction import detect_reaction, predict_reaction_move
from strategies.frequency import detect_freq
from strategies.frequency_short_term import detect_freq_short_term



def player1(prev_play, opponent_history=[]):

    if (prev_play):
        opponent_history.append(prev_play)

    if (not hasattr(player1, "my_history")):
        player1.my_history = []

    counter = {"R": "P", "P": "S", "S": "R"}

    d1 = detect_repeat(opponent_history)
    if (d1["repeated_move"]):
        opp = d1["repeated_move"]
        my_move = counter[opp]
        player1.my_history.append(my_move)
        return my_move

    d3 = detect_reaction(player1.my_history, opponent_history)
    if (isinstance(d3, dict)):
        last_move = player1.my_history[-1]
        opp = predict_reaction_move(d3, last_move)
        if (opp):
            my_move = counter[opp]
            player1.my_history.append(my_move)
            return my_move

    d2 = detect_cycle(opponent_history)
    if (d2):
        cycle = d2[0]
        preds = []
        n = len(cycle)
        for i, c in enumerate(cycle):
            if (c == prev_play):
                preds.append(cycle[(i + 1) % n])
        if (preds):
            my_move = counter[choice(preds)]
            player1.my_history.append(my_move)
            return my_move

    d5 = detect_freq_short_term(opponent_history)
    if (d5["frequent_move_short_term"]):
        opp = choice(d5["frequent_move_short_term"])
        my_move = counter[opp]
        player1.my_history.append(my_move)
        return my_move

    d4 = detect_freq(opponent_history)
    if (d4["frequent_move"]):
        opp = choice(d4["frequent_move"])
        my_move = counter[opp]
        player1.my_history.append(my_move)
        return my_move

    my_move = choice(["R", "P", "S"])
    player1.my_history.append(my_move)
    return my_move








    
    

    
    
