from solution import find_bathroom_code

# Test with the example from the problem
test_input = [
    "ULL",
    "RRDDD",
    "LURDL",
    "UUUUD"
]

result = find_bathroom_code(test_input)
print(f"Example test result: {result}")
print(f"Expected: 1985")
print(f"Match: {result == '1985'}")
