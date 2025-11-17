def solve():
    # Step 1: Read input
    with open('input.md', 'r') as f:
        directions = f.read().strip()

    # Step 2: Initialize tracking variables
    visited = set()
    x, y = 0, 0
    visited.add((x, y))  # Starting position

    # Step 3: Direction mapping
    direction_map = {
        '^': (0, 1),   # North
        'v': (0, -1),  # South
        '>': (1, 0),   # East
        '<': (-1, 0)   # West
    }

    # Step 4: Process each direction
    for direction in directions:
        dx, dy = direction_map[direction]
        x += dx
        y += dy
        visited.add((x, y))

    # Step 5: Output result
    print(len(visited))
    return len(visited)

def run_test(input_str, expected, test_name):
    """Simple test function to validate solution logic"""
    visited = set()
    x, y = 0, 0
    visited.add((x, y))

    direction_map = {'^': (0, 1), 'v': (0, -1), '>': (1, 0), '<': (-1, 0)}

    for direction in input_str:
        dx, dy = direction_map[direction]
        x += dx
        y += dy
        visited.add((x, y))

    result = len(visited)
    status = "PASS" if result == expected else "FAIL"
    print(f"{status}: {test_name} - Expected {expected}, Got {result}")
    return result == expected

if __name__ == "__main__":
    # First run the test suite
    print("Running test suite...")
    print("-" * 50)

    # Example test cases from problem statement
    run_test(">", 2, "Single move east")
    run_test("^>v<", 4, "Square path")
    run_test("^v^v^v^v^v", 2, "Back and forth")

    # Edge cases
    run_test("", 1, "Empty input")
    run_test("^", 2, "Single move north")
    run_test("v", 2, "Single move south")
    run_test("<", 2, "Single move west")
    run_test(">>>>>>>>", 9, "Straight line east")
    run_test("<v", 3, "Negative coordinates")

    print("-" * 50)
    print("\nRunning solution on actual input...")
    print("-" * 50)

    # Run the actual solution
    solve()
