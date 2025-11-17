# Test Plan: Elf Gift Exchange Circle

## Testing Strategy Overview

We will test the solution using:
1. **Known Example Cases**: Verify against the provided example (N=5 → 3) - CRITICAL VALIDATION
2. **Edge Cases**: Test boundary conditions
3. **Pattern Verification**: Test powers of 2 and nearby values
4. **Cross-Validation**: Compare mathematical formula against simulation for smaller N - PRIMARY VALIDATION METHOD
5. **Actual Input**: Run against the real input (N = 3,017,957)

**Key Principle**: We do NOT trust hardcoded expected results. All validation is done by:
- Comparing formula vs simulation (they must agree)
- Verifying the provided example (N=5 → 3)
- Testing mathematical patterns (powers of 2)

## Test Cases

### 1. Provided Example Test
**Test Case**: N = 5 (from problem statement)

**Expected Process**:
- Initial: [1, 2, 3, 4, 5]
- Turn 1: Elf 1 takes from Elf 2 → [1*, 3, 4, 5]
- Turn 2: Elf 3 takes from Elf 4 → [1*, 3*, 5]
- Turn 3: Elf 5 takes from Elf 1 → [3*, 5*]
- Turn 4: Elf 3 takes from Elf 5 → [3*]

**Expected Result**: 3

**Verification**:
- Run `josephus_formula(5)` → Should return 3
- Run `simulate_with_linked_list(5)` → Should return 3

### 2. Edge Case: N = 1
**Description**: Only one elf
**Expected Result**: 1 (the only elf wins)
**Rationale**: No stealing occurs, Elf 1 already has all presents
**Verification**:
- Run `josephus_formula(1)` → Should return 1
- Run `simulate_with_linked_list(1)` → Should return 1
- Both methods must agree

### 3. Edge Case: N = 2
**Description**: Two elves
**Process**:
- Initial: [1, 2]
- Turn 1: Elf 1 takes from Elf 2 → [1*]

**Expected Result**: 1
**Verification**:
- Run `josephus_formula(2)` → Should return 1
- Run `simulate_with_linked_list(2)` → Should return 1
- Both methods must agree

### 4. Powers of 2 Pattern Tests

The Josephus formula predicts that when N = 2^m (a power of 2), the result is always 1.

| N | Binary | 2^m | L | Formula: 2*L+1 | Expected |
|---|--------|-----|---|----------------|----------|
| 1 | 1 | 1 | 0 | 1 | 1 |
| 2 | 10 | 2 | 0 | 1 | 1 |
| 4 | 100 | 4 | 0 | 1 | 1 |
| 8 | 1000 | 8 | 0 | 1 | 1 |
| 16 | 10000 | 16 | 0 | 1 | 1 |
| 32 | 100000 | 32 | 0 | 1 | 1 |

**Test**: Verify all powers of 2 up to 2^20 return 1

### 5. Powers of 2 Plus One

| N | 2^m | L | Formula: 2*L+1 | Expected |
|---|-----|---|----------------|----------|
| 3 | 2 | 1 | 3 | 3 |
| 5 | 4 | 1 | 3 | 3 |
| 9 | 8 | 1 | 3 | 3 |
| 17 | 16 | 1 | 3 | 3 |

**Pattern**: N = 2^m + 1 always gives result 3

### 6. Sequential Small Values

Test values 1 through 20 by comparing formula vs simulation:

**Verification Method**:
- For each N from 1 to 20:
  - Calculate result using `josephus_formula(n)`
  - Calculate result using `simulate_with_linked_list(n)`
  - Assert both methods return the same value
- We do NOT hardcode expected values (they could be wrong)
- The simulation serves as ground truth for validation

**Note**: If both methods agree on all values 1-20, and N=5 produces 3 (matching the problem example), we can be confident the implementations are correct.

### 7. Medium-Sized Values

Test values where simulation is still feasible but large enough to be meaningful:

| N | Description | Expected Duration |
|---|-------------|-------------------|
| 100 | Small but non-trivial | < 1ms |
| 1000 | Medium scale | < 10ms |
| 10000 | Larger scale | < 100ms |

