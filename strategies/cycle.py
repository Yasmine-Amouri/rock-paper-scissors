from collections import deque

def occ_cycle(cycle,size,l):
     
    window = deque(maxlen = size)
    occ = 0
    for e in l:
        window.append(e)
        if(len(window) == size):
            if(list(window) == cycle):
                occ += 1
    return occ

def not_exist(cycle,L):
    if(len(L) == 0):
        return True
    for e in L:
        if(e[0] == cycle):
            return False
    return True

def longest_consecutive_occ_cycle(cycle,size,L):

    maxi = 0
    
    i = 0

    while(i<=(len(L)-size)):
        
        if(L[i:(i+size)] == cycle):
            cpt = 1
            j = i+size

            while((j<=(len(L)-size))and(L[j:j+size] == cycle)):
                cpt += 1
                j += size

            maxi = max(maxi,cpt)

            i = j
        else:
            i += 1

    return maxi

def choose(l,hist):

    if(len(l) == 1):
        return l[0]
    max_occ = l[len(l)-1][1]
    max_consec_occ = l[len(l)-1][2]
    choices = []
    choices.append(l[len(l)-1])

    i = len(l)-2

    while((i>=0)and(l[i][1] == max_occ)and(l[i][2] == max_consec_occ)):
        choices.append(l[i])
        i -= 1
    
    if(len(choices) == 1):
        return choices[0]
    
    #we need to choose the recent cycle
    s = "".join(hist)
    maxi_pos = 0
    chosen =()

    for e in choices:
        s1 = "".join(e[0])
        i = s.rfind(s1)

        if(i>maxi_pos):
            maxi_pos = i
            chosen = e

        elif (i == maxi_pos):
        #this is used when using choose function but with cycles with different lengths
        #tie-breaker by longer cycle
            if len(e[0])>len(chosen[0]):
                chosen = e

    return chosen


def detect_cycle(opponent_history):

    if(len(opponent_history) <= 12):
        return None

    #store general occ for each cycle = n
    #store c = consecutive_occ not just (in case 2 cycles for a given l have the same n)
    #if both cycles have the same n and c we pick the most recent one

    m = []
    
    for l in range(2,6):

        checked_cycles = set() #to avoid recomputing of weak and strong cycles
        cycles_size_l = [] #to store strong cycles
        
        for i in range(len(opponent_history) - l + 1):
            cycle = opponent_history[i:i+l]
            cycle_tuple = tuple(cycle)

            if(cycle_tuple not in checked_cycles):
                checked_cycles.add(cycle_tuple)
                recent_hist = opponent_history[-400:]
                occ = occ_cycle(cycle,l,recent_hist)
                moves_used = l*occ
                if ((occ>2)and(moves_used>=(len(recent_hist)/2))):
                    consecutive_occ = longest_consecutive_occ_cycle(cycle,l,recent_hist)
                    my_tuple = (cycle,occ,consecutive_occ)
                    cycles_size_l.append(my_tuple)
        m.append(cycles_size_l)

    candidates = []

    for l in m:
        if(len(l)>0):
            l.sort(key=lambda x: (x[1], x[2]))  #sorts in ascending order first according to occ then to consec_occ
            choice = choose(l,opponent_history)
            candidates.append(choice)

    if (len(candidates)>0):
        candidates.sort(key=lambda x: (x[1], x[2])) #we pick the one with largest occ then consecutive_occ
        return choose(candidates,opponent_history)
    
    return None
