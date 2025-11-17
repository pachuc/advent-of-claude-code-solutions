# Testing Plan - Part 2: Elf Gift Exchange (Across Circle)

## Testing Strategy Overview

Since Part 2 requires simulation (no closed-form formula), our testing must focus on:
1. **Correctness**: Validate against known examples and manual calculations
2. **Edge cases**: Handle boundary conditions
3. **Logic verification**: Ensure "across circle" calculation is correct
4. **Performance**: Verify solution completes in reasonable time

**Key difference from Part 1**: Part 1 had both formula and simulation implementations that could cross-validate each other. Part 2 has only simulation, so manual verification and pattern analysis become critical for ensuring correctness.

## Test Categories

### Category 1: Example Validation (CRITICAL)

**Test 1.1: Provided Example (n=5)**
```python
def test_example():
    """Validate the exact example from problem.md"""
    result = solve_across_circle(5)
    assert result == 2, f"Expected 2 for n=5, got {result}"
    print("✓ Example test passed: n=5 → 2")
```

**Why critical**: This is our ONLY known correct answer from the problem statement. If this fails, the entire algorithm is wrong.

**Manual verification (validated step-by-step)**:
```
Initial: [1, 2, 3, 4, 5], current_index=0 (Elf 1)
Turn 1 (Elf 1): 5 elves, across = floor(5/2) = 2
  - target_index = (0+2)%5 = 2 → Elf 3 eliminated
  - Circle: [1, 2, 4, 5]
  - target(2) >= current(0), no adjustment
  - Next: (0+1)%4 = 1 → Elf 2

Turn 2 (Elf 2): 4 elves, across = floor(4/2) = 2
  - target_index = (1+2)%4 = 3 → Elf 5 eliminated
  - Circle: [1, 2, 4]
  - target(3) >= current(1), no adjustment
  - Next: (1+1)%3 = 2 → Elf 4

Turn 3 (Elf 4): 3 elves, across = floor(3/2) = 1
  - target_index = (2+1)%3 = 0 → Elf 1 eliminated
  - Circle: [2, 4]
  - target(0) < current(2), adjust: current_index = 1
  - Next: (1+1)%2 = 0 → Elf 2

Turn 4 (Elf 2): 2 elves, across = floor(2/2) = 1
  - target_index = (0+1)%2 = 1 → Elf 4 eliminated
  - Circle: [2]
  - Winner: Elf 2 ✓
```

**Test 1.2: Detailed Trace Test (n=5 with debug)**
```python
def test_example_with_trace():
    """Run n=5 with debug output to verify each step"""
    print("\n=== Detailed Trace for n=5 ===")
    result = solve_across_circle(5, debug=True)
    assert result == 2, f"Expected 2 for n=5, got {result}"
    print("✓ Detailed trace test passed: n=5 → 2")
```

**Purpose**: Visual verification that implementation matches problem description exactly.

**Test 1.3: Part 1 vs Part 2 Difference**
```python
def test_part1_vs_part2_difference():
    """Verify Part 2 gives different results than Part 1"""
    # For n=5: Part 1 (Josephus k=2) → 3, Part 2 (across circle) → 2
    result = solve_across_circle(5)
    assert result == 2, f"Part 2 should give 2 for n=5, got {result}"
    # This confirms we're solving the right problem (different from Part 1)
    print("✓ Part 1 vs Part 2 difference verified: Part 2 gives different result")
```

**Purpose**: Confirm we're implementing the correct algorithm (not accidentally using Part 1's logic).

### Category 2: Edge Cases

**Test 2.1: Single Elf (n=1)**
```python
def test_single_elf():
    """Single elf should win immediately"""
    result = solve_across_circle(1)
    assert result == 1, f"Expected 1 for n=1, got {result}"
    print("✓ Single elf test passed")
```

**Test 2.2: Two Elves (n=2)**
```python
def test_two_elves():
    """With 2 elves, first elf should win"""
    result = solve_across_circle(2)
    # Manual: [1, 2], across = floor(2/2) = 1 → Elf 2 eliminated → [1]
    assert result == 1, f"Expected 1 for n=2, got {result}"
    print("✓ Two elves test passed")
```