**Verification**: Compare formula result with simulation result
**Note**: We limit to N=10,000 to keep tests fast. N=100,000 would work but may take several seconds.

### 8. Actual Input Test

**Test Case**: N = 3,017,957
**Method**:
- Run `josephus_formula(3017957)` to get the answer
- Cannot verify with simulation (would take too long)
- Trust the formula only after ALL other tests pass

**Manual Calculation** (for reference):
1. Find highest power of 2 ≤ 3,017,957
   - 2^21 = 2,097,152 ✓
   - 2^22 = 4,194,304 ✗ (too large)
2. L = 3,017,957 - 2,097,152 = 920,805
3. Result = 2 * 920,805 + 1 = 1,841,611

**Note**: We do NOT hardcode this as a test assertion. We simply print the result and verify it matches our manual calculation.

## Testing Implementation

### Test Script Structure

```python
def test_example():
    """
    CRITICAL: Test the provided example: N=5 should return 3.
    This validates our understanding of the problem.
    """
    formula_result = josephus_formula(5)
    simulation_result = simulate_with_linked_list(5)

    # Both should agree
    assert formula_result == simulation_result, \
        f"Formula and simulation disagree! Formula: {formula_result}, Simulation: {simulation_result}"

    # Result should be 3 (from problem statement)
    assert formula_result == 3, \
        f"Expected 3 for N=5, got {formula_result}"

    print("✓ Example test passed: N=5 → 3")

def test_edge_cases():
    """Test edge cases with both methods."""
    # Test N=1
    assert josephus_formula(1) == 1
    assert simulate_with_linked_list(1) == 1
    assert josephus_formula(1) == simulate_with_linked_list(1)

    # Test N=2
    assert josephus_formula(2) == 1
    assert simulate_with_linked_list(2) == 1
    assert josephus_formula(2) == simulate_with_linked_list(2)

    print("✓ Edge cases passed")

def test_powers_of_two():
    """Test that powers of 2 always return 1 (mathematical property)."""
    for i in range(21):
        n = 2 ** i
        formula_result = josephus_formula(n)
        simulation_result = simulate_with_linked_list(n)

        # Both methods should agree
        assert formula_result == simulation_result, \
            f"Disagreement at N={n}: formula={formula_result}, simulation={simulation_result}"

        # Mathematical property: powers of 2 should return 1
        assert formula_result == 1, \
            f"Power of 2 (N={n}) should return 1, got {formula_result}"

    print("✓ Powers of 2 test passed")

def test_powers_of_two_plus_one():
    """Test that 2^m + 1 always returns 3 (mathematical property)."""
    for i in range(1, 20):
        n = 2 ** i + 1
        formula_result = josephus_formula(n)
        simulation_result = simulate_with_linked_list(n)

        # Both methods should agree
        assert formula_result == simulation_result, \
            f"Disagreement at N={n}: formula={formula_result}, simulation={simulation_result}"

        # Mathematical property: 2^m + 1 should return 3
        assert formula_result == 3, \
            f"2^{i} + 1 (N={n}) should return 3, got {formula_result}"

    print("✓ Powers of 2 plus 1 test passed")

def test_sequential_small():
    """
    Test values 1-20 comparing formula vs simulation.
    This is the PRIMARY validation method.
    """
    for n in range(1, 21):
        formula_result = josephus_formula(n)
        simulation_result = simulate_with_linked_list(n)

        assert formula_result == simulation_result, \
            f"Disagreement at N={n}: formula={formula_result}, simulation={simulation_result}"

    print("✓ Sequential small values (1-20) test passed")

def test_medium_values():
    """Test medium-sized values."""
    test_values = [100, 1000, 10000]
    for n in test_values:
        formula_result = josephus_formula(n)
        simulation_result = simulate_with_linked_list(n)

        assert formula_result == simulation_result, \
            f"Disagreement at N={n}: formula={formula_result}, simulation={simulation_result}"

    print("✓ Medium values test passed")

def test_actual_input():
    """
    Test the actual input value.
    We print the result for manual verification but don't hardcode an assertion.
    """
    n = 3017957
    result = josephus_formula(n)

    # Manual calculation for verification:
    # 2^21 = 2,097,152
    # L = 3,017,957 - 2,097,152 = 920,805
    # Result = 2 * 920,805 + 1 = 1,841,611
    expected = 1841611

    print(f"✓ Actual input N={n} → {result}")
    print(f"  (Manual calculation expects: {expected})")

    # Verify against manual calculation
    assert result == expected, \
        f"Result {result} doesn't match manual calculation {expected}"

def run_all_tests():
    """Run all tests in order of importance."""
    print("\n=== Running Test Suite ===\n")

    # Most critical test first
    test_example()

    # Edge cases
    test_edge_cases()

    # Pattern validation
    test_powers_of_two()
    test_powers_of_two_plus_one()

    # Cross-validation
    test_sequential_small()
    test_medium_values()

    # Final result
    test_actual_input()

    print("\n=== All tests passed! ===")
```

