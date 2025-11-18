from random import choice, choices
from strategies.repeat import detect_repeat
from strategies.cycle import detect_cycle
from strategies.reaction import detect_reaction, predict_reaction_move
from strategies.frequency import detect_freq
from strategies.frequency_short_term import detect_freq_short_term
from RPS.consequences import consequence

def player2(prev_play, opponent_history = []):

    if(prev_play):
        opponent_history.append(prev_play)
    
    #history for my moves
    if (not hasattr(player2,"my_history")):
        player2.my_history = []
    
    if(not hasattr(player2,"previous_predictions")):
        player2.previous_predictions = {
            "repeat": None,
            "reaction": None,
            "cycle": None,
            "freq_short_term": None,
            "freq": None
        }   

    if(not hasattr(player2,"prediction_score")):
        player2.prediction_score = {
            "repeat": 0,
            "reaction": 0,
            "cycle": 0,
            "freq_short_term": 0,
            "freq": 0
        }
    
    alpha = 0.2 
    if(prev_play):
        for s in player2.prediction_score:
            cons = consequence(prev_play, player2.previous_predictions[s])
            player2.prediction_score[s] = player2.prediction_score[s]*(1-alpha) + alpha*cons
            
    
    
    d1 = detect_repeat(opponent_history)
    d2 = detect_cycle(opponent_history)
    d3 = detect_reaction(player2.my_history, opponent_history)
    d4 = detect_freq(opponent_history)
    d5 = detect_freq_short_term(opponent_history)

    counter = {"R":"P","P":"S","S":"R"}

    if(d1["repeated_move"]):
        player2.previous_predictions["repeat"] = d1["repeated_move"]

    if(d2):
        cycle = d2[0]
        preds = []
        n = len(cycle)
        for i, c in enumerate(cycle):
            if (c == prev_play):
                preds.append(cycle[(i + 1) % n])
        #if cycle = RPSR and prev = R so preds = [R,P]

        if(preds):
            player2.previous_predictions["cycle"] = "".join(preds)

    if(isinstance(d3, dict)):
        my_last_move = player2.my_history[-1]
        player2.previous_predictions["reaction"] = predict_reaction_move(d3,my_last_move)
        
    if(d4["frequent_move"]):
        player2.previous_predictions["freq"] = "".join(d4["frequent_move"])
    
    if(d5["frequent_move_short_term"]):
        player2.previous_predictions["freq_short_term"] = "".join(d5["frequent_move_short_term"])
    
    total_score = sum(max(player2.prediction_score[s], 0) for s in player2.prediction_score)
    move_weights = {}
    if total_score > 0:
        for s, score in player2.prediction_score.items():
            pred = player2.previous_predictions[s]
            if pred:
                weight = max(score,0)/total_score
                for m in pred:
                    move_weights[m] = move_weights.get(m, 0) + weight
    else:
        for m in ["R","P","S"]:
            move_weights[m] = 1/3

    total = sum(move_weights.values())
    if (total == 0):
        move_weights = {"R": 1/3, "P": 1/3, "S": 1/3}
        total = 1
    for m in move_weights:
        move_weights[m] /= total

    moves = list(move_weights.keys())
    weights = [w**2 for w in move_weights.values()]  
    opp = choices(moves, weights=weights, k=1)[0]
    
    my_move = counter[opp]
    player2.my_history.append(my_move)
    return my_move

