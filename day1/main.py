import re

file = "input"

def part1():
    with open(file, "r") as f:
        total = 0
        for line in f.readlines():
            # Get first and last digit as string
            first_digit = re.search("\d", line).group()
            last_digit = re.search("\d", line[::-1]).group()
            
            # Combine digits and get value as integer
            calibration_value = int(first_digit+last_digit)

            # Update value
            total += calibration_value
        
        print(f"Part 1 : Sum of calibrations = {total}")

def part2():
    digit_string_to_int = {"zero":"0",
                           "one":"1",
                           "two":"2",
                           "three":"3",
                           "four":"4",
                           "five":"5",
                           "six":"6",
                           "seven":"7",
                           "eight":"8",
                           "nine":"9"}

    # Create lists of digits written using letters
    digits_as_string = [x for x in digit_string_to_int.keys()]
    digits_as_string_reversed = [x[::-1] for x in digit_string_to_int.keys()]

    # Create pattern for regex
    pattern_direct = "|" .join(["\d"]+digits_as_string)
    pattern_reverse = "|" .join(["\d"]+digits_as_string_reversed)

    def convert_to_digit(token):
        if token.isdigit():
            # Already a digit
            return token
        else:
            # Digit it written using letter
            if not token in digit_string_to_int.keys():
                # For the last digit (for example orez instead of zero)
                token = token[::-1]
                
            return digit_string_to_int[token]
            
    with open(file, "r") as f:
        total = 0
        for line in f.readlines():
            # Get first and last digit as string
            first_digit = re.search(pattern_direct, line).group()
            last_digit = re.search(pattern_reverse, line[::-1]).group()
            
            # Convert to digit if necessary
            first_digit = convert_to_digit(first_digit)
            last_digit = convert_to_digit(last_digit)
            
            # Combine digits and get value as integer
            calibration_value = int(first_digit+last_digit)

            # Update value
            total += calibration_value
        
        print(f"Part 2 : Sum of calibrations = {total}")
        
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "1":
        part1()
    elif sys.argv[1] == "2":
        part2()
    else:
        raise NotImplementedError
