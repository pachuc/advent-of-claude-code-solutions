from solution import find_bathroom_code

# Define the diamond-shaped keypad
keypad = {
    (0, 2): '1',
    (1, 1): '2', (1, 2): '3', (1, 3): '4',
    (2, 0): '5', (2, 1): '6', (2, 2): '7', (2, 3): '8', (2, 4): '9',
    (3, 1): 'A', (3, 2): 'B', (3, 3): 'C',
    (4, 2): 'D'
}

# Test with example input
example_instructions = [
    "ULL",
    "RRDDD",
    "LURDL",
    "UUUUD"
]

code = find_bathroom_code(example_instructions, keypad)
print(f"Result: {code}")
print(f"Expected: 5DB3")
print(f"Test {'PASSED' if code == '5DB3' else 'FAILED'}")
