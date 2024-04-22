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
    pass

if __name__== "__main__":
    import sys

    if sys.argv[1] == "1":
        part1()
    elif sys.argv[1] == "2":
        part2()
    else:
        raise NotImplementedError