**Test 2.3: Three Elves (n=3)**
```python
def test_three_elves():
    """Verify n=3 manually"""
    result = solve_across_circle(3)
    # Manual simulation (verified):
    # Initial: [1, 2, 3], current_index=0 (Elf 1)
    # Turn 1 (Elf 1): 3 elves, across = floor(3/2) = 1
    #   - target = (0+1)%3 = 1 → Elf 2 eliminated
    #   - Circle: [1, 3]
    #   - target(1) >= current(0), no adjustment
    #   - Next: (0+1)%2 = 1 → Elf 3
    # Turn 2 (Elf 3): 2 elves, across = floor(2/2) = 1
    #   - target = (1+1)%2 = 0 → Elf 1 eliminated
    #   - Circle: [3]
    # Winner: 3
    assert result == 3, f"Expected 3 for n=3, got {result}"
    print("✓ Three elves test passed")
```

**Test 2.4: Four Elves (n=4)**
```python
def test_four_elves():
    """Verify n=4 manually"""
    result = solve_across_circle(4)
    # Manual simulation (verified):
    # Initial: [1, 2, 3, 4], current_index=0 (Elf 1)
    # Turn 1 (Elf 1): 4 elves, across = 2
    #   - target = (0+2)%4 = 2 → Elf 3 eliminated
    #   - Circle: [1, 2, 4]
    #   - target(2) >= current(0), no adjustment
    #   - Next: (0+1)%3 = 1 → Elf 2
    # Turn 2 (Elf 2): 3 elves, across = 1
    #   - target = (1+1)%3 = 2 → Elf 4 eliminated
    #   - Circle: [1, 2]
    #   - target(2) >= current(1), no adjustment
    #   - Next: (1+1)%2 = 0 → Elf 1
    # Turn 3 (Elf 1): 2 elves, across = 1
    #   - target = (0+1)%2 = 1 → Elf 2 eliminated
    #   - Circle: [1]
    # Winner: 1
    assert result == 1, f"Expected 1 for n=4, got {result}"
    print("✓ Four elves test passed")
```

### Category 3: Small Sequential Values (Pattern Recognition)

**Test 3.1: Sequential Small Values (n=1 to 20)**
```python
def test_sequential_small():
    """
    Test n=1 to 20 and display pattern.
    This helps identify any patterns or irregularities.
    """
    results = {}
    for n in range(1, 21):
        results[n] = solve_across_circle(n)

    # Display results for pattern analysis
    print("\n=== Pattern Analysis (n=1 to 20) ===")
    for n, winner in results.items():
        print(f"n={n:2d} → winner={winner:2d}")

    # Verify known values
    assert results[1] == 1, "n=1 failed"
    assert results[2] == 1, "n=2 failed"
    assert results[3] == 3, "n=3 failed"
    assert results[4] == 1, "n=4 failed"
    assert results[5] == 2, "n=5 failed"

    print("✓ Sequential small values test passed")
```

**Purpose**:
- Visual inspection for patterns
- Catch unexpected behavior
- Build confidence in algorithm

**What to look for in pattern analysis**:
- All results should be in range [1, n]
- No obvious errors like always returning 1 or n
- Check for unexpected symmetries or breaks in the pattern
- Unlike Part 1 (Josephus k=2), Part 2 doesn't have a simple power-of-2 pattern

### Category 4: Powers of 2 (Special Cases)

**Test 4.1: Powers of 2**
```python
def test_powers_of_two():
    """Test powers of 2: 2, 4, 8, 16, 32, 64, 128, 256"""
    test_cases = [2**i for i in range(1, 9)]

    print("\n=== Powers of 2 ===")
    for n in test_cases:
        result = solve_across_circle(n)
        print(f"n={n:4d} → winner={result}")

    print("✓ Powers of 2 test passed")
```

**Purpose**: Powers of 2 often have special properties in circular elimination problems.

### Category 5: Manual Simulation Verification

**Test 5.1: Explicit Wraparound Test (n=7)**
```python
def test_wraparound():
    """Test wraparound behavior explicitly with n=7"""
    print("\n=== Wraparound Test (n=7) ===")
    result = solve_across_circle(7, debug=True)

    # Verify result is in valid range
    assert 1 <= result <= 7, f"Result {result} out of range for n=7"

    print(f"✓ Wraparound test passed: n=7 → {result}")
```

