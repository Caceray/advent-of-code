"""
Let's talk about physics...
H = holding button time, is equivalent to speed (1 ms = 1mm/ms)
T = race duration
D = (speed of the boat) * (remaining time) = H * (T-H)
The condition to win is beating the current record R:
    H * (T-H) > R
Let's solve the second degree equation:
    -H**2 + HT - R = 0 , Delta = T**2 - 4R
A (realistic) solution exists if Delta >= 0 <=> T**2 >= 4 * R
Solutions :
    H1 = .5 * ( T - 2*sqrt(Delta) )
    H2 = .5 * ( T + 2*sqrt(Delta) )
You have to hold button for a duration in the range ]H1,H2[, so the solution of
this exercise is counting the integers in this range.
"""

def count_ways_to_wins(inputs):
    result = 1
    for T, R in inputs:
        if T**2 < 4*R:
            # There is no way to win this race...
            continue
        else:
            root_Delta = (T**2 - 4*R) ** .5
            H1 = .5 * ( T - root_Delta )
            H2 = .5 * ( T + root_Delta )

            # Count only integers in the range ]H1,H2[
            H1 = int(H1) + 1
            if(H2 == int(H2)):
                H2 = int(H2) - 1
            else:
                H2 = int(H2)

            result *= H2 - H1 + 1

    print(f"Number of ways to beat record = {result}")

if __name__ == "__main__":
    import sys

    if sys.argv[1] == "1":
        inputs = [(53, 313),
                  (89, 1090),
                  (76, 1214),
                  (98, 1201)]
        count_ways_to_wins(inputs)
    elif sys.argv[1] == "2":
        inputs = [(53897698, 313109012141201)]
        count_ways_to_wins(inputs)
    else:
        raise NotImplementedError
