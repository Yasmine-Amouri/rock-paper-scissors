def detect_freq(opponent_history):

    res = {"pattern":"freq","frequent_move": None}

    if(len(opponent_history)==0):
        return res
    freq = {}

    for i in opponent_history:
        freq[i] = freq.get(i,0)+1

    max_occ = max(freq.values())
    res["frequent_move"] = [i for i in freq if freq[i] == max(max_occ,len(opponent_history)/2)]
    return res