def parse_input(filename):
    """Parse the input file and return a list of integers."""
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]


def simulate(instructions):
    """Run Part 2 simulation on a list of instructions (modifies in place)."""
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]

        # PART 2 CHANGE: Conditional modification based on offset value
        if offset >= 3:
            instructions[position] -= 1
        else:
            instructions[position] += 1

        position += offset
        steps += 1

    return steps


def simulate_part1(instructions):
    """Run Part 1 simulation for regression testing."""
    position = 0
    steps = 0

    while 0 <= position < len(instructions):
        offset = instructions[position]
        instructions[position] += 1
        position += offset
        steps += 1

    return steps


def solve(filename):
    """Solve the jump instruction maze with conditional offset modification."""
    instructions = parse_input(filename)
    return simulate(instructions)


def run_all_tests():
    """Run all test cases to verify the solution."""
    print("Running Part 2 Jump Instruction Maze Tests...")
    print("=" * 50)

    # Test 1: Part 2 Example from problem statement
    def test_part2_example():
        instructions = [0, 3, 0, 1, -3]
        result = simulate(instructions[:])  # Use copy to preserve original
        assert result == 10, f"Expected 10 steps, got {result}"
        print("✓ Part 2 example test passed (10 steps)")

    # Test 2: Part 1 Regression - verify Part 1 logic still works
    def test_part1_regression():
        instructions = [0, 3, 0, 1, -3]
        result = simulate_part1(instructions[:])
        assert result == 5, f"Expected 5 steps, got {result}"
        print("✓ Part 1 regression test passed (5 steps)")

    # Test 3: Boundary condition - offset exactly 3 (should decrement)
    def test_boundary_offset_3():
        instructions = [3]
        result = simulate(instructions[:])
        assert result == 1, f"Expected 1 step, got {result}"
        print("✓ Boundary test (offset = 3) passed")

    # Test 4: Boundary condition - offset exactly 2 (should increment)
    def test_boundary_offset_2():
        instructions = [2]
        result = simulate(instructions[:])
        assert result == 1, f"Expected 1 step, got {result}"
        print("✓ Boundary test (offset = 2) passed")

    # Test 5: Zero offset (should increment)
    def test_zero_offset():
        instructions = [0]
        result = simulate(instructions[:])
        assert result == 2, f"Expected 2 steps, got {result}"
        print("✓ Zero offset test passed")

    # Test 6: Negative offset (should increment)
    def test_negative_offset():
        instructions = [-1]
        result = simulate(instructions[:])
        assert result == 1, f"Expected 1 step, got {result}"
        print("✓ Negative offset test passed")

    # Test 7: Large offset (should decrement)
    def test_large_offset():
        instructions = [100]
        result = simulate(instructions[:])
        assert result == 1, f"Expected 1 step, got {result}"
        print("✓ Large offset test passed")

    # Test 8: Multiple zeros
    def test_multiple_zeros():
        instructions = [0, 0, 0]
        result = simulate(instructions[:])
        assert result == 6, f"Expected 6 steps, got {result}"
        print("✓ Multiple zeros test passed")

    # Test 9: Order of operations
    def test_order_of_operations():
        instructions = [1, 1]
        result = simulate(instructions[:])
        assert result == 2, f"Expected 2 steps, got {result}"
        print("✓ Order of operations test passed")

    # Test 10: Input integrity check
    def test_input_integrity():
        instructions = parse_input('input.md')
        assert len(instructions) == 1037, f"Expected 1037 instructions, got {len(instructions)}"
        assert instructions[0] == 1, f"Expected first value 1, got {instructions[0]}"
        assert instructions[-1] == -572, f"Expected last value -572, got {instructions[-1]}"
        print("✓ Input integrity verified (1037 values)")

    # Run all unit tests
    test_part2_example()
    test_part1_regression()
    test_boundary_offset_3()
    test_boundary_offset_2()
    test_zero_offset()
    test_negative_offset()
    test_large_offset()
    test_multiple_zeros()
    test_order_of_operations()
    test_input_integrity()

    print("=" * 50)
    print("All unit tests passed!")


if __name__ == "__main__":
    # Run all tests first
    run_all_tests()

    # Solve the actual problem
    print("\nSolving the actual problem...")
    result = solve('input.md')
    print(f"Answer: {result}")
