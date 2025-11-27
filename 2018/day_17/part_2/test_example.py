from solution import solve

# Example from the problem description
example_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=10..13
x=506, y=1..2
x=498, y=13..13
y=13, x=498..504"""

result = solve(example_input)
print(f"Example result: {result}")
print(f"Expected: 29")
assert result == 29, f"Expected 29, got {result}"
print("Example test PASSED!")
