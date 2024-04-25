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
            self.connections = {"south":"east", "west":"north"}
            
        elif symbol == "|":
            self.connections = {"south":"south", "north":"north"}
    
        elif symbol == "J":
            self.connections = {"south":"west", "east":"north"}
            
        elif symbol == "F":
            self.connections = {"north":"east", "west":"south"}
        
        elif symbol == "-":
            self.connections = {"west":"west", "east":"east"}
            
        elif symbol == "7":
            self.connections = {"north":"west", "east":"south"}
        
    def get_next_direction(self, direction):
        return self.connections.get(direction, None)
        
pipes = {s:Pipe(s) for s in ["|","F","J","7","-","L","S"]}

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
        direction = pipes[symbol].get_next_direction(direction)
        
        dy, dx = dP[direction]
        y += dy
        x += dx
        count += 1

        if [y,x] == start:
            break
            
    print(f"Farthest point is {count//2} steps away")
    
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

