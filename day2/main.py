import re

file = "input"

pattern1 = "Game ([\d]+): (.*)"
pattern2 = "([\d]+ [\w]+)"

def part1():
    # Do not exceed limits
    
    limits = {"red":12, "green":13, "blue":14}
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            # Isolate the list of games as string
            game_id, subset = re.search(pattern1, line).groups()

            # Split the string to list object of games
            batches = subset.split(";")
            
            # Scan games and determine if batch is valid
            valid_game = True
            for batch in batches:
                batch_contents = re.findall(pattern2, batch)
                
                for content in batch_contents:
                    quantity, color = content.split(" ")

                    # Check if batch is valid
                    if int(quantity) > limits[color]:
                        valid_game = False
                        break
                
                # If current game is not valid, the batch is not valid, stop
                if not valid_game:
                    break
            
            # Only increase all games were valid
            if valid_game:
                sum += int(game_id)

    print(f"Result = {sum}")
    
def part2():
    # Determine minimum of each color for each game
    
    sum = 0
    with open(file, "r") as f:
        for line in f.readlines():
            # Isolate the list of games as string
            game_id, subset = re.search(pattern1, line).groups()

            # Split the string to list object of games
            batches = subset.split(";")
            
            # Scan games and collect minimal values for each color
            minimal_values = {"red":0, "blue":0, "green":0}
            for batch in batches:
                batch_contents = re.findall(pattern2, batch)
                
                for content in batch_contents:
                    quantity, color = content.split(" ")
                    
                    quantity = int(quantity)
                    if quantity > minimal_values[color]:
                        minimal_values[color] = quantity
            
            P = 1
            for value in minimal_values.values():
                P *= value
            sum += P

    print(f"Result = {sum}")
    
if __name__ == "__main__":
    import sys
    
    if sys.argv[1] == "1":
        part1()
    else:
        part2()
    
