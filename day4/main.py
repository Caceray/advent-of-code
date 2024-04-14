import re

file = "input"
pattern = "Card\s*([\d]+)\s*\:(.*?)\|(.*)"

def parse_line(line):
    """ Collect data from input file """
    x, y, z = re.search(pattern, line).groups()
    winNumbers, numbers = [set(k.split()) for k in (y,z)]
    cardId = int(x)
    return cardId, winNumbers, numbers

def part1():
    result = 0
    with open(file, "r") as f:
        for line in f.readlines():
            cardId, winNumbers, numbers = parse_line(line)
            
            I = winNumbers.intersection(numbers)
            N = len(I)
            if N:
                result += 2 ** (N-1)
    print(f"Total points = {result}")

def part2():
    result = 0
    copies = {}

    def add_first_copy(cardId):
        if not cardId in copies.keys():
            copies[cardId] = 1

    def add_copy(cardId, copyCount):
        add_first_copy(cardId)
        copies[cardId] += copyCount

    with open(file, "r") as f:
        for line in f.readlines():
            cardId, winNumbers, numbers = parse_line(line)
            
            I = winNumbers.intersection(numbers)
            N = len(I)

            add_first_copy(cardId)
            result += copies[cardId]

            for i in range(N):
                add_copy(cardId + 1 + i, copies[cardId])

    print(f"Total scratchcards = {result}")
if __name__ == "__main__":
    import sys
    
    if sys.argv[1] == "1":
        part1()
    elif sys.argv[1] == "2":
        part2()
    else:
        raise NotImplementedError
