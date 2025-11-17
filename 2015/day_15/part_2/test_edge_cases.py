"""Test edge cases for the solution."""
import tempfile
import os
from solution import parse_ingredients, calculate_score, calculate_calories, find_max_score

print("Running edge case tests...")
print("=" * 60)

# Test 1: Simple two-ingredient case where all combinations have same calories
print("\nTest 1: Two ingredients, all combinations yield 500 calories")
test_input_1 = """A: capacity 1, durability 1, flavor 1, texture 1, calories 5
B: capacity 1, durability 1, flavor 1, texture 1, calories 5"""

with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write(test_input_1)
    temp_file_1 = f.name

try:
    ingredients = parse_ingredients(temp_file_1)
    score, amounts = find_max_score(ingredients)
    # With 100 teaspoons and 5 cal/tsp, total is always 500 calories
    # All properties total to 100, so score = 100^4 = 100,000,000
    expected_score = 100 * 100 * 100 * 100
    print(f"  Expected score: {expected_score}")
    print(f"  Actual score: {score}")
    print(f"  Best amounts: {amounts}")
    assert score == expected_score, f"Score mismatch! Expected {expected_score}, got {score}"
    print("  ✓ PASSED")
finally:
    os.unlink(temp_file_1)

# Test 2: Impossible calorie constraint
print("\nTest 2: Impossible calorie constraint (min 1000, need 500)")
test_input_2 = """A: capacity 1, durability 1, flavor 1, texture 1, calories 10
B: capacity 1, durability 1, flavor 1, texture 1, calories 10"""

with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write(test_input_2)
    temp_file_2 = f.name

try:
    ingredients = parse_ingredients(temp_file_2)
    score, amounts = find_max_score(ingredients)
    # No combination can achieve 500 calories (minimum is 1000)
    print(f"  Expected score: 0")
    print(f"  Actual score: {score}")
    print(f"  Best amounts: {amounts}")
    assert score == 0, f"Score should be 0 when no valid combination exists!"
    assert amounts is None, "Best amounts should be None when no valid combination exists!"
    print("  ✓ PASSED")
finally:
    os.unlink(temp_file_2)

# Test 3: Negative property values
print("\nTest 3: Single ingredient with all negative properties")
test_input_3 = """A: capacity -1, durability -1, flavor -1, texture -1, calories 5"""

with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write(test_input_3)
    temp_file_3 = f.name

try:
    ingredients = parse_ingredients(temp_file_3)
    score, amounts = find_max_score(ingredients)
    # All properties become 0 after max(), so score is 0
    print(f"  Expected score: 0")
    print(f"  Actual score: {score}")
    print(f"  Best amounts: {amounts}")
    assert score == 0, f"Score should be 0 when all properties are negative!"
    print("  ✓ PASSED")
finally:
    os.unlink(temp_file_3)

# Test 4: Three ingredients to verify variable number support
print("\nTest 4: Three ingredients (not hardcoded to 4)")
test_input_4 = """A: capacity 2, durability 2, flavor 2, texture 2, calories 5
B: capacity 1, durability 1, flavor 1, texture 1, calories 5
C: capacity 1, durability 1, flavor 1, texture 1, calories 5"""

with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write(test_input_4)
    temp_file_4 = f.name

try:
    ingredients = parse_ingredients(temp_file_4)
    score, amounts = find_max_score(ingredients)
    print(f"  Score: {score}")
    print(f"  Best amounts: {amounts}")
    print(f"  Total teaspoons: {sum(amounts) if amounts else 0}")
    print(f"  Total calories: {calculate_calories(amounts, ingredients) if amounts else 0}")
    assert score > 0, "Should find a valid combination with 3 ingredients!"
    assert sum(amounts) == 100, "Should use exactly 100 teaspoons!"
    assert calculate_calories(amounts, ingredients) == 500, "Should have exactly 500 calories!"
    print("  ✓ PASSED")
finally:
    os.unlink(temp_file_4)

print("\n" + "=" * 60)
print("All edge case tests PASSED!")
print("=" * 60)
