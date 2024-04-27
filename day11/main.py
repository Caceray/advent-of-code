file = "input"

def get_input():
    rows = []

    with open(file,"r") as f:
        for line in f.readlines():
            rows.append(line.strip())
    return rows
    
def expand_universe(universe):
    coordinates = []
    for i,line in enumerate(universe):
        if set(line) == {"."}:
            coordinates.append(i)
    
    return coordinates
    
def rotate_universe(universe):
    n = len(universe[0])
    new_universe = ["" for _ in range(n)]
    
    for i in range(n):
        for row in universe:
            new_universe[i] += row[i]
    return new_universe
    
def get_total_distance(universe, expansion_factor):
    # Expand / rotate / expand
    C1 = expand_universe(universe)
    universe = rotate_universe(universe)
    C2 = expand_universe(universe)

    # Find position of galaxies
    galaxies = []
    for i, line in enumerate(universe):
        for j, s in enumerate(line):
            if s == "#":
                galaxies.append([i,j])

    # Calculate distance between each pair
    N = len(galaxies)
    total = 0
    for i in range(N):
        for j in range(i+1, N):
            P1, P2 = galaxies[i], galaxies[j]
            x1, y1 = P1
            x2, y2 = P2
            
            distance = 0
            
            # Evaluate absolute distance in dimension 1
            k = 0
            if x1 < x2:
                k = len([x for x in C2 if x1<x<x2])
                distance += (x2 - x1)
            elif x1 > x2:
                k = len([x for x in C2 if x2<x<x1])
                distance += (x1 - x2)
            
            # Add expansion in dimension 1
            distance += k * (expansion_factor-1)
            
            # Evaluate absolute distance in dimension 2
            k = 0
            if y1 < y2:
                k = len([x for x in C1 if y1<x<y2])
                distance += (y2 - y1)
            elif y1 > y2:
                k = len([x for x in C1 if y2<x<y1])
                distance += (y1 - y2)
                
            # Add expansion in dimension 2
            distance += k * (expansion_factor-1)
            
            total += distance
            
    print(f"Total distance = {total}")
    
def part1():
    universe = get_input()
    expansion_factor = 2
    get_total_distance(universe, expansion_factor)
        
def part2():
    universe = get_input()
    expansion_factor = 1000000
    get_total_distance(universe, expansion_factor)

if __name__== "__main__":
    import sys

    if sys.argv[1] == "1":
        part1()
    elif sys.argv[1] == "2":
        part2()
    else:
        raise NotImplementedError
