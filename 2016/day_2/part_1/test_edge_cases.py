from solution import find_bathroom_code

# Test 1: Boundary Testing - All Edges
print("Test 1: Boundary Testing")
test1 = ["UL", "U", "UR", "R", "DR", "D", "DL", "L"]
result1 = find_bathroom_code(test1)
print(f"Result: {result1}")
print(f"Expected: 11236987")
print(f"Match: {result1 == '11236987'}")
print()

# Test 2: No Movement and Empty Line Handling
print("Test 2: No Movement")
test2 = ["UDLR", "RLDU"]
result2 = find_bathroom_code(test2)
print(f"Result: {result2}")
print(f"Expected: 55")
print(f"Match: {result2 == '55'}")
print()

# Test 3: All Invalid Moves
print("Test 3: All Invalid Moves")
test3 = ["UUUUUUUUU", "LLLLLLLLL"]
result3 = find_bathroom_code(test3)
print(f"Result: {result3}")
print(f"Expected: 21")
print(f"Match: {result3 == '21'}")
print()

# Test 4: Single Direction Sequences
print("Test 4: Single Direction Sequences")
test4 = ["UUU", "DDD", "LLL", "RRR"]
result4 = find_bathroom_code(test4)
print(f"Result: {result4}")
print(f"Expected: 2879")
print(f"Match: {result4 == '2879'}")
print()

# Test 5: Manual trace of first instruction line from actual input
print("Test 5: Manual trace of first few moves from actual input")
from solution import move, get_button_at_position

row, col = 1, 1  # Start at 5
print(f"Start: button {get_button_at_position(row, col)} at ({row},{col})")

# First few characters: LURLLLL
row, col = move(row, col, 'L')
print(f"After L: button {get_button_at_position(row, col)} at ({row},{col})")

row, col = move(row, col, 'U')
print(f"After U: button {get_button_at_position(row, col)} at ({row},{col})")

row, col = move(row, col, 'R')
print(f"After R: button {get_button_at_position(row, col)} at ({row},{col})")

row, col = move(row, col, 'L')
print(f"After L: button {get_button_at_position(row, col)} at ({row},{col})")

row, col = move(row, col, 'L')
print(f"After L: button {get_button_at_position(row, col)} at ({row},{col})")

row, col = move(row, col, 'L')
print(f"After L: button {get_button_at_position(row, col)} at ({row},{col})")

row, col = move(row, col, 'L')
print(f"After L: button {get_button_at_position(row, col)} at ({row},{col})")
