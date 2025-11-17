from solution import find_basement_position


def test_examples():
    """Test provided examples"""
    # Test 1: Single character immediate basement
    result = find_basement_position(')')
    assert result == 1, f"Expected 1, got {result}"
    print(f"✓ Test 1 passed: ')' -> {result}")

    # Test 2: Multiple steps before basement
    result = find_basement_position('()())')
    assert result == 5, f"Expected 5, got {result}"
    print(f"✓ Test 2 passed: '()())' -> {result}")

    print("✓ All example tests passed\n")


def test_edge_cases():
    """Test edge cases"""
    # Test: Immediate basement after ups
    result = find_basement_position('((()))')
    assert result is None, f"Expected None (never reaches -1), got {result}"
    print(f"✓ Test 3 passed: '((()))' -> {result} (never reaches basement)")

    # Test: Alternating pattern
    result = find_basement_position('()()()())')
    assert result == 9, f"Expected 9, got {result}"
    print(f"✓ Test 4 passed: '()()()())' -> {result}")

    # Test: Multiple down immediately
    result = find_basement_position('))))')
    assert result == 1, f"Expected 1, got {result}"
    print(f"✓ Test 5 passed: '))))' -> {result}")

    # Test: Basement from floor 0
    result = find_basement_position('())')
    assert result == 3, f"Expected 3, got {result}"
    print(f"✓ Test 6 passed: '())' -> {result}")

    print("✓ All edge case tests passed\n")


def test_boundaries():
    """Test boundary conditions"""
    # Never reaching basement - only going up
    result = find_basement_position('((((')
    assert result is None, f"Expected None, got {result}"
    print(f"✓ Test 7 passed: '((((' -> {result} (never reaches basement)")

    # Balanced parentheses
    result = find_basement_position('((()))')
    assert result is None, f"Expected None, got {result}"
    print(f"✓ Test 8 passed: '((()))' -> {result} (never reaches basement)")

    print("✓ All boundary tests passed\n")


def verify_result(instructions, position):
    """Verify a result is correct"""
    if position is None:
        # Verify we never reach floor -1
        floor = 0
        for char in instructions:
            floor += 1 if char == '(' else -1
            if floor == -1:
                raise AssertionError("Found floor -1, but result was None")
        print(f"✓ Verified: Never reaches floor -1")
        return

    # At the result position, we should be at floor -1
    floor = 0
    for i, char in enumerate(instructions[:position], 1):
        if char == '(':
            floor += 1
        else:
            floor -= 1

    assert floor == -1, f"At position {position}, floor should be -1, got {floor}"

    # At position-1, we should NOT be at floor -1 (if position > 1)
    if position > 1:
        floor = 0
        for char in instructions[:position-1]:
            floor += 1 if char == '(' else -1
        assert floor != -1, f"Floor -1 reached before position {position}"

    print(f"✓ Verified: Position {position} is correct (floor = -1)")


def test_actual_input():
    """Test with actual problem input"""
    with open('input.md', 'r') as f:
        instructions = f.read().strip()

    result = find_basement_position(instructions)
    assert result is not None, "Result should not be None for actual input"
    assert isinstance(result, int), f"Result should be integer, got {type(result)}"
    assert result > 0, f"Position should be positive, got {result}"
    assert result <= len(instructions), f"Position {result} exceeds input length {len(instructions)}"

    print(f"✓ Actual input test passed: position = {result}")
    print(f"  Input length: {len(instructions)} characters")

    # Verify the result
    verify_result(instructions, result)

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Santa's Basement Entry Position Solution")
    print("=" * 60 + "\n")

    test_examples()
    test_edge_cases()
    test_boundaries()
    result = test_actual_input()

    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print(f"Final answer: {result}")
    print("=" * 60)
