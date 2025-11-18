def detect_freq_short_term(opponent_history):

    res = {"pattern":"freq_short_term","frequent_move_short_term": None}

    if(len(opponent_history)<99):
        return res
    freq = {}

    recent_hist = opponent_history[-100:]

    for i, move in enumerate(recent_hist):
        freq[move] = freq.get(move, 0) + 1
        if (i>=50):   # last 50 moves extra weight
                freq[move] += 0.3

    max_occ = max(freq.values())
    res["frequent_move"] = [i for i in freq if freq[i] == max(max_occ,len(recent_hist)/2)]
    return res