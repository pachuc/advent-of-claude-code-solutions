from solution import get_pattern

# Test pattern generation with a known state
# State has plants at pots 0, 2, 4
state = {0, 2, 4}

# Test various pot positions
test_cases = [
    (-2, "....#"),  # checks pots [-4,-3,-2,-1,0]
    (-1, "...#."),  # checks pots [-3,-2,-1,0,1]
    (0, "..#.#"),   # checks pots [-2,-1,0,1,2]
    (1, ".#.#."),   # checks pots [-1,0,1,2,3]
    (2, "#.#.#"),   # checks pots [0,1,2,3,4]
    (5, ".#..."),   # checks pots [3,4,5,6,7]
]

print("Testing pattern generation:")
all_passed = True
for pot, expected in test_cases:
    result = get_pattern(pot, state)
    status = "✓" if result == expected else "✗"
    if result != expected:
        all_passed = False
    print(f"{status} pot {pot:2d}: got '{result}', expected '{expected}'")

print(f"\nAll tests {'PASSED' if all_passed else 'FAILED'}")
