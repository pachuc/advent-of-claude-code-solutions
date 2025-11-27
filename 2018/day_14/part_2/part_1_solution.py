def solve(num_recipes=None):
    """
    Solve the recipe scoreboard problem.

    Args:
        num_recipes: Number of recipes to skip before extracting result.
                    If None, reads from input.md file.

    Returns:
        String of 10 digits representing the next 10 recipe scores.
    """
    # Step 1: Parse input
    if num_recipes is None:
        with open('input.md', 'r') as f:
            num_recipes = int(f.read().strip())

    # Step 2: Initialize state
    scoreboard = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    # Step 3: Generate recipes
    while len(scoreboard) < num_recipes + 10:
        # 3a: Create new recipes
        score1 = scoreboard[elf1_pos]
        score2 = scoreboard[elf2_pos]
        recipe_sum = score1 + score2

        if recipe_sum >= 10:
            scoreboard.append(1)
            scoreboard.append(recipe_sum - 10)
        else:
            scoreboard.append(recipe_sum)

        # 3b: Update positions (using updated scoreboard length)
        elf1_pos = (elf1_pos + 1 + score1) % len(scoreboard)
        elf2_pos = (elf2_pos + 1 + score2) % len(scoreboard)

    # Step 4: Extract result
    result = ''.join(str(score) for score in scoreboard[num_recipes:num_recipes + 10])

    # Step 5: Output
    print(result)
    return result


def test_examples():
    """Test all provided examples"""
    test_cases = [
        (9, "5158916779"),
        (5, "0124515891"),
        (18, "9251071085"),
        (2018, "5941429882"),
    ]

    print("Testing examples:")
    for num_recipes, expected in test_cases:
        result = solve(num_recipes)
        if result == expected:
            print(f"✓ Test passed for n={num_recipes}")
        else:
            print(f"✗ Test FAILED for n={num_recipes}: got {result}, expected {expected}")
            return False
    return True


def test_first_10_recipes():
    """Test that the first 10 recipes match expected pattern"""
    print("\nTesting first 10 recipes:")
    result = solve(0)
    expected = "3710101245"
    if result == expected:
        print(f"✓ First 10 recipes are correct: {result}")
        return True
    else:
        print(f"✗ First 10 recipes FAILED: got {result}, expected {expected}")
        return False


def test_output_format(result):
    """Verify output format is correct"""
    print("\nValidating output format:")
    if len(result) == 10:
        print(f"✓ Output length is 10")
    else:
        print(f"✗ Output length is {len(result)}, expected 10")
        return False

    if all(c.isdigit() for c in result):
        print(f"✓ All characters are digits")
    else:
        print(f"✗ Output contains non-digit characters")
        return False

    return True


def test_deterministic():
    """Verify solution is deterministic"""
    print("\nTesting deterministic behavior:")
    result1 = solve()
    result2 = solve()
    result3 = solve()
    if result1 == result2 == result3:
        print(f"✓ Solution is deterministic (all runs returned: {result1})")
        return True
    else:
        print(f"✗ Solution is not deterministic")
        return False


if __name__ == '__main__':
    import time

    # Run example tests
    if not test_examples():
        exit(1)

    # Test first 10 recipes
    if not test_first_10_recipes():
        exit(1)

    # Run actual solution with timing
    print("\n" + "="*50)
    print("Running actual solution (n=47801):")
    print("="*50)
    start = time.time()
    result = solve()
    elapsed = time.time() - start
    print(f"\nRuntime: {elapsed:.3f}s")

    # Validate output format
    test_output_format(result)

    # Test deterministic behavior
    test_deterministic()

    print("\n" + "="*50)
    print(f"Final Answer: {result}")
    print("="*50)
