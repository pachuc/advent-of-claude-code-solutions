from itertools import groupby

def read_input(filename):
    """Read and prepare input string"""
    with open(filename, 'r') as f:
        content = f.read().strip()

    # Basic validation
    if not content:
        raise ValueError("Input file is empty")
    if not content.isdigit():
        raise ValueError("Input must contain only digits")

    return content

def look_and_say(s):
    """Apply one look-and-say transformation"""
    return ''.join(str(len(list(group))) + key
                   for key, group in groupby(s))

def apply_iterations(initial_string, num_iterations):
    """Apply look-and-say transformation n times"""
    current = initial_string
    for i in range(num_iterations):
        current = look_and_say(current)
    return current

def main():
    """Main execution function"""
    input_string = read_input('input.md')

    # Apply 40 iterations
    num_iterations = 40

    final_string = apply_iterations(input_string, num_iterations)
    result_length = len(final_string)

    # Output the result
    print(result_length)

    return result_length

if __name__ == "__main__":
    main()
