def detect_repeat(opponent_history):

    res = {"pattern": "repeat", "repeated_move": None}
    if(len(opponent_history) <= 6):
        return res
    
    cpt = 1
    for i in range(min(10,len(opponent_history)-1),-1,-1):
        if(opponent_history[i] == opponent_history[i-1]):
            cpt += 1

    if(cpt>=min(4,len(opponent_history)-1)):
        res["repeated_move"] = opponent_history[len(opponent_history)-1]
        return res
    return res