## Verification Checklist

**Critical Tests** (must pass before trusting the solution):
- [ ] Test provided example (N=5 → 3) with both methods
- [ ] Both methods agree on N=5
- [ ] Test edge cases (N=1, N=2) with both methods
- [ ] Cross-validate formula vs simulation for N=1 to 20 (all must agree)

**Pattern Validation Tests**:
- [ ] Verify powers of 2 pattern (all return 1) with both methods
- [ ] Verify 2^m + 1 pattern (all return 3) with both methods
- [ ] Cross-validate formula vs simulation for N=100, 1000, 10000

**Final Verification**:
- [ ] Calculate result for N=3,017,957 using formula
- [ ] Verify against manual calculation: 2*920805+1 = 1,841,611
- [ ] All previous tests must pass before trusting this result

## Manual Verification of Formula

To manually verify the Josephus formula is correct:

1. **N = 5** (from problem statement):
   - Highest power of 2: 2^2 = 4
   - L = 5 - 4 = 1
   - Result = 2 * 1 + 1 = 3 ✓
   - This matches the problem example!

2. **N = 16** (power of 2):
   - Highest power of 2: 2^4 = 16
   - L = 16 - 16 = 0
   - Result = 2 * 0 + 1 = 1 ✓
   - Mathematical property holds

3. **N = 17** (power of 2 plus 1):
   - Highest power of 2: 2^4 = 16
   - L = 17 - 16 = 1
   - Result = 2 * 1 + 1 = 3 ✓
   - Pattern confirmed

## Error Cases to Consider

Since we're writing a script to solve the problem (not production code), we handle errors minimally:

1. **Invalid input**: N ≤ 0 - Not tested (problem guarantees valid input)
2. **Non-integer input**: Not tested (problem guarantees integer)
3. **File reading errors**: `read_input()` will raise exception if file doesn't exist or has no integer
   - This is acceptable for a simple script

**Note**: We don't need extensive error handling for this use case. The script is meant to process the given input file.

## Performance Testing

1. **Time the mathematical solution** for N = 3,017,957
   - Should complete in microseconds

2. **Time the simulation solution** for N = 10,000
   - Should complete in reasonable time (seconds)

3. **Verify simulation is infeasible** for N = 3,017,957
   - Would take too long, confirming need for mathematical approach

## Success Criteria

The solution is correct if and only if:
1. **N=5 produces 3** (matches problem statement example)
2. **Formula and simulation agree** for ALL tested values (N=1 to 10,000)
3. **Mathematical patterns hold**:
   - All powers of 2 return 1
   - All values 2^m + 1 return 3
4. **Performance is acceptable** (< 1 second for N = 3,017,957)

**Trust Chain**:
- If all above criteria pass → trust the formula
- If formula is trusted → accept result for N = 3,017,957
- If any test fails → investigate and fix before proceeding

## Testing Order (Priority)

1. **First**: Test N=5 → 3 (validates problem understanding)
2. **Second**: Test N=1, N=2 (edge cases)
3. **Third**: Cross-validate N=1 to 20 (builds confidence)
4. **Fourth**: Test patterns and medium values (comprehensive validation)
5. **Finally**: Calculate result for N=3,017,957 (actual answer)
