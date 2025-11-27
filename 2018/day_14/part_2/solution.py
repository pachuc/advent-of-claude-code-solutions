def solve(target_str=None):
    """
    Find the position where target sequence first appears in the scoreboard.

    Args:
        target_str: String of digits to search for.
                   If None, reads from input.md file.

    Returns:
        Integer representing number of recipes before the pattern.
    """
    # Step 1: Parse input
    if target_str is None:
        with open('input.md', 'r') as f:
            target_str = f.read().strip()

    target = [int(d) for d in target_str]
    pattern_len = len(target)

    # Step 2: Initialize state
    scoreboard = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    # Step 3: Generate recipes with pattern detection
    iteration_count = 0
    MAX_ITERATIONS = 100_000_000

    while True:
        iteration_count += 1
        if iteration_count > MAX_ITERATIONS:
            raise RuntimeError(f"Pattern not found after {MAX_ITERATIONS} iterations")

        # 3a: Create new recipes
        score1 = scoreboard[elf1_pos]
        score2 = scoreboard[elf2_pos]
        recipe_sum = score1 + score2

        if recipe_sum >= 10:
            scoreboard.append(1)
            scoreboard.append(recipe_sum - 10)
        else:
            scoreboard.append(recipe_sum)

        # 3b: Update positions
        elf1_pos = (elf1_pos + 1 + score1) % len(scoreboard)
        elf2_pos = (elf2_pos + 1 + score2) % len(scoreboard)

        # 3c: Check for pattern
        # IMPORTANT: Each iteration can add 1 or 2 recipes, so we must check both cases
        if len(scoreboard) >= pattern_len:
            # Case 1: Pattern ends at current position (last recipe added completes it)
            if scoreboard[-pattern_len:] == target:
                return len(scoreboard) - pattern_len

            # Case 2: Pattern ends one position before current (second-to-last recipe completes it)
            # This handles when 2 recipes were added and the pattern was completed by the first one
            if len(scoreboard) > pattern_len and scoreboard[-pattern_len-1:-1] == target:
                return len(scoreboard) - pattern_len - 1


def generate_recipes(num_recipes):
    """
    Helper function: Generate exactly num_recipes and return the scoreboard.
    Useful for testing and cross-validation.

    Args:
        num_recipes: Number of recipes to generate

    Returns:
        List representing the scoreboard
    """
    scoreboard = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    while len(scoreboard) < num_recipes:
        score1 = scoreboard[elf1_pos]
        score2 = scoreboard[elf2_pos]
        recipe_sum = score1 + score2

        if recipe_sum >= 10:
            scoreboard.append(1)
            scoreboard.append(recipe_sum - 10)
        else:
            scoreboard.append(recipe_sum)

        elf1_pos = (elf1_pos + 1 + score1) % len(scoreboard)
        elf2_pos = (elf2_pos + 1 + score2) % len(scoreboard)

    return scoreboard


def test_examples():
    """Test all provided examples"""
    test_cases = [
        ("51589", 9),      # Pattern appears after 9 recipes
        ("01245", 5),      # Pattern appears after 5 recipes
        ("92510", 18),     # Pattern appears after 18 recipes
        ("59414", 2018),   # Pattern appears after 2018 recipes
    ]

    print("Testing examples:")
    all_passed = True
    for pattern, expected_pos in test_cases:
        result = solve(pattern)
        if result == expected_pos:
            print(f"✓ Test passed for pattern {pattern} (position {expected_pos})")
        else:
            print(f"✗ Test FAILED for pattern {pattern}: got {result}, expected {expected_pos}")
            all_passed = False

    return all_passed


def test_recipe_generation():
    """Verify recipe generation matches expected pattern"""
    print("\nTesting recipe generation:")
    scoreboard = generate_recipes(20)
    # Expected first 20 recipes (from Part 1)
    expected_first_20 = [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9, 2]

    if scoreboard[:20] == expected_first_20:
        print(f"✓ Recipe generation correct: first 20 recipes match expected sequence")
        return True
    else:
        print(f"✗ Recipe generation FAILED: got {scoreboard[:20]}")
        print(f"                         expected {expected_first_20}")
        return False


def test_output_format(result):
    """Verify output format is correct"""
    print("\nValidating output format:")
    if isinstance(result, int):
        print(f"✓ Output is an integer")
    else:
        print(f"✗ Output is not an integer: {type(result)}")
        return False

    if result >= 0:
        print(f"✓ Output is non-negative")
    else:
        print(f"✗ Output is negative: {result}")
        return False

    return True


def test_deterministic():
    """Verify solution is deterministic"""
    print("\nTesting deterministic behavior:")
    result1 = solve()
    result2 = solve()
    if result1 == result2:
        print(f"✓ Solution is deterministic (result: {result1})")
        return True
    else:
        print(f"✗ Solution is not deterministic: {result1} vs {result2}")
        return False


def test_cross_validation(result, target="047801"):
    """Cross-check answer by regenerating and verifying pattern exists at claimed position"""
    print("\nCross-validating result:")
    # Regenerate scoreboard up to result + len(target)
    scoreboard = generate_recipes(result + len(target))

    # Extract pattern at claimed position
    extracted = ''.join(str(scoreboard[i]) for i in range(result, result + len(target)))

    if extracted == target:
        print(f"✓ Cross-validation passed: pattern '{target}' confirmed at position {result}")
        return True
    else:
        print(f"✗ Cross-validation FAILED: got '{extracted}', expected '{target}'")
        return False


if __name__ == '__main__':
    import time

    # Test 1: Recipe generation
    if not test_recipe_generation():
        exit(1)

    # Test 2: Examples
    print("\n" + "="*50)
    if not test_examples():
        exit(1)

    # Test 3: Actual solution
    print("\n" + "="*50)
    print("Running actual solution (pattern: 047801):")
    print("="*50)
    start = time.time()
    result = solve()
    elapsed = time.time() - start
    print(f"\nResult: {result}")
    print(f"Runtime: {elapsed:.3f}s")

    # Test 4: Output format
    if not test_output_format(result):
        exit(1)

    # Test 5: Deterministic
    if not test_deterministic():
        exit(1)

    # Test 6: Cross-validation
    if not test_cross_validation(result):
        exit(1)

    print("\n" + "="*50)
    print(f"Final Answer: {result}")
    print("="*50)
