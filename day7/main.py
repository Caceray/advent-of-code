file = "input"

def get_input():
    H = []
    with open(file, "r") as f:
        for line in f.readlines():
            hand, bid = line.strip().split(" ")
            bid = int(bid)
            H.append([hand, bid])
    return H
    
def get_label(hand, joker):
    # Count occurences for each card in hand
    arr = {}
    for card in hand:
        if not card in arr.keys():
            arr[card] = 0
        arr[card] += 1
        
    counts = {}
    X = list(arr.values())
    for i in range(2,6):
        n = X.count(i)
        if n:
            counts[i] = X.count(i)

    label = 0 # High card
    K = counts.keys()
    if 5 in K: # Five of kind
        label = 6
        
    elif 4 in K: # Four of kind
        label = 5
        
    elif 3 in K: # Three of kind
        if 2 in K: # + pair
            label = 4
        else:
            label = 3
            
    elif 2 in K: # At least one pair
        if counts[2] == 2: # Two pairs
            label = 2
        else:
            label = 1
            
    if joker and hand.count("J"): # Part 2
        if label == 0:
            label = 1
        elif label == 1:
            label = 3
        elif label == 2:
            if hand.count("J") == 1:
                label = 4
            else:
                label = 5
        elif label == 3:
            label = 5
        elif label == 4:
            label = 6
        elif label == 5:
            label = 6
        else:
            pass

    return label
    
def compare_hands(input, card_value, joker):

    encoded_hands = []
    for hand, bid in input:
        label = get_label(hand, joker)
        hand_as_values = [card_value[s] for s in hand]
        
        # Store bid value at the end of container to use it later in the multiplication
        encoded_hands.append( [label] + hand_as_values + [int(bid)])

    # Sort containers to rank them
    encoded_hands = sorted(encoded_hands)
    
    total = 0
    for i, item in enumerate(encoded_hands):
        # Rank = (i+1) / Bid = item[-1]
        total += item[-1] * (i+1)

    print(f"Total winnings = {total}")
    
def part1():
    """
    Hands are sorted according to :
        - Rule 1 : Label
        - Rule 2 : Compare values card-by-card
    This equivalent to compare arrays element-wise
    """
    
    # Normal order and values
    order = "AKQJT" + "".join([str(x) for x in range(9,1,-1)])
    card_value = {s:i for i,s in enumerate(order[::-1])}
    
    input = get_input()
    compare_hands(input, card_value, joker=False)
    
    
def part2():
    """
    Specific rules for Jack (J):
        - Rule 1 : Lower than 2
        - Rule 2 : Can be used as joker
    """
    
    # Rule 1
    order = "AKQT" + "".join([str(x) for x in range(9,1,-1)]) + "J"
    card_value = {s:i for i,s in enumerate(order[::-1])}
    
    input = get_input()
    compare_hands(input, card_value, joker=True)

if __name__== "__main__":
    import sys

    if sys.argv[1] == "1":
        part1()
    elif sys.argv[1] == "2":
        part2()
    else:
        raise NotImplementedError
