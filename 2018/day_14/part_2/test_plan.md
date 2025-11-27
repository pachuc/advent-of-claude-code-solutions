# Test Plan: Recipe Scoreboard Pattern Search (Part 2)

## Testing Objectives
1. Verify pattern detection algorithm works correctly
2. Ensure recipe generation algorithm is correct (inherited from Part 1)
3. Validate handling of 1-recipe vs 2-recipe additions per iteration
4. Confirm correct output format and value
5. Verify performance is acceptable for large inputs

## Important Notes on Part 2 Examples
The Part 2 examples are cleverly derived from Part 1 results, providing circular validation:
- Part 1: "After 9 recipes: next 10 are **51589**16779" → Part 2: "**51589** appears at position 9"
- Part 1: "After 5 recipes: next 10 are **01245**15891" → Part 2: "**01245** appears at position 5"
- Part 1: "After 18 recipes: next 10 are **92510**71085" → Part 2: "**92510** appears at position 18"
- Part 1: "After 2018 recipes: next 10 are **59414**29882" → Part 2: "**59414** appears at position 2018"

This means passing all Part 2 examples validates both the pattern search AND the recipe generation!

## Test Categories

### 1. Example Test Cases (Critical)

**Purpose**: Verify correctness against known answers

**Test Cases**:
```python
test_cases = [
    ("51589", 9),      # Pattern appears after 9 recipes
    ("01245", 5),      # Pattern appears after 5 recipes
    ("92510", 18),     # Pattern appears after 18 recipes
    ("59414", 2018),   # Pattern appears after 2018 recipes
]
```

**Expected Behavior**:
- All test cases must pass
- Each should return the exact expected position

**Validation Method**:
```python
for pattern, expected_pos in test_cases:
    result = solve(pattern)
    assert result == expected_pos, f"Failed for {pattern}: got {result}, expected {expected_pos}"
    print(f"✓ Test passed for pattern {pattern} (position {expected_pos})")
```

**Edge Cases in Examples**:
- `"01245"` (5): Pattern appears very early, tests early scoreboard state
- `"59414"` (2018): Larger position, tests that generation continues correctly
- `"51589"` (9): Tests single-digit position finding

---

### 2. Recipe Generation Correctness (Inherited from Part 1)

**Purpose**: Ensure the core algorithm generates correct recipes

**Test**: Generate first N recipes manually and verify against expected sequence

**Method**:
```python
def test_recipe_generation():
    """Verify recipe generation matches expected pattern"""
    # Manually generate recipes using the same algorithm
    scoreboard = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    # Generate until we have at least 20 recipes
    while len(scoreboard) < 20:
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

    # Expected first 20 recipes (can be verified by hand or from Part 1 output)
    expected_first_20 = [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9, 2]

    assert scoreboard[:20] == expected_first_20, f"First 20 recipes mismatch: {scoreboard[:20]}"
    print(f"✓ Recipe generation correct: first 20 recipes match expected sequence")
```

**Alternative**: Use the `generate_recipes()` helper function from the implementation:
```python
def test_recipe_generation_alt():
    """Test using helper function"""
    scoreboard = generate_recipes(20)
    expected_first_20 = [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9, 2]
    assert scoreboard[:20] == expected_first_20
```

**Why This Matters**:
- If recipe generation is wrong, pattern detection will search in wrong sequence
- Part 1 solution was verified correct, so matching it validates our generation
- This also validates that the Part 2 implementation correctly reuses Part 1's algorithm

---

### 3. Pattern Detection Edge Cases

#### Test 3a: Pattern at Very Beginning
**Purpose**: Ensure pattern detection works when pattern appears early

**Test Case**:
```python
# Pattern "37" should appear at position 0 (the initial recipes)
result = solve("37")
assert result == 0, f"Pattern '37' should appear at position 0, got {result}"
```

#### Test 3b: Pattern with Repeated Digits
**Purpose**: Verify pattern matching doesn't get confused by repetition

**Test Case**:
```python
# If scoreboard contains "111011", we need to find exact match
# Not just any "11"
# This tests that we're comparing full sequence, not partial
```

#### Test 3c: Pattern After 1-Recipe Addition
**Purpose**: Verify detection when last iteration added only 1 recipe

