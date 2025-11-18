def consequence(prev_play,s):

    if(s is None):
        return 0
    
    if((len(s) == 1)and(prev_play == s)):
        return 2

    if(prev_play in s): 
        #there are multiple answers containg the correct one
        return (1/len(s))
    
    #1 answer and is wrong or multiple answers and all of them wrong
    return -0.5