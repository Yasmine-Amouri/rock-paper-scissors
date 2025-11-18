def opponent_strategy(c,d):

    most_used_opponent_move = max(d, key = d.get)
 
    if(most_used_opponent_move == c):
        return "mirror"
    
    cycle = "PSR"
    p = cycle.index(c)
    counter_move = cycle[(p+1)%3]

    #the opponent thinks that I'm gonna repeat my previous_move
    if(counter_move == most_used_opponent_move):
        return "counter"
    
    return "anti-repeat"

    
    
def detect_reaction(my_history, opponent_history):

    if(len(my_history) <= 12):
        return False
    
    next_move = {
        "R": {"R":0, "S":0, "P":0},
        "S": {"R":0, "S":0, "P":0},
        "P": {"R":0, "S":0, "P":0}
    }

    limit = min(len(my_history)-1, len(opponent_history)-1)

    for i in range(limit):
        next_move[my_history[i]][opponent_history[i+1]] += 1
    
    res = {"R":"random","S":"random","P":"random"}

    for d in next_move:
        s = sum(next_move[d].values())
        if(s==0):
            res[d] = "no_data" #move not used by me at all or used once in the end
            continue
        prob = {k: v/s for k, v in next_move[d].items()}
        if (max(prob.values()) - min(prob.values()) >= 0.08): #not random 
            res[d] = opponent_strategy(d,next_move[d])

    return res

def predict_reaction_move(d,move):

    if(move == "R"):
        if(d["R"] == "mirror"):
            return "R"
        if(d["R"] == "counter"):
            return "P"
        if(d["R"] == "anti-repeat"):
            return "S"
    
    if(move == "S"):
        if(d["S"] == "mirror"):
            return "S"
        if(d["S"] == "counter"):
            return "R"
        if(d["S"] == "anti-repeat"):
            return "P"
    
    if(move == "P"):
        if(d["P"] == "mirror"):
            return "P"
        if(d["P"] == "counter"):
            return "S"
        if(d["P"] == "anti-repeat"):
            return "R"
        
    return None