def parse_input(filename):
    """Parse the input file and return a list of integers."""
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]


def solve(filename):
    """Solve the jump instruction maze problem."""
    # Step 1: Parse input
    instructions = parse_input(filename)

    # Step 2: Initialize state
    position = 0
    steps = 0

    # Step 3: Main simulation loop
    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    # Step 4: Return result
    return steps


def run_all_tests():
    """Run all test cases to verify the solution."""
    print("Running Jump Instruction Maze Tests...")
    print("=" * 50)

    # Test 1: Example from problem statement
    def test_example():
        instructions = [0, 3, 0, 1, -3]
        position = 0
        steps = 0

        while 0 <= position < len(instructions):
            offset = instructions[position]
            instructions[position] += 1
            position += offset
            steps += 1

        assert steps == 5, f"Expected 5 steps, got {steps}"
        print("✓ Example test passed")

    # Test 2: Immediate exit
    def test_immediate_exit():
        instructions = [5]
        position = 0
        steps = 0

        while 0 <= position < len(instructions):
            offset = instructions[position]
            instructions[position] += 1
            position += offset
            steps += 1

        assert steps == 1, f"Expected 1 step, got {steps}"
        print("✓ Immediate exit test passed")

    # Test 3: Backward exit
    def test_backward_exit():
        instructions = [-1]
        position = 0
        steps = 0

        while 0 <= position < len(instructions):
            offset = instructions[position]
            instructions[position] += 1
            position += offset
            steps += 1

        assert steps == 1, f"Expected 1 step, got {steps}"
        print("✓ Backward exit test passed")

    # Test 4: Zero offset
    def test_zero_offset():
        instructions = [0]
        position = 0
        steps = 0

        while 0 <= position < len(instructions):
            offset = instructions[position]
            instructions[position] += 1
            position += offset
            steps += 1

        assert steps == 2, f"Expected 2 steps, got {steps}"
        print("✓ Zero offset test passed")

    # Test 5: Multiple zeros
    def test_multiple_zeros():
        instructions = [0, 0, 0]
        position = 0
        steps = 0

        while 0 <= position < len(instructions):
            offset = instructions[position]
            instructions[position] += 1
            position += offset
            steps += 1

        assert steps == 6, f"Expected 6 steps, got {steps}"
        print("✓ Multiple zeros test passed")

    # Test 6: Large forward jump
    def test_large_forward_jump():
        instructions = [100, 1, 1]
        position = 0
        steps = 0

        while 0 <= position < len(instructions):
            offset = instructions[position]
            instructions[position] += 1
            position += offset
            steps += 1

        assert steps == 1, f"Expected 1 step, got {steps}"
        print("✓ Large forward jump test passed")

    # Test 7: Modification order
    def test_modification_order():
        instructions = [1, 1]
        position = 0
        steps = 0

        while 0 <= position < len(instructions):
            offset = instructions[position]
            instructions[position] += 1
            position += offset
            steps += 1

        assert steps == 2, f"Expected 2 steps, got {steps}"
        print("✓ Modification order test passed")

    # Test 8: Oscillation pattern
    def test_oscillation_pattern():
        instructions = [2, -1, 0]
        position = 0
        steps = 0

        while 0 <= position < len(instructions):
            offset = instructions[position]
            instructions[position] += 1
            position += offset
            steps += 1

        assert steps == 3, f"Expected 3 steps, got {steps}"
        print("✓ Oscillation pattern test passed")

    # Test 9: Modification persistence
    def test_modification_persistence():
        instructions = [0, 1, 0]
        position = 0
        steps = 0

        while 0 <= position < len(instructions):
            offset = instructions[position]
            instructions[position] += 1
            position += offset
            steps += 1

        assert instructions != [0, 1, 0], "List should be modified"
        assert steps == 5, f"Expected 5 steps, got {steps}"
        print("✓ Modification persistence test passed")

    # Run all unit tests
    test_example()
    test_immediate_exit()
    test_backward_exit()
    test_zero_offset()
    test_multiple_zeros()
    test_large_forward_jump()
    test_modification_order()
    test_oscillation_pattern()
    test_modification_persistence()

    print("=" * 50)
    print("All unit tests passed!")


if __name__ == "__main__":
    # Run all tests first
    run_all_tests()

    # Solve the actual problem
    print("\nSolving the actual problem...")
    result = solve('input.md')
    print(f"Answer: {result}")