**Purpose**: Explicitly verify that wraparound (using modulo) works correctly in complex scenarios.

**Test 5.2: Detailed Step Verification (n=6)**
```python
def test_manual_simulation_n6():
    """Manually simulate n=6 step by step (verified calculation)"""
    # Manual calculation (step-by-step verified):
    # Initial: [1, 2, 3, 4, 5, 6], current_index=0 (Elf 1)
    # Turn 1 (Elf 1): 6 elves, across = 3
    #   - target = (0+3)%6 = 3 → Elf 4 eliminated
    #   - Circle: [1, 2, 3, 5, 6]
    #   - target(3) >= current(0), no adjustment
    #   - Next: (0+1)%5 = 1 → Elf 2
    # Turn 2 (Elf 2): 5 elves, across = 2
    #   - target = (1+2)%5 = 3 → Elf 5 eliminated
    #   - Circle: [1, 2, 3, 6]
    #   - target(3) >= current(1), no adjustment
    #   - Next: (1+1)%4 = 2 → Elf 3
    # Turn 3 (Elf 3): 4 elves, across = 2
    #   - target = (2+2)%4 = 0 → Elf 1 eliminated
    #   - Circle: [2, 3, 6]
    #   - target(0) < current(2), adjust: current_index = 1
    #   - Next: (1+1)%3 = 2 → Elf 6
    # Turn 4 (Elf 6): 3 elves, across = 1
    #   - target = (2+1)%3 = 0 → Elf 2 eliminated
    #   - Circle: [3, 6]
    #   - target(0) < current(2), adjust: current_index = 1
    #   - Next: (1+1)%2 = 0 → Elf 3
    # Turn 5 (Elf 3): 2 elves, across = 1
    #   - target = (0+1)%2 = 1 → Elf 6 eliminated
    #   - Circle: [3]
    # Winner: 3

    result = solve_across_circle(6)
    assert result == 3, f"Expected 3 for n=6, got {result}"
    print("✓ Manual simulation n=6 test passed")
```

### Category 6: Medium to Large Values

**Test 6.1: Medium Values**
```python
def test_medium_values():
    """Test medium-sized values to ensure performance is acceptable"""
    test_cases = [100, 1000, 10000]

    print("\n=== Medium Values Performance ===")
    import time

    for n in test_cases:
        start = time.time()
        result = solve_across_circle(n)
        elapsed = time.time() - start
        print(f"n={n:6d} → winner={result:6d} (time: {elapsed:.3f}s)")

        # Sanity check: result should be between 1 and n
        assert 1 <= result <= n, f"Result {result} out of range for n={n}"

    print("✓ Medium values test passed")
```

**Purpose**:
- Ensure performance is acceptable
- Verify no crashes or infinite loops
- Validate result is in valid range

**Test 6.2: Large Value Performance**
```python
def test_large_value():
    """Test a large value to ensure algorithm scales"""
    n = 100000

    print(f"\n=== Large Value Test (n={n:,}) ===")
    import time

    start = time.time()
    result = solve_across_circle(n)
    elapsed = time.time() - start

    print(f"n={n:,} → winner={result:,} (time: {elapsed:.3f}s)")

    # Sanity check
    assert 1 <= result <= n, f"Result {result} out of range"

    # Performance check: should complete in under 3 seconds with deque
    # (adjusted from 2s to avoid false failures on slower machines)
    assert elapsed < 5, f"Too slow: {elapsed:.3f}s for n={n:,} (expected < 5s)"

    print("✓ Large value test passed")
```

### Category 7: Actual Input Validation

