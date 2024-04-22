def get_input():
    import re
    with open("input", "r") as f:
        instruction, maps = "", {}
        for i,line in enumerate(f.readlines()):
            if not i:
                # Encode instructions as 0 and 1
                instruction = line.strip()
                instruction = instruction.replace("L","0")
                instruction = instruction.replace("R","1")
                
            elif i > 1:
                # Populate mapper
                key, left, right = re.search("([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line).groups()
                assert(not key in maps.keys())
                maps[key] = [left, right]

        return instruction, maps
    
def part1():
    instruction, maps = get_input()
    
    count, N = 0, len(instruction)
    key = "AAA"
    while key != "ZZZ" :
        for i in range(N):
            key = maps[key][int(instruction[i])]
        count += 1
    print(f"Result found after {count} loops, that is {N*count} steps")

def part2():
    """
    Let M the number of loops that we must do in order to reach the goal. For k starting
    points, we want the result to be a multiple of each starting points (M_1,...,M_k),
    that is a mathematical problm known as least common multiple (LCM).
    We have to solve each N individually and implement the algorithm for LCM.
    """
    instruction, maps = get_input()
    start_nodes = [x for x in maps.keys() if x.endswith("A")]

    N = len(instruction)
    
    # Store the result of N steps starting from a given key so we don't compute twice the same path
    shortcuts = {}

    # Container for M_k results
    counts = []
    for key in start_nodes:
        count = 0
        # The condition here is a bit different than part 1
        while not key.endswith("Z") :
            count += 1
            # Check if path from starting point [key] has been computed
            if key in shortcuts.keys():
                key = shortcuts[key]
            else:
                start = key
                for i in range(N):
                    key = maps[key][int(instruction[i])]
                shortcuts[start] = key
        
        counts.append(count)
    
    # Implementation of LCM algorithm
    import math
    def lcm(a, b):
        # Euclide algorithm for LCM
        return abs(a * b) // math.gcd(a, b)
    
    res = 1
    for count in counts:
        res = lcm(res, count)
        
    # The result stands for number of loops, we multiply the result by N to get the number
    # of steps
    print(f"Result found after {res} loops, that is {res*N} steps")

if __name__== "__main__":
    import sys

    if sys.argv[1] == "1":
        part1()
    elif sys.argv[1] == "2":
        part2()
    else:
        raise NotImplementedError
