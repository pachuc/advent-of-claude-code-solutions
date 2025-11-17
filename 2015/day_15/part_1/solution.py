def parse_input(filename):
    """
    Parse ingredient data from file.

    Returns:
        List of dictionaries, each containing:
        - name: str
        - capacity: int
        - durability: int
        - flavor: int
        - texture: int
        - calories: int
    """
    ingredients = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse format: "Name: capacity X, durability Y, flavor Z, texture W, calories C"
            parts = line.split(':')
            name = parts[0].strip()

            properties = {}
            prop_parts = parts[1].split(',')
            for prop in prop_parts:
                prop = prop.strip()
                key_value = prop.split()
                prop_name = key_value[0]
                prop_value = int(key_value[1])
                properties[prop_name] = prop_value

            ingredient = {
                'name': name,
                'capacity': properties['capacity'],
                'durability': properties['durability'],
                'flavor': properties['flavor'],
                'texture': properties['texture'],
                'calories': properties['calories']
            }
            ingredients.append(ingredient)

    return ingredients


def calculate_score(ingredients, amounts):
    """
    Calculate the total score for a given distribution of ingredients.

    Args:
        ingredients: List of ingredient dictionaries
        amounts: List of teaspoon amounts (same order as ingredients)

    Returns:
        Integer score (product of property totals, with negatives replaced by 0)
    """
    # Calculate total for each property
    capacity_total = sum(amounts[i] * ingredients[i]['capacity'] for i in range(len(ingredients)))
    durability_total = sum(amounts[i] * ingredients[i]['durability'] for i in range(len(ingredients)))
    flavor_total = sum(amounts[i] * ingredients[i]['flavor'] for i in range(len(ingredients)))
    texture_total = sum(amounts[i] * ingredients[i]['texture'] for i in range(len(ingredients)))

    # Replace negative totals with 0
    capacity_total = max(0, capacity_total)
    durability_total = max(0, durability_total)
    flavor_total = max(0, flavor_total)
    texture_total = max(0, texture_total)

    # Calculate final score
    score = capacity_total * durability_total * flavor_total * texture_total

    return score


def generate_distributions(num_ingredients, total_teaspoons):
    """
    Generate all valid distributions of teaspoons across ingredients.

    Args:
        num_ingredients: Number of ingredients
        total_teaspoons: Total teaspoons to distribute (100)

    Yields:
        Tuples of amounts that sum to total_teaspoons
    """
    if num_ingredients == 2:
        # Base case for 2 ingredients
        for a in range(total_teaspoons + 1):
            yield (a, total_teaspoons - a)
    elif num_ingredients == 3:
        # Case for 3 ingredients
        for a in range(total_teaspoons + 1):
            for b in range(total_teaspoons - a + 1):
                c = total_teaspoons - a - b
                yield (a, b, c)
    elif num_ingredients == 4:
        # Case for 4 ingredients (our main use case)
        for a in range(total_teaspoons + 1):
            for b in range(total_teaspoons - a + 1):
                for c in range(total_teaspoons - a - b + 1):
                    d = total_teaspoons - a - b - c
                    yield (a, b, c, d)
    else:
        raise NotImplementedError(f"generate_distributions not implemented for {num_ingredients} ingredients")


def find_optimal_recipe(ingredients):
    """
    Find the distribution of ingredients that maximizes the score.

    Args:
        ingredients: List of ingredient dictionaries

    Returns:
        Tuple of (max_score, optimal_amounts)
    """
    max_score = 0
    best_amounts = None

    for distribution in generate_distributions(len(ingredients), 100):
        score = calculate_score(ingredients, distribution)
        if score > max_score:
            max_score = score
            best_amounts = distribution

    return max_score, best_amounts


