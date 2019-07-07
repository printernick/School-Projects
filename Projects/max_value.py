


def max_value(gifts: ((int, int)), max_weight: int) -> int:
    '''Given a list of gifts representeted by a tuple of 2-tuples,
    calculate the maximum value of gifts while staying within
    the weight limit

    @param gifts: tuple of 2-tuples: each 2 tuple is an (1) int
    representing the value of the gift and (2) the weight of
    the gift
    @param max_weight: an integer representing the maximum weight
    allowed

    @return: an integer for the maximum value possible within the
    weight limit'''

    
    if len(gifts) == 0:
        return 0
    else:
        w, v = gifts[0]
        
        if w <= max_weight:
            return max((v + max_value(gifts[1:], max_weight - w), max_value(gifts[1:], max_weight)))
        else:
            return max_value(gifts[1:], max_weight)


if __name__ == '__main__':
     pass   
    #ex1 = ((10, 70), (15, 80), (20, 140), (20, 150), (30, 200))
    #print(max_value(ex1, 50))
