# Testing Plan: Reindeer Race Simulation

## Testing Strategy Overview

We need to verify:
1. Input parsing works correctly
2. Distance calculation is mathematically correct
3. Edge cases are handled properly
4. The solution produces the correct answer for the given input

**Note**: This is a script to solve a specific problem, not production code. Tests focus on correctness of the core algorithm and validation against known examples, without over-engineering test infrastructure.

## Test Categories

### 1. Unit Tests - Input Parsing

**Test 1.1: Parse Single Reindeer**
- **Input**: `"Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."`
- **Expected**: `("Comet", 14, 10, 127)`
- **Purpose**: Verify basic parsing works

**Test 1.2: Parse Multiple Reindeer**
- **Input**: The full input.md file (9 reindeer)
- **Expected**: List of 9 tuples with correct values
- **Verification**:
  - Check length = 9
  - Spot check: First line → ("Dancer", 27, 5, 132)
  - Spot check: Last line → ("Vixen", 18, 5, 84)

**Test 1.3: Parse with Varying Spacing**
- **Purpose**: Ensure parser is robust to whitespace variations
- **Note**: For this script, we assume input is well-formed, so this is lower priority

### 2. Unit Tests - Distance Calculation

**Test 2.1: Example Validation (Comet at 1000s)**
- **Input**: speed=14, fly_time=10, rest_time=127, total_time=1000
- **Expected**: 1120 km
- **Calculation**:
  - Cycle = 137s
  - Complete cycles = 1000 // 137 = 7
  - Remainder = 1000 % 137 = 41s
  - Distance = 7×10×14 + min(41,10)×14 = 980 + 140 = 1120
- **Purpose**: Verify against known example from problem statement

**Test 2.2: Example Validation (Dancer at 1000s)**
- **Input**: speed=16, fly_time=11, rest_time=162, total_time=1000
- **Expected**: 1056 km
- **Calculation**:
  - Cycle = 173s
  - Complete cycles = 1000 // 173 = 5
  - Remainder = 1000 % 173 = 135s
  - Distance = 5×11×16 + min(135,11)×16 = 880 + 176 = 1056
- **Purpose**: Verify against known example from problem statement

**Test 2.3: Exact Cycle Boundary**
- **Input**: speed=10, fly_time=5, rest_time=5, total_time=100
- **Expected**: 500 km
- **Calculation**:
  - Cycle = 10s
  - Complete cycles = 100 // 10 = 10
  - Remainder = 0
  - Distance = 10×5×10 + 0 = 500
- **Purpose**: Verify no off-by-one errors when time is exact multiple of cycle

**Test 2.4: Race Ends During Flying**
- **Input**: speed=10, fly_time=10, rest_time=5, total_time=12
- **Expected**: 100 km
- **Calculation**:
  - Cycle = 15s
  - Complete cycles = 0
  - Remainder = 12s
  - Flying portion = min(12, 10) = 10s (reindeer flies for first 10s, then starts resting at 11s)
  - Distance = 0 + 10×10 = 100 km
- **Purpose**: Verify remainder calculation when race ends during flying phase

**Test 2.5: Race Ends During Resting**
- **Input**: speed=10, fly_time=5, rest_time=10, total_time=12
- **Expected**: 50 km
- **Calculation**:
  - Cycle = 15s
  - Complete cycles = 0
  - Remainder = 12s
  - Distance = 0 + min(12,5)×10 = 50
- **Purpose**: Verify remainder calculation when race ends during rest phase

**Test 2.6: Single Incomplete Cycle**
- **Input**: speed=20, fly_time=10, rest_time=5, total_time=7
- **Expected**: 140 km
- **Calculation**:
  - Cycle = 15s
  - Complete cycles = 0
  - Remainder = 7s
  - Distance = min(7,10)×20 = 140
- **Purpose**: Verify calculation when race is shorter than one cycle

**Test 2.7: Zero Time**
- **Input**: speed=10, fly_time=5, rest_time=5, total_time=0
- **Expected**: 0 km
- **Purpose**: Edge case boundary condition

### 3. Integration Tests

**Test 3.1: Two Reindeer Race**
- **Input**:
  - Reindeer A: speed=10, fly_time=10, rest_time=5, time=100
  - Reindeer B: speed=5, fly_time=20, rest_time=5, time=100
- **Calculation**:
  - A: cycle=15, cycles=6, remainder=10, distance=6×10×10+min(10,10)×10=600+100=700
  - B: cycle=25, cycles=4, remainder=0, distance=4×20×5+0=400