def verify_solution():
    """
    Quick verification of the solution with known examples.

    This function runs critical tests to ensure correctness.
    """
    # Test 1: Known example from problem statement (Butterscotch and Cinnamon)
    test_ingredients = [
        {'name': 'Butterscotch', 'capacity': -1, 'durability': -2, 'flavor': 6, 'texture': 3, 'calories': 8},
        {'name': 'Cinnamon', 'capacity': 2, 'durability': 3, 'flavor': -2, 'texture': -1, 'calories': 3}
    ]
    score = calculate_score(test_ingredients, [44, 56])
    assert score == 62842880, f"Example test failed: got {score}, expected 62842880"
    print("✓ Test 1 passed: Known example (Butterscotch + Cinnamon) = 62,842,880")

    # Test 2: Distribution count for 4 ingredients, 100 teaspoons
    count = sum(1 for _ in generate_distributions(4, 100))
    assert count == 176851, f"Distribution count test failed: got {count}, expected 176851"
    print(f"✓ Test 2 passed: Generated exactly 176,851 distributions")

    # Test 3: Distribution constraints (first 1000 distributions)
    for i, dist in enumerate(generate_distributions(4, 100)):
        if i >= 1000:
            break
        assert sum(dist) == 100, f"Distribution {dist} doesn't sum to 100"
        assert all(x >= 0 for x in dist), f"Distribution {dist} has negative values"
    print("✓ Test 3 passed: First 1000 distributions sum to 100 and are non-negative")

    # Test 4: Small scale verification (2 ingredients, 3 teaspoons)
    small_dists = list(generate_distributions(2, 3))
    expected_small = [(0, 3), (1, 2), (2, 1), (3, 0)]
    assert len(small_dists) == 4, f"Small test failed: expected 4, got {len(small_dists)}"
    assert small_dists == expected_small, f"Small test failed: distributions don't match"
    print("✓ Test 4 passed: Small scale verification (2 ingredients, 3 teaspoons)")

    # Test 5: Zero property handling
    test_ingredients_zero = [
        {'name': 'A', 'capacity': -10, 'durability': 1, 'flavor': 1, 'texture': 1, 'calories': 0},
        {'name': 'B', 'capacity': 0, 'durability': 0, 'flavor': 0, 'texture': 0, 'calories': 0}
    ]
    score = calculate_score(test_ingredients_zero, [100, 0])
    assert score == 0, f"Zero handling test failed: capacity should be 0, score should be 0, got {score}"
    print("✓ Test 5 passed: Negative property totals correctly replaced with 0")


def main():
    """Main execution function."""
    import time

    # Run verification tests first
    print("Running verification tests...")
    verify_solution()
    print("\nAll verification tests passed!\n")

    # Parse input
    ingredients = parse_input('input.md')
    print(f"Parsed {len(ingredients)} ingredients:")
    for ing in ingredients:
        print(f"  {ing['name']}: capacity={ing['capacity']}, durability={ing['durability']}, "
              f"flavor={ing['flavor']}, texture={ing['texture']}, calories={ing['calories']}")
    print()

    # Find optimal recipe with timing
    print("Searching for optimal recipe...")
    start_time = time.time()
    max_score, optimal_amounts = find_optimal_recipe(ingredients)
    elapsed_time = time.time() - start_time

    # Output result (this is the main answer)
    print(max_score)

    # Print additional details for verification
    print(f"\nOptimal distribution:")
    for i, ing in enumerate(ingredients):
        print(f"  {ing['name']}: {optimal_amounts[i]} teaspoons")
    print(f"\nTotal teaspoons: {sum(optimal_amounts)}")

    # Verify the score manually
    capacity = sum(optimal_amounts[i] * ingredients[i]['capacity'] for i in range(len(ingredients)))
    durability = sum(optimal_amounts[i] * ingredients[i]['durability'] for i in range(len(ingredients)))
    flavor = sum(optimal_amounts[i] * ingredients[i]['flavor'] for i in range(len(ingredients)))
    texture = sum(optimal_amounts[i] * ingredients[i]['texture'] for i in range(len(ingredients)))

    print(f"\nProperty totals:")
    print(f"  Capacity: {capacity} -> {max(0, capacity)}")
    print(f"  Durability: {durability} -> {max(0, durability)}")
    print(f"  Flavor: {flavor} -> {max(0, flavor)}")
    print(f"  Texture: {texture} -> {max(0, texture)}")
    print(f"  Score: {max(0, capacity)} × {max(0, durability)} × {max(0, flavor)} × {max(0, texture)} = {max_score}")

    print(f"\nExecution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
