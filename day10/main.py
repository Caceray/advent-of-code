file = "input"

# Convert string direction to delta (dP)
dP = {"north":[-1, 0],
      "east":[0, 1],
      "south":[1, 0],
      "west":[0, -1]}
              
class Pipe:
    def __init__(self, symbol):
        self.symbol = symbol
        if symbol == "L":
            self.connections = {"south": "east", "west": "north"}
                    
        elif symbol == "|":
            self.connections = {"south": "south", "north": "north"}
            
        elif symbol == "J":
            self.connections = {"south": "west", "east": "north"}
                                    
        elif symbol == "F":
            self.connections = {"north": "east", "west": "south"}
                                    
        elif symbol == "-":
            self.connections = {"west": "west", "east": "east"}
                    
        elif symbol == "7":
            self.connections = {"north": "west", "east": "south"}
            
        elif symbol == ".":
            self.connections = {}
            
    def get_next_direction(self, direction):
        return self.connections.get(direction, None)
        
pipes = {s:Pipe(s) for s in ["|","F","J","7","-","L"]}

def get_input():
    rows, start = [], []
    with open(file, "r") as f:
        for i, line in enumerate(f.readlines()):
            if not start and "S" in line :
                start = [i, line.index("S")]
            rows.append( line )
            
    return rows, start
              
def part1():
    rows, start = get_input()
    y, x = start
    positions, symbols = [[y,x]], ["S"]
    
    source = None
    
    # Find possible first move
    for direction, dp in dP.items():
        dy, dx = dp
        symbol = rows[y+dy][x+dx]
        pipe = pipes[symbol]
        next = pipe.connections.get(direction, None)
        if next:
            x += dx
            y += dy
            source = direction
            break

    # Move until returning to start position
    count = 1
    while True:
        symbol = rows[y][x]
        symbols.append( symbol )
        positions.append( [y,x] )
        direction = pipes[symbol].get_next_direction(direction)
        
        dy, dx = dP[direction]
        y += dy
        x += dx
        count += 1
        
        if [y,x] == start:
            break
            
    print(f"Farthest point is {count//2} steps away")

    return symbols, positions
    
def part2():
    """
    Mathematical approach : Jordan's theorem
    For each point, if not in the path (positions), count how many times it crosses the path
    in a given direction.
    To simplify, let the direction be an horizontal line, starting from the point itself,
    going to the right (east).
    When it "crosses" a wall, increase by 1.
    When it "crosses" a corner, we need to apply specific rule:
        - F + J : is a wall (north - east - north)
        - F + 7 : is not a wall (north - east - south)
        - L + J : is not a wall
        - L + 7 : is a wall
    Since we only consider "vertical" walls, ignore "-" here...
    """
    
    symbols, positions = part1()
  
    rows, _ = get_input()
    N, M = len(rows), len(rows[0])
    
    # List non horizontal obstacles, line by line
    obstacles = [[] for _ in range(N)]
    for s,p in zip(symbols, positions):
        obstacles[p[0]].append(p[1])

    wall_equivalent = [set(["L","7"]), set(["F","J"])]
    tiles = []
    
    for n in range(N):
        obstacles_in_line = sorted(obstacles[n])
        
        # If there is no obstacle in this line, the line does not contain any tile
        if not obstacles_in_line:
            continue
            
        # No need to scan points ouside the range as they can't be a tile
        x_start = obstacles_in_line[0]+1
        x_end = obstacles_in_line[-1]
        
        for m in range(x_start, x_end):
            if m in obstacles_in_line:
                # An element of the path cannot be a tile
                continue
                
            crosses_count = 0
            turn = None # To be used for corner specific rule
            for obstacle in obstacles_in_line:
                if obstacle <= m:
                    continue
                    
                symbol = rows[n][obstacle]

                if symbol == "|":
                    crosses_count += 1
                elif symbol == "-": # Ignore horizontal obstacles
                    continue
                else:
                    if turn:
                        if set([turn,symbol]) in wall_equivalent:
                            crosses_count += 1
                        turn = None
                    else :
                        turn = symbol

            # Jordan's theorem
            if crosses_count%2:
                tiles.append([n,m]) # Not necessary, but can be fun to store the value and print...

    print(f"There are {len(tiles)} tiles")
    
if __name__== "__main__":
    import sys

    if sys.argv[1] == "1":
        part1()
    elif sys.argv[1] == "2":
        part2()
    else:
        raise NotImplementedError