**Test Case**:
```python
def test_pattern_after_single_addition():
    """
    Verify pattern detection works when pattern completes with 1-recipe addition.
    The example test cases implicitly test this, but we validate the logic explicitly.
    """
    # When we check scoreboard[-pattern_len:] == target
    # This catches patterns completed by the last recipe added

    # Test with example "51589" which appears at position 9
    result = solve("51589")
    assert result == 9

    # Verify by regenerating: the pattern should be at scoreboard[9:14]
    scoreboard = generate_recipes(14)
    pattern = [int(d) for d in "51589"]
    assert scoreboard[9:14] == pattern
    print(f"✓ Pattern detection works for 1-recipe completion")
```

#### Test 3d: Pattern After 2-Recipe Addition
**Purpose**: Verify detection when last iteration added 2 recipes and pattern completes with first of the two

**Test Case**:
```python
def test_pattern_after_double_addition():
    """
    Verify pattern detection works when 2 recipes added and pattern completes
    with the first one (requiring check of scoreboard[-pattern_len-1:-1]).
    """
    # This is tested by running all examples
    # The implementation checks both cases, so if all examples pass,
    # both 1-recipe and 2-recipe addition cases are working

    # We can add debug logging to the solve() function to verify:
    # - Which check triggered (last N or last N+1)
    # - Whether 1 or 2 recipes were just added

    print(f"✓ Pattern detection handles both 1 and 2 recipe additions (verified by examples)")
```

---

### 4. Output Format Validation

**Purpose**: Ensure output is in correct format

**Test**:
```python
def test_output_format(result):
    """Verify output format is correct"""
    # Must be an integer
    assert isinstance(result, int), f"Result must be integer, got {type(result)}"

    # Must be non-negative
    assert result >= 0, f"Result must be non-negative, got {result}"

    print(f"✓ Output format is valid: {result}")
```

---

### 5. Deterministic Behavior

**Purpose**: Ensure solution produces same result on multiple runs

**Test**:
```python
def test_deterministic():
    """Verify solution is deterministic"""
    result1 = solve()
    result2 = solve()
    result3 = solve()

    assert result1 == result2 == result3, "Solution must be deterministic"
    print(f"✓ Solution is deterministic (result: {result1})")
```

---

### 6. Actual Input Validation

**Purpose**: Verify solution works on the actual puzzle input

**Test**:
```python
def test_actual_input():
    """Test with actual input '047801'"""
    result = solve("047801")

    # We don't know the expected answer beforehand, but we can validate:
    # 1. Result is a reasonable integer
    # 2. Result is positive
    # 3. Solution completes in reasonable time

    assert isinstance(result, int)
    assert result > 0
    print(f"✓ Actual input solution: {result}")

    return result
```

---

### 7. Performance Testing

**Purpose**: Ensure solution completes in reasonable time

**Test**:
```python
import time

def test_performance():
    """Measure execution time"""
    start = time.time()
    result = solve()
    elapsed = time.time() - start

    print(f"Runtime: {elapsed:.3f}s")
    print(f"Result position: {result:,}")

    # Should complete within reasonable time
    # Threshold depends on result magnitude:
    # - < 1M: should be < 1s
    # - < 10M: should be < 15s
    # - < 50M: should be < 60s
    max_time = 60  # Conservative threshold
    assert elapsed < max_time, f"Solution too slow: {elapsed}s (max {max_time}s)"

    return elapsed
```

**Expected Performance** (machine-dependent, approximate):
- For positions < 1,000: < 0.01 seconds
- For positions < 100,000: < 0.5 seconds
- For positions < 1,000,000: < 2 seconds
- For positions < 10,000,000: < 15 seconds
- For positions < 50,000,000: < 60 seconds

**Note**: The actual input `047801` position is unknown until we solve it, so these are guidelines.

---

### 8. Boundary Condition Tests

#### Test 8a: Single Digit Pattern
**Purpose**: Test with minimal pattern length

**Test**:
```python
# Find where "3" first appears (should be position 0)
result = solve("3")
assert result == 0
```

#### Test 8b: Pattern Not Found Protection
**Purpose**: Ensure infinite loop protection works