- **Expected Winner**: A with 700 km
- **Purpose**: Verify max finding works correctly

**Test 3.2: Tie Scenario**
- **Input**:
  - Reindeer A: speed=10, fly_time=5, rest_time=5, time=100
  - Reindeer B: speed=10, fly_time=5, rest_time=5, time=100
- **Expected**: 500 km (both tie, either is acceptable)
- **Purpose**: Verify handling of ties (we just need max value)

### 4. System Tests - Full Solution

**Test 4.1: Example Input (1000 seconds)**
- **Input**: The example reindeer from problem (Comet and Dancer) at 1000 seconds
- **Expected**: 1120 km (Comet wins)
- **Purpose**: End-to-end validation against problem example

**Test 4.2: Actual Input (2503 seconds)**
- **Input**: The provided input.md with 9 reindeer at 2503 seconds
- **Expected**: Calculate manually for verification
- **Manual Calculation for each reindeer**:

1. **Dancer**: 27 km/s, 5s fly, 132s rest
   - Cycle: 137s, Cycles: 18, Remainder: 37s
   - Distance: 18×5×27 + min(37,5)×27 = 2430 + 135 = 2565 km

2. **Cupid**: 22 km/s, 2s fly, 41s rest
   - Cycle: 43s, Cycles: 58, Remainder: 9s
   - Distance: 58×2×22 + min(9,2)×22 = 2552 + 44 = 2596 km

3. **Rudolph**: 11 km/s, 5s fly, 48s rest
   - Cycle: 53s, Cycles: 47, Remainder: 12s
   - Distance: 47×5×11 + min(12,5)×11 = 2585 + 55 = 2640 km

4. **Donner**: 28 km/s, 5s fly, 134s rest
   - Cycle: 139s, Cycles: 18, Remainder: 1s
   - Distance: 18×5×28 + min(1,5)×28 = 2520 + 28 = 2548 km

5. **Dasher**: 4 km/s, 16s fly, 55s rest
   - Cycle: 71s, Cycles: 35, Remainder: 18s
   - Distance: 35×16×4 + min(18,16)×4 = 2240 + 64 = 2304 km

6. **Blitzen**: 14 km/s, 3s fly, 38s rest
   - Cycle: 41s, Cycles: 61, Remainder: 2s
   - Distance: 61×3×14 + min(2,3)×14 = 2562 + 28 = 2590 km

7. **Prancer**: 3 km/s, 21s fly, 40s rest
   - Cycle: 61s, Cycles: 41, Remainder: 2s
   - Distance: 41×21×3 + min(2,21)×3 = 2583 + 6 = 2589 km

8. **Comet**: 18 km/s, 6s fly, 103s rest
   - Cycle: 109s, Cycles: 22, Remainder: 105s
   - Distance: 22×6×18 + min(105,6)×18 = 2376 + 108 = 2484 km

9. **Vixen**: 18 km/s, 5s fly, 84s rest
   - Cycle: 89s, Cycles: 28, Remainder: 11s
   - Distance: 28×5×18 + min(11,5)×18 = 2520 + 90 = 2610 km

- **Expected Winner**: Rudolph with 2640 km
- **Purpose**: Verify solution against actual problem input

### 5. Edge Case Tests (Lower Priority)

**Note**: These tests involve unrealistic parameter values not present in the actual input. They verify mathematical correctness but are lower priority for a script solving a specific problem.

**Test 5.1: Very Long Fly Time**
- **Input**: speed=1, fly_time=10000, rest_time=1, total_time=2503
- **Expected**: 2503 km (never needs to rest)
- **Purpose**: Verify handling when fly_time > total_time
- **Priority**: Low (unrealistic scenario)

**Test 5.2: Very Long Rest Time**
- **Input**: speed=100, fly_time=1, rest_time=10000, total_time=2503
- **Expected**: 100 km (flies once, then rests)
- **Purpose**: Verify handling when rest_time causes very few cycles
- **Priority**: Low (unrealistic scenario)

**Test 5.3: Speed = 0**
- **Input**: speed=0, fly_time=10, rest_time=10, total_time=100
- **Expected**: 0 km
- **Purpose**: Verify handling of edge case (though unlikely in real input)
- **Priority**: Low (unrealistic scenario)

## Testing Execution Plan

### Phase 1: Core Unit Tests (Priority: HIGH)
1. Implement the `run_tests()` function with Tests 2.1-2.7
2. Run tests to verify distance calculation is correct
3. All tests must pass before proceeding to actual input
4. **Focus**: This validates the mathematical algorithm

