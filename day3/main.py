import re

class Token:
    def __init__(self, value, start, stop):
        self.value = value
        self.start = start
        self.stop = stop
        
    def __str__(self):
        # For debug
        return f"Token [{self.value}] found at position [{self.start}]"
        
    def is_connected_to_tokens(self, tokens):
        result = False
        for token in tokens:
            if token.start > self.stop:
                # No need to continue scan as next symbols are further than current one
                break
            elif token.stop < self.start:
                # Symbol and number are disjoint
                continue
            else:
                # Tokens are necessarily connected
                result = True
                break

        return result
        
    def get_connections(self, tokens):
        result = []
        for token in tokens:
            if token.start > self.stop:
                # No need to continue scan as next symbols are further than current one
                break
            elif token.stop < self.start:
                # Symbol and number are disjoint
                continue
            else:
                # Tokens are necessarily connected
                result.append( token )
        return result
        
def get_token(line, lineId, charId, mode):
    start = charId
    while True:
        charId += 1
        charValue = line[charId]
        
        if mode == "digit":
            boolTest = not charValue.isdigit()
            
        # It seems thats symbols and gears are only one char so its useless to loop but it should stop after first loop
        elif mode == "gear":
            boolTest = charValue != "*"
        elif mode == "symbol":
            boolTest = charValue == "." or charValue.isdigit()
        else:
            raise NotImplementedError
            
        if boolTest:
#            print(f"Found new token [{line[start:charId]}] starting at {start}")
            return Token(line[start:charId], start, charId), charId
    
def extract_tokens(extractGear=False):
    file = "input"

    lineId = 0
    numbers = {}
    symbols = {}
    gears = {}
    
    # Extract tokens from lines
    with open(file, "r") as f:
        for line in f.readlines():
            charId = 0
            numbers[lineId] = []
            symbols[lineId] = []
            gears[lineId] = []
            while charId < len(line)-1:
                if line[charId].isdigit():
                    # Found digit token
                    token, charId = get_token(line, lineId, charId, "digit")
                    numbers[lineId].append( token )

#                elif line[charId] == "*" and extractGear:
#                    # Found gear token
#                    token, charId = get_token(line, lineId, charId, "gear")
#                    gears[lineId].append( token )
                    
                elif line[charId] != ".":
                    # Non-digit different from .
                    token, charId = get_token(line, lineId, charId, "symbol")
                    symbols[lineId].append( token )
                    if token.value == "*":
                        gears[lineId].append( token )
                    
                else:
                    charId += 1
                
            lineId += 1
    return numbers, symbols, gears
    
def part1():
    numbers, symbols, _ = extract_tokens()
    
    N = len(numbers.keys())
    
    # Scan lines and count partNumbers
    # Store in dictionnary for part2
    partNumbers = {}
    for i in range(N):
        partNumbers[i] = []
        for number in numbers[i]:
            isPartNumber = False
            
            #Check previous line
            if i and number.is_connected_to_tokens(symbols[i-1]):
                isPartNumber = True
                
            #Check current line left and right
            if not isPartNumber and number.is_connected_to_tokens(symbols[i]):
                isPartNumber = True
            
            #Check next line
            if not isPartNumber and  i<N-1 and number.is_connected_to_tokens(symbols[i+1]):
                isPartNumber = True
              
            if isPartNumber:
                partNumbers[i].append( number )

    # Compute the result
    sum = 0
    for numbers in partNumbers.values():
        for number in numbers:
            sum += int(number.value)
        
    print(f"Sum of part numbers = {sum}")
    
    # Return output for part2
    return partNumbers
    
def part2():
    # Use output of part1 as we need to know what are partNumbers
    partNumbers = part1()
    _, _, gears = extract_tokens(extractGear=True)

    N = len(partNumbers.keys())

    # Scan lines and count gears
    validGears = []
    for i in range(N):
#        print(f"Possible gears in line [{i}] = [{len(gears[i])}]")
        for gear in gears[i]:
            connectionsCount = []
            
            #Check previous line
            if i:
                connectionsCount += gear.get_connections(partNumbers[i-1])
                
            #Check current line left and right
            connectionsCount += gear.get_connections(partNumbers[i])
            
            #Check next line
            if i<N-1:
                connectionsCount += gear.get_connections(partNumbers[i+1])
              
            if len(connectionsCount) == 2:
                validGears.append( connectionsCount )
                
    # Compute the result
    sum = 0
    for gear in validGears:
        x, y = [int(z.value) for z in gear]
        sum += x * y
        
    print(f"Sum of gear ratios = {sum}")
    
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "1":
        part1()
    elif sys.argv[1] == "2":
        part2()
    else:
        raise NotImplementedError