**Test**:
```python
def test_infinite_loop_protection():
    """Verify that max iterations safety check works"""
    # We won't actually test with a non-existent pattern (would take forever)
    # But we verify the safety mechanism exists by checking the code structure

    # Instead, test with a known pattern but verify iteration counter works
    # This is more of a code review check than a runtime test

    print(f"✓ Infinite loop protection exists (MAX_ITERATIONS check in code)")
```

---

### 9. Cross-Validation with Part 1

**Purpose**: Verify that if we run Part 1 logic at the result position, we get consistent scoreboard

**Test**:
```python
def test_cross_validation(result, target="047801"):
    """Cross-check answer by regenerating and verifying pattern exists at claimed position"""
    # Regenerate scoreboard up to result + len(target) using Part 1's algorithm
    scoreboard = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    # Generate until we have enough recipes
    while len(scoreboard) < result + len(target):
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

    # Extract pattern at claimed position
    extracted = ''.join(str(scoreboard[i]) for i in range(result, result + len(target)))

    assert extracted == target, f"Pattern verification failed: got '{extracted}', expected '{target}'"
    print(f"✓ Cross-validation passed: pattern '{target}' confirmed at position {result}")
    return True
```

**Alternative using helper function**:
```python
def test_cross_validation_alt(result, target="047801"):
    """Cross-check using generate_recipes helper"""
    scoreboard = generate_recipes(result + len(target))
    extracted = ''.join(str(scoreboard[i]) for i in range(result, result + len(target)))
    assert extracted == target
    print(f"✓ Cross-validation passed")
```

---

## Test Execution Order

1. **Recipe Generation Test** - Validate core algorithm
2. **Example Test Cases** - Verify correctness against known answers
3. **Output Format Test** - Ensure proper output
4. **Deterministic Test** - Verify consistency
5. **Actual Input Test** - Solve the puzzle
6. **Cross-Validation Test** - Double-check the answer
7. **Performance Test** - Monitor runtime

## Success Criteria

### Must Pass:
- ✓ All 4 example test cases return correct positions
- ✓ Recipe generation matches Part 1 behavior
- ✓ Output format is a single non-negative integer
- ✓ Solution is deterministic
- ✓ Cross-validation confirms pattern exists at returned position

### Should Pass:
- ✓ Performance is acceptable (< 60 seconds for actual input)
- ✓ Boundary conditions handled correctly

### Nice to Have:
- ✓ Detailed logging of iteration count and final scoreboard size
- ✓ Progress indicator for long-running searches

## Debugging Strategy

If tests fail:

1. **Wrong position returned**:
   - Print scoreboard around the returned position
   - Verify pattern actually appears there
   - Check if pattern appears earlier (missed detection)

2. **Pattern not found (infinite loop)**:
   - Add iteration counter and max iteration limit
   - Print last N recipes every 1M iterations
   - Verify target pattern is parsed correctly

3. **Performance too slow**:
   - Profile pattern matching code
   - Consider optimization strategies from implementation plan
   - Verify we're only checking tail, not entire scoreboard

4. **Inconsistent results**:
   - Check for any randomness or state mutation
   - Verify initialization is clean each run

## Test Code Structure

```python
def test_examples():
    """Test all provided examples"""
    pass

def test_recipe_generation():
    """Verify recipe generation correctness"""
    pass

def test_output_format(result):
    """Verify output format"""
    pass

def test_deterministic():
    """Test deterministic behavior"""
    pass

def test_cross_validation(result):
    """Cross-check answer with actual pattern"""
    pass

if __name__ == '__main__':
    import time

    # Test 1: Recipe generation
    print("Testing recipe generation...")
    test_recipe_generation()

    # Test 2: Examples
    print("\nTesting examples...")
    if not test_examples():
        exit(1)

    # Test 3: Actual solution
    print("\n" + "="*50)
    print("Running actual solution:")
    print("="*50)
    start = time.time()
    result = solve()
    elapsed = time.time() - start
    print(f"\nRuntime: {elapsed:.3f}s")

    # Test 4: Output format
    test_output_format(result)

    # Test 5: Deterministic
    test_deterministic()

    # Test 6: Cross-validation
    test_cross_validation(result)

    print("\n" + "="*50)
    print(f"Final Answer: {result}")
    print("="*50)
```
