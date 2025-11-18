from random import choice, choices
from strategies.repeat import detect_repeat
from strategies.cycle import detect_cycle
from strategies.reaction import detect_reaction, predict_reaction_move
from strategies.frequency import detect_freq
from strategies.frequency_short_term import detect_freq_short_term
from RPS.consequences import consequence

def player3(prev_play, opponent_history = []):

    if(prev_play):
        opponent_history.append(prev_play)
    
    #history for my moves
    if (not hasattr(player3,"my_history")):
        player3.my_history = []
    
    if(not hasattr(player3,"previous_predictions")):
        player3.previous_predictions = {
            "repeat": None,
            "reaction": None,
            "cycle": None,
            "freq_short_term": None,
            "freq": None
        }   

    if(not hasattr(player3,"prediction_score")):
        player3.prediction_score = {
            "repeat": 0,
            "reaction": 0,
            "cycle": 0,
            "freq_short_term": 0,
            "freq": 0
        }

    
    if (not hasattr(player3, "score_drop")):
        player3.score_drop = 0

    if (not hasattr(player3, "prev_best_score")):
        player3.prev_best_score = 0

    if(prev_play):
        for k in player3.prediction_score:
            player3.prediction_score[k] += consequence(prev_play, player3.previous_predictions[k])

    d1 = detect_repeat(opponent_history)
    d2 = detect_cycle(opponent_history)
    d3 = detect_reaction(player3.my_history, opponent_history)
    d4 = detect_freq(opponent_history)
    d5 = detect_freq_short_term(opponent_history)

    counter = {"R":"P","P":"S","S":"R"}

    if (d1["repeated_move"]):
        player3.previous_predictions["repeat"] = d1["repeated_move"] 

    if (d2):
        cycle = d2[0]
        preds = []
        n = len(cycle)
        for i, c in enumerate(cycle):
            if (c == prev_play):
                preds.append(cycle[(i + 1) % n])
        
        if(preds):
            player3.previous_predictions["cycle"] = "".join(preds)

    if (isinstance(d3, dict)):
        player3.previous_predictions["reaction"] = predict_reaction_move(d3, player3.my_history[-1])

    if (d4["frequent_move"]):
        player3.previous_predictions["freq"] = "".join(d4["frequent_move"]) 
    
    if (d5["frequent_move_short_term"]):
        player3.previous_predictions["freq_short_term"] = "".join(d5["frequent_move_short_term"]) 
   
    best_score = max(player3.prediction_score.values())
    if (best_score < player3.prev_best_score):
        player3.score_drop += 1
    else:
        player3.score_drop = max(player3.score_drop - 1, 0)
    player3.prev_best_score = best_score

    if (player3.score_drop > 2):
        my_move = choice(["R","P","S"])
        player3.my_history.append(my_move)
        return my_move

    best_strats = [k for k,v in player3.prediction_score.items() if v == best_score]
    predicted_moves = []
    for s in best_strats:
        pred = player3.previous_predictions[s]
        if (pred): 
            predicted_moves.extend(list(pred))

    if (not predicted_moves):
        my_move = choice(["R","P","S"])
    elif (len(predicted_moves) == 1):
        my_move = counter[predicted_moves[0]]
    else:
        my_move = counter[choice(predicted_moves)]

    player3.my_history.append(my_move)
    return my_move