### Phase 2: System Testing with Actual Input (Priority: HIGH)
1. Run against actual input (2503 seconds) with all 9 reindeer
2. Verify output is 2640 km (Rudolph wins)
3. **Focus**: This validates the complete solution

### Phase 3: Manual Verification (Priority: MEDIUM)
1. Manually calculate at least 3 reindeer distances (Rudolph, Dancer, Vixen)
2. Compare with program output to ensure correctness
3. Verify calculations in Test 4.2 are accurate
4. **Focus**: Independent verification of results

### Phase 4: Optional Tests (Priority: LOW)
1. Integration tests (3.1-3.2) - useful but not critical
2. Edge case tests (5.1-5.3) - unrealistic scenarios
3. Input parsing tests - only if issues arise
4. **Focus**: Additional confidence, but lower priority for a script

## Success Criteria

**Must Have (Required for Correctness)**:
- ✓ All core unit tests (2.1-2.7) pass
- ✓ Example case (1000s) produces 1120 km (Test 2.1: Comet)
- ✓ Actual input (2503s) produces 2640 km (Test 4.2: Rudolph wins)
- ✓ Manual calculation matches program output for at least 2 reindeer
- ✓ No runtime errors or exceptions

**Should Have (Quality Checks)**:
- ✓ Execution completes quickly (< 1 second expected with O(n) algorithm)
- ✓ Code is readable and well-documented
- ✓ Parser handles the given input correctly

**Nice to Have (Optional)**:
- Integration tests pass (if implemented)
- Edge case tests pass (if implemented)

## Testing Tools and Methods

- **Simple test harness**: Create a test function with assert statements
- **Print statements**: Add debug output to verify intermediate calculations
- **Manual calculation**: Use calculator to verify at least 3 reindeer independently
- **Comparison**: Cross-reference with problem's example (Comet and Dancer at 1000s)

## Simple Test Harness Structure

```python
def run_tests():
    """Run all test cases and verify correctness."""
    print("Running tests...")

    # Test 2.1: Comet at 1000s
    assert calculate_distance(14, 10, 127, 1000) == 1120, "Test 2.1 failed"
    print("✓ Test 2.1 passed: Comet at 1000s")

    # Test 2.2: Dancer at 1000s
    assert calculate_distance(16, 11, 162, 1000) == 1056, "Test 2.2 failed"
    print("✓ Test 2.2 passed: Dancer at 1000s")

    # Test 2.3: Exact cycle boundary
    assert calculate_distance(10, 5, 5, 100) == 500, "Test 2.3 failed"
    print("✓ Test 2.3 passed: Exact cycle boundary")

    # Test 2.4: Race ends during flying
    assert calculate_distance(10, 10, 5, 12) == 100, "Test 2.4 failed"
    print("✓ Test 2.4 passed: Race ends during flying")

    # Test 2.5: Race ends during resting
    assert calculate_distance(10, 5, 10, 12) == 50, "Test 2.5 failed"
    print("✓ Test 2.5 passed: Race ends during resting")

    # Test 2.6: Single incomplete cycle
    assert calculate_distance(20, 10, 5, 7) == 140, "Test 2.6 failed"
    print("✓ Test 2.6 passed: Single incomplete cycle")

    # Test 2.7: Zero time
    assert calculate_distance(10, 5, 5, 0) == 0, "Test 2.7 failed"
    print("✓ Test 2.7 passed: Zero time")

    print("\nAll unit tests passed!")

# Optionally run tests before main computation
if __name__ == '__main__':
    run_tests()
    main()
```

This simple test harness:
- Uses assert statements for validation
- Provides clear pass/fail feedback
- Focuses on the most important test cases (2.1-2.7)
- Can be easily commented out after verification
- No external testing framework required

## Improvements Based on Review

This testing plan has been refined with the following enhancements:

1. **Simple Test Harness**: Added a concrete `run_tests()` function with assert statements
2. **Prioritized Testing**: Clearly marked high-priority tests (core algorithm validation) vs low-priority tests (unrealistic edge cases)
3. **Structured Phases**: Organized testing into clear phases with priority levels
4. **Success Criteria**: Categorized into "Must Have", "Should Have", and "Nice to Have"
5. **Focused Approach**: Emphasizes testing what matters for the specific problem rather than over-engineering
6. **Clarified Test 2.4**: Removed confusing self-corrections and provided clear explanation
7. **Practical Testing**: Appropriate scope for a script solving a specific problem, not production code