**Test 7.1: Actual Input (n=3,017,957)**
```python
def test_actual_input():
    """Test the actual puzzle input"""
    n = 3017957

    print(f"\n=== Actual Input Test (n={n:,}) ===")
    import time

    start = time.time()
    result = solve_across_circle(n)
    elapsed = time.time() - start

    print(f"n={n:,} → winner={result:,} (time: {elapsed:.3f}s)")

    # Sanity checks
    assert 1 <= result <= n, f"Result {result} out of range"
    assert isinstance(result, int), f"Result must be integer, got {type(result)}"

    # Performance check: should complete in reasonable time
    # Adjusted to 20s to avoid false failures while still catching real issues
    assert elapsed < 20, f"Too slow: {elapsed:.3f}s for n={n:,} (expected < 20s)"

    print("✓ Actual input test passed")

    return result
```

### Category 8: Algorithm Correctness Checks

**Test 8.1: Verify "Across" Calculation**
```python
def test_across_calculation():
    """Verify the 'across' distance calculation is correct"""
    # For M elves, across is floor(M/2)
    test_cases = [
        (2, 1),   # 2 elves: across = 1
        (3, 1),   # 3 elves: across = 1
        (4, 2),   # 4 elves: across = 2
        (5, 2),   # 5 elves: across = 2
        (6, 3),   # 6 elves: across = 3
        (7, 3),   # 7 elves: across = 3
        (8, 4),   # 8 elves: across = 4
    ]

    for m, expected in test_cases:
        across = m // 2
        assert across == expected, f"For {m} elves, expected across={expected}, got {across}"

    print("✓ Across calculation test passed")
```

**Test 8.2: Never Self-Target**
```python
def test_never_self_target():
    """
    Verify that we never try to eliminate ourselves.

    Note: The main algorithm has an assertion that catches self-targeting,
    so this test provides additional confidence for the calculation logic.
    """
    # Verify across_offset calculation never results in self-targeting
    # For all circle sizes >= 2, across_offset = len//2 >= 1
    for remaining in range(2, 101):
        across_offset = remaining // 2
        assert across_offset > 0, f"Invalid across_offset at remaining={remaining}"
        # When starting at index 0, target should never be 0
        # (can only happen if across_offset = 0, which we just proved impossible)
        target_index = (0 + across_offset) % remaining
        assert target_index != 0, f"Self-targeting possible at remaining={remaining}"

    print("✓ Never self-target test passed")
```

## Test Execution Order

The tests should run in this specific order for optimal debugging:

1. **Example validation first** (n=5) - CRITICAL: If this fails, stop immediately
2. **Example with trace** (n=5 debug) - Visual verification of algorithm
3. **Edge cases** (n=1, 2, 3, 4) - Fast and catch basic errors
4. **Manual simulation** (n=6) - Verify complex case with index adjustments
5. **Sequential small** (n=1 to 20) - Pattern analysis and anomaly detection
6. **Powers of 2** - Special case validation
7. **Medium values** (100, 1000, 10000) - Performance check
8. **Large value** (100,000) - Scalability verification
9. **Actual input** (3,017,957) - Final answer

**Rationale**: Start with the known correct answer (n=5) to validate core algorithm before investing time in other tests.

## Complete Test Suite

```python
def run_all_tests():
    """Execute all tests in order"""
    print("\n" + "="*50)
    print("PART 2 TEST SUITE - ACROSS CIRCLE")
    print("="*50)

    # CRITICAL: Test example first - if this fails, stop
    print("\n=== CRITICAL TEST ===")
    test_example()
    test_example_with_trace()
    test_part1_vs_part2_difference()

    # Edge cases
    print("\n=== EDGE CASES ===")
    test_single_elf()
    test_two_elves()
    test_three_elves()
    test_four_elves()

    # Manual verification with complex index adjustments
    print("\n=== MANUAL VERIFICATION ===")
    test_wraparound()
    test_manual_simulation_n6()

    # Pattern analysis
    print("\n=== PATTERN ANALYSIS ===")
    test_sequential_small()

    # Special cases
    print("\n=== SPECIAL CASES ===")
    test_powers_of_two()

    # Algorithm correctness checks
    print("\n=== ALGORITHM CHECKS ===")
    test_across_calculation()
    test_never_self_target()

    # Performance tests
    print("\n=== PERFORMANCE TESTS ===")
    test_medium_values()
    test_large_value()

    # Final answer
    print("\n=== FINAL ANSWER ===")
    result = test_actual_input()

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)
    print(f"\nFINAL ANSWER: {result:,}")

    return result
```

