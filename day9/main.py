file = "input"

def reconstruct(line, mode):
    if mode:
        key, sign = -1, 1
    else:
        key, sign = 0, -1
        
    # Step 1 : Get info until only zeros
    current = [int(x) for x in line.split()]
    layers = [current]
    while True:
        next = [y-x for x,y in zip(current[:-1],current[1:])]
        layers.append( next )
        if set(next) == {0}:
            break
        else:
            current = next
            
    # Step 2 : Extrapolate
    layers = layers[::-1]
    placeholder = layers[0][key]

    for layer in layers[1:]:
        placeholder = layer[key] + placeholder * sign

    return placeholder
    
def part1():
    total = 0
    with open(file, "r") as f:
        for line in f.readlines():
            total += reconstruct(line, True)
    print(f"The puzzle answer is {total}")
    
def part2():
    total = 0
    with open(file, "r") as f:
        for line in f.readlines():
            total += reconstruct(line, False)
    print(f"The puzzle answer is {total}")

if __name__== "__main__":
    import sys

    if sys.argv[1] == "1":
        part1()
    elif sys.argv[1] == "2":
        part2()
    else:
        raise NotImplementedError
