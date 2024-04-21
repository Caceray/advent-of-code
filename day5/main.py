import re

def load_input():
    file = "input"
    
    # Extract blocs from input
    pattern = r"(.*?):(.*?)(?=[a-z]|\Z)"
    
    with open(file, "r") as f:
        content = "\n".join(f.readlines())

    blocs = re.findall(pattern, content, flags=re.DOTALL)
    result = {}
    
    seeds, rules = None, []
    
    # For each bloc, get the name (key) and the content
    for bloc in blocs:
        key = bloc[0]
        values = []
        for line in bloc[1].split("\n"):
            if not line.strip():
                continue
            values.append([int(x) for x in line.split()])
        
        if seeds:
            rules.append(values)
        else:
            seeds = values[0]

    return seeds, rules

def get_destination(x, rule):
    offset = rule[1] - rule[0]
    return x - offset
        
def find_location(seed, rules):
    # Map a seed (source) to a destination based on rules
    dest = None
    for rule in rules:
        dest_start, src_start, rng = rule
        if src_start <= seed < src_start + rng:
            dest = get_destination(seed, rule)
            break
    
    # If not mapped, dest = src
    if dest is None:
        dest = seed
        
    return dest
    
def part1():
    seeds, rules = load_input()
    
    locations = []
    for seed in seeds:
        x = seed
        # Loop over the mappings until location
        for rule in rules:
            x = find_location(x, rule)
        locations.append( x )
        
    location_number = sorted(locations)[0]
    print(f"Lowest location number = {location_number}")
    
def part2():
    """
    In this part, there are too many seeds to use brute force (>2bns in my input)
    in order to determine lowest number location.
    
    Each seed is provided with a range number.
    
    """
    encoded_seeds, rules = load_input()
        
    def split_range(rng, rules):
        """
        - The whole range (A,B) is mapped in the current rule (C,D)
        Case 0 : C <= A < B <= D
            All numbers betweeen [A,B] will be mapped by current rule
            
        - Only part of the range (A,B) is mapped in the current rule (C,D)
        Case 1 : A < C < D < B
            All numbers betweeen [C,D] will be mapped by current rule
            Two subsets ([A,C],[D,B]) still need to be reviewed
        Case 2 : A < C
            All numbers between [C,B] are mapped by current rule
            Subset [A,C] still need to be reviewed
        Case 3 : D < B
            All numbers between [A,C] are mapped by current rule
            Subset [C,D] still need to be reviewed
        """
        
        start, end = rng
        output = []
        for rule in rules:
            dest, rule_start, rule_range = rule
            rule_end = rule_start + rule_range - 1
            
            # Disjoint ranges, the rule does not apply
            if end < rule_start or start > rule_end:
                continue
                
            # Case 0
            if rule_start <= start < end <= rule_end:
                output.append( [get_destination(start, rule), get_destination(end, rule)] )
                break
                
            else:
                # Case 1
                if start < rule_start < rule_end < end:
                    output.append( [get_destination(rule_start, rule), get_destination(rule_end, rule)] )
                    p1 = split_range([start, rule_start-1], rules)
                    p2 = split_range([rule_start + rule_range, end], rules)
                    output += p1 + p2
                    break

                # Case 2
                elif start < rule_start:
                    assert(end<=rule_end)
                    output.append( [get_destination(rule_start, rule), get_destination(end, rule)] )
                    end = rule_start - 1
                    
                # Case 3
                elif rule_end < end:
                    assert(rule_start<=start)
                    output.append( [get_destination(start, rule), get_destination(rule_end, rule)] )
                    start = rule_end + 1
                    
                else:
                    raise Exception
    
        if not output:
            output.append( [start, end] )
            
        return output
        
    lowest_destinations = []
    for i in range(len(encoded_seeds)//2):
        seed_start, seed_rng = encoded_seeds[2*i:2*i+2]
        ranges = [[seed_start, seed_start + seed_rng - 1]]

        for rule in rules:
            new_ranges = []
            for rng in ranges:
                new_ranges += split_range(rng, rule)
            ranges = new_ranges

        # rngs contains an array of destinations ranges reachable from any seed in [seed_start,seed_start+seed_rng[
        # find lowest destination over the ranges and add it to lowest_destinations
        X = sorted([rng[0] for rng in ranges])
        lowest_destinations.append( X[0] )

    lowest_location_number = sorted(lowest_destinations)[0]
    print(f"Lowest location number = {lowest_location_number}")
    
if __name__== "__main__":
    import sys

    if sys.argv[1] == "1":
        part1()
    elif sys.argv[1] == "2":
        part2()
    else:
        raise NotImplementedError