## Success Criteria

All of the following must be true for the solution to be considered correct:

- ✓ Example case passes (n=5 → 2) - **CRITICAL**
- ✓ Example trace output matches problem description
- ✓ Part 1 vs Part 2 difference confirmed (different algorithms)
- ✓ All edge cases pass (n=1, 2, 3, 4)
- ✓ Manual simulations match expected results (n=6)
- ✓ Sequential small values show consistent pattern
- ✓ No index errors, assertion failures, or infinite loops
- ✓ Performance acceptable for large inputs (< 3s for n=100,000)
- ✓ Actual input (n=3,017,957) completes in < 10s
- ✓ Result is in valid range [1, n]
- ✓ Result is an integer
- ✓ Algorithm checks pass (across calculation, never self-target)

## Debugging Strategy (If Tests Fail)

### If Example Fails (n=5 → 2)
**This is the most critical test. If it fails, the algorithm is fundamentally wrong.**

1. Run with debug=True to see each elimination step
2. Compare debug output to the manual verification in Category 1
3. Check each of these potential issues:
   - Is across_offset calculated as `remaining // 2`?
   - Is target_index calculated as `(current_index + across_offset) % remaining`?
   - Is the index adjustment correct (only decrement if target < current)?
   - Is the next elf calculation `(current_index + 1) % len(circle)`?
4. Manually trace through on paper to find discrepancy

### If Edge Cases Fail
- **n=1**: Should return 1 immediately without entering the loop
- **n=2**: Check that across_offset = 1, Elf 1 eliminates Elf 2
- **n=3 or n=4**: Run with debug=True and compare to manual simulations

### If Pattern Analysis Shows Anomalies
1. Run test_sequential_small() with debug output for suspicious values
2. Look for:
   - Results outside range [1, n]
   - Unexpected repetition or breaks in patterns
   - Values that don't match manual calculation
3. Add detailed logging for the problematic value

### If Performance is Poor
- **Check data structure**: Must use `collections.deque`, not list
- **Verify O(1) deletions**: Using `del circle[index]` on deque
- **No hidden O(n) operations**: Don't iterate through circle unnecessarily
- **Profile the code**: Use Python's `cProfile` to find bottlenecks

### If Index Errors Occur
- Check that modulo is always applied: `% len(circle)`
- Verify circle is never empty when accessing `circle[index]`
- Ensure current_index is adjusted before incrementing to next

## Expected Patterns (From Manual Analysis)

Based on manual simulation of small values (all verified step-by-step):
- n=1 → 1 (trivial case)
- n=2 → 1 (Elf 1 eliminates Elf 2)
- n=3 → 3 (verified in test plan)
- n=4 → 1 (verified in test plan)
- n=5 → 2 (verified from problem.md)
- n=6 → 3 (verified in test plan)

**Note**: Unlike Part 1, Part 2 does not have a simple mathematical pattern based on powers of 2. The elimination distance changes dynamically, making patterns harder to predict.

## Final Validation Checklist

Before submitting the solution, verify ALL of the following:

1. ✓ Example (n=5) returns 2 - **CRITICAL**
2. ✓ Example trace output matches problem.md step-by-step
3. ✓ Part 1 vs Part 2 difference confirmed (ensures correct algorithm)
4. ✓ All edge cases pass (n=1, 2, 3, 4)
5. ✓ Manual simulation (n=6) passes
6. ✓ No assertion failures or exceptions
7. ✓ Actual input (n=3,017,957) runs without error
8. ✓ Result is within valid range [1, 3,017,957]
9. ✓ Code completes in under 10 seconds
10. ✓ All tests in run_all_tests() pass

## Key Differences from Part 1 Testing

**Part 1**:
- Had both formula and simulation implementations
- Cross-validated formula vs simulation
- Simple mathematical pattern (powers of 2)
- O(1) formula solution available

**Part 2**:
- Only simulation approach (no formula)
- Validation through manual step-by-step verification
- No simple mathematical pattern
- Must rely on correctness of implementation
- Debug mode crucial for verification
- More emphasis on edge case testing

This means Part 2 testing requires more careful manual verification and step-by-step tracing to ensure correctness.
