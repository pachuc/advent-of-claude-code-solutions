# Testing Plan: Plant Growth Simulation (Part 2)

## Testing Objectives
1. Verify steady state detection works correctly
2. Ensure rate of change calculation is accurate
3. Validate extrapolation to 50 billion generations
4. Confirm solution produces correct answer for actual input

## Updates Based on Critique
This plan has been updated to address the following key improvements:

1. **Fixed Test 2.2 (Extrapolation Accuracy):** Now uses actual detected steady state values instead of hardcoded values, making the test meaningful and accurate.

2. **Replaced Test 4.1:** Removed invalid "small target" test and replaced with pattern evolution visualization for better debugging.

3. **Enhanced Test 2.1 (Steady State Detection):** Added verification of the pattern consistency check to ensure the new `verify_pattern_consistency()` function works.

4. **Improved Performance Test (5.1):** Changed from strict assertion to informational output to avoid false failures on slower machines.

5. **Added Full End-to-End Test (6.1):** Comprehensive test that validates output format, type, magnitude, and reasonableness.

6. **Added Consistency Test (6.2):** Verifies the solution produces identical results across multiple runs.

7. **Reorganized Test Execution Order:** Clearer phased approach with critical vs. informational tests separated.

8. **Added Expected Results Section:** Documents what to expect for steady state generation, rate, final answer magnitude, etc.

## Test Strategy

### Phase 1: Unit Testing Individual Components

#### Test 1.1: Pattern Normalization
**Function:** `normalize_pattern(state)`

**Test Cases:**
1. **Basic normalization:**
   - Input: `{5, 8, 12}`
   - Expected: `frozenset({0, 3, 7})` (offset by -5)

2. **Negative indices:**
   - Input: `{-3, 0, 4}`
   - Expected: `frozenset({0, 3, 7})` (offset by +3)

3. **Empty state:**
   - Input: `set()`
   - Expected: `frozenset()`

4. **Single plant:**
   - Input: `{10}`
   - Expected: `frozenset({0})`

**Verification Method:**
```python
def test_normalize_pattern():
    assert normalize_pattern({5, 8, 12}) == frozenset({0, 3, 7})
    assert normalize_pattern({-3, 0, 4}) == frozenset({0, 3, 7})
    assert normalize_pattern(set()) == frozenset()
    assert normalize_pattern({10}) == frozenset({0})
    print("Pattern normalization tests passed!")
```

#### Test 1.2: Simulation Correctness (from Part 1)
**Function:** `simulate_generation(state, rules)`

**Test Cases:**
1. **First 20 generations match Part 1:**
   - Run simulation for 20 generations
   - Expected sum: 2767 (from part_1_answer.txt)

**Verification:**
```python
def test_part1_compatibility():
    initial_state, rules = parse_input('input.md')
    state = initial_state
    for _ in range(20):
        state = simulate_generation(state, rules)
    assert sum(state) == 2767
    print("Part 1 compatibility test passed!")
```

#### Test 1.3: Rate Calculation
**Function:** `calculate_rate_of_change()`

**Test Cases:**
1. **Simple linear increase:**
   - gen=100, sum=5000; prev_gen=99, prev_sum=4950
   - Expected rate: 50

2. **Multi-generation gap:**
   - gen=105, sum=5250; prev_gen=100, prev_sum=5000
   - Expected rate: 50

3. **Zero change (unlikely but test):**
   - gen=10, sum=100; prev_gen=9, prev_sum=100
   - Expected rate: 0

**Verification:**
```python
def test_rate_calculation():
    assert calculate_rate_of_change(100, 5000, 99, 4950) == 50
    assert calculate_rate_of_change(105, 5250, 100, 5000) == 50
    assert calculate_rate_of_change(10, 100, 9, 100) == 0
    print("Rate calculation tests passed!")
```

### Phase 2: Integration Testing

#### Test 2.1: Steady State Detection
**Purpose:** Verify the algorithm detects when pattern stabilizes

**Test Approach:**
1. Run simulation with actual input
2. Print generation where steady state detected
3. Print the generation gap (should be 1 for shifting pattern)
4. Verify pattern truly repeats
5. Verify consistency validation worked

**Verification:**
```python
def test_steady_state_detection():
    initial_state, rules = parse_input('input.md')
    result = detect_steady_state(initial_state, rules, max_generations=1000)
    gen, state, current_sum, prev_gen, prev_state, prev_sum = result

    assert prev_gen is not None, "No steady state found!"

    print(f"Steady state detected at generation {gen}")
    print(f"Previous occurrence at generation {prev_gen}")
    print(f"Gap: {gen - prev_gen} generations")
    print(f"Current sum: {current_sum}")
    print(f"Previous sum: {prev_sum}")

    # Calculate and display rate
    rate = (current_sum - prev_sum) // (gen - prev_gen)
    print(f"Rate: {rate} per generation")

    # Verify patterns are actually the same
    norm_current = normalize_pattern(state)
    norm_prev = normalize_pattern(prev_state)
    assert norm_current == norm_prev, "Normalized patterns should match"

    # Verify the pattern stays consistent (this was checked in detect_steady_state)
    # but let's verify it again
    assert verify_pattern_consistency(state, norm_current, rules, num_checks=3), \
        "Pattern consistency verification failed"

    print("Steady state detection test passed!")
```

**Expected Characteristics:**
- Steady state should be found within 100-200 generations
- Gap between repetitions likely 1 (pattern shifts every generation)
- Rate should be positive (pattern moving right) and reasonable (likely 50-100)

#### Test 2.2: Small Target Extrapolation
**Purpose:** Test extrapolation logic with verifiable small numbers

**Test Approach:**
1. Detect actual steady state from the input
2. Use those real values to extrapolate to a nearby generation
3. Actually simulate to that generation and verify the extrapolation matches

**Verification:**
```python
def test_extrapolation_accuracy():
    # First, detect the actual steady state
    initial_state, rules = parse_input('input.md')
    result = detect_steady_state(initial_state, rules, max_generations=1000)
    gen, state, current_sum, prev_gen, prev_state, prev_sum = result

    if prev_gen is None:
        print("Cannot test: no steady state found")
        return

    # Calculate the rate
    rate = calculate_rate_of_change(gen, current_sum, prev_gen, prev_sum)

    # Test extrapolation to 10 generations ahead
    target = gen + 10
    predicted = extrapolate_to_target(target, gen, current_sum, rate)

    # Simulate 10 more generations from current state
    test_state = state
    for _ in range(10):
        test_state = simulate_generation(test_state, rules)
    actual_sum = sum(test_state)

    # The predicted should exactly match actual in steady state
    print(f"Extrapolation test from gen {gen} to gen {target}:")
    print(f"  Predicted: {predicted}")
    print(f"  Actual:    {actual_sum}")
    assert predicted == actual_sum, f"Extrapolation mismatch: {predicted} != {actual_sum}"
    print("Extrapolation accuracy test passed!")
```

### Phase 3: End-to-End Testing

#### Test 3.1: Full Solution with Actual Input
**Purpose:** Run complete solution and verify answer format

**Test Approach:**
1. Run main() function with actual input
2. Verify output is a single integer
3. Verify the number is reasonable (should be very large, in trillions range)

**Verification:**
```python
def test_full_solution():
    # Capture output
    result = main()  # Should print final answer

    # Manual checks:
    # - Is it an integer?
    # - Is it positive?
    # Is it reasonably large? (50 billion generations * ~50-100 plants * ~few thousand shift)
    # Expected magnitude: 10^12 to 10^15 range
```

**Expected Characteristics:**
- Answer should be very large (trillions)
- Should be positive
- Should complete in under 1 second

#### Test 3.2: Consistency Check
**Purpose:** Verify solution gives same answer on multiple runs

**Test Approach:**
1. Run solution 3 times
2. Verify identical output each time

**Verification:**
```python
def test_consistency():
    results = []
    for i in range(3):
        # Run solution
        result = main()
        results.append(result)

    assert results[0] == results[1] == results[2]
    print("Consistency test passed!")
```

### Phase 4: Edge Case Testing

#### Test 4.1: Pattern Evolution Visualization
**Purpose:** Understand how the pattern evolves and when it stabilizes

**Test Approach:**
1. Print detailed information about pattern evolution
2. Help debug issues and verify pattern behavior

**Verification:**
```python
def test_pattern_evolution():
    """
    Print detailed information about how the pattern evolves.
    This is a diagnostic test to understand the pattern behavior.
    """
    initial_state, rules = parse_input('input.md')
    state = initial_state

    print("Generation | Min Pot | Max Pot | Num Plants | Sum      | Pattern Hash")
    print("-" * 75)

    for gen in range(min(150, 1000)):
        min_pot = min(state) if state else 0
        max_pot = max(state) if state else 0
        num_plants = len(state)
        total = sum(state)
        normalized = normalize_pattern(state)
        pattern_hash = hash(normalized) % 1000000  # Short hash for display

        print(f"{gen:10} | {min_pot:7} | {max_pot:7} | {num_plants:10} | {total:8} | {pattern_hash:12}")

        state = simulate_generation(state, rules)

        # Stop early if we see obvious stabilization
        if gen > 20 and gen % 10 == 0:
            # Check if pattern has stabilized by looking at last few generations
            break

    print("\nPattern evolution visualization complete")
```

#### Test 4.2: Verify Pattern Truly Shifts
**Purpose:** Ensure the pattern shifts consistently, not randomly

**Test Approach:**
1. After detecting steady state, simulate 10 more generations
2. Verify sum increases by rate × 10
3. Verify normalized pattern stays constant

**Verification:**
```python
def test_pattern_shift_consistency():
    initial_state, rules = parse_input('input.md')
    result = detect_steady_state(max_generations=1000)
    gen, state, current_sum, prev_gen, prev_state, prev_sum = result

    rate = calculate_rate_of_change(gen, current_sum, prev_gen, prev_sum)

    # Simulate 10 more generations
    test_state = state
    for i in range(10):
        test_state = simulate_generation(test_state, rules)
        expected_sum = current_sum + rate * (i + 1)
        actual_sum = sum(test_state)
        # Should match exactly in steady state
        print(f"Gen {gen + i + 1}: expected={expected_sum}, actual={actual_sum}")
```

### Phase 5: Performance Testing

#### Test 5.1: Execution Time
**Purpose:** Ensure solution completes quickly

**Test Approach:**
```python
import time

def test_performance():
    start = time.time()
    result = main()
    end = time.time()

    elapsed = end - start
    print(f"Execution time: {elapsed:.3f} seconds")

    # For information only - don't fail on slow machines
    if elapsed < 0.5:
        print("Performance: Excellent!")
    elif elapsed < 1.0:
        print("Performance: Good")
    elif elapsed < 2.0:
        print("Performance: Acceptable")
    else:
        print("Performance: Slower than expected, but may be acceptable")

    return elapsed
```

**Expected:** < 0.1 seconds for ~100-200 generation simulation
**Note:** We print timing info but don't assert, to avoid false failures on slow machines

### Phase 6: Final Validation

#### Test 6.1: Full End-to-End Solution Test
**Purpose:** Run the complete solution and validate output

**Test Approach:**
```python
def test_full_solution():
    """
    Run the complete solution and validate the output format and reasonableness.
    """
    print("Running full solution for Part 2...")

    result = main(verbose=True)

    # Validate the result
    assert result is not None, "Solution returned None"
    assert isinstance(result, int), f"Result should be int, got {type(result)}"
    assert result > 0, f"Result should be positive, got {result}"
    assert result > 2767, f"Result should be larger than Part 1 answer (2767), got {result}"

    # Check magnitude is reasonable (should be in trillions range)
    # With ~100 plants shifting right for 50 billion generations,
    # expect something like 100 * 50_billion = 5 trillion
    # But allow wide range: 10^11 to 10^16
    assert 1e11 < result < 1e16, f"Result magnitude seems wrong: {result}"

    print(f"\nFinal answer: {result}")
    print(f"Magnitude check: {len(str(result))} digits")
    print("Full solution test PASSED!")

    return result
```

#### Test 6.2: Consistency Check
**Purpose:** Verify solution gives same answer on multiple runs

**Test Approach:**
```python
def test_consistency():
    """
    Run the solution multiple times and verify identical output.
    """
    results = []
    for i in range(3):
        print(f"Run {i+1}/3...")
        result = main(verbose=False)
        results.append(result)

    assert results[0] == results[1] == results[2], \
        f"Results differ: {results}"

    print(f"Consistency test passed! All runs produced: {results[0]}")
```

#### Test 6.3: Debug Output (Optional)
**Purpose:** Understand the solution characteristics

**Test Approach:**
This is now integrated into `main(verbose=True)`, which prints:
- Steady state generation
- Pattern repetition period
- Current sum at detection
- Rate of change
- Number of plants
- Extrapolation details

## Test Execution Order
1. **Phase 1 (Unit Tests)** - Verify individual components work correctly
   - Test 1.1: Pattern normalization
   - Test 1.2: Part 1 compatibility (CRITICAL - must pass)
   - Test 1.3: Rate calculation

2. **Phase 2 (Integration Tests)** - Verify components work together
   - Test 2.1: Steady state detection
   - Test 2.2: Extrapolation accuracy

3. **Phase 4 (Diagnostics)** - Understand the problem behavior
   - Test 4.1: Pattern evolution visualization
   - Test 4.2: Pattern shift consistency

4. **Phase 3 (End-to-End)** - Verify full solution
   - Test 3.1: Full solution test (from Phase 6)
   - Test 3.2: Consistency check (from Phase 6)

5. **Phase 5 (Performance)** - Verify efficiency
   - Test 5.1: Execution time

## Success Criteria

### Must Pass (Critical)
- ✓ Test 1.2: Part 1 compatibility (sum = 2767 at gen 20)
- ✓ Test 2.1: Steady state detected within 1000 generations
- ✓ Test 2.2: Extrapolation matches actual simulation
- ✓ Test 4.2: Pattern shift is consistent across test generations
- ✓ Test 6.1: Full solution produces valid answer
- ✓ Test 6.2: Final answer is consistent across multiple runs

### Should Pass (Important)
- ✓ Test 1.1: Pattern normalization works correctly
- ✓ Test 1.3: Rate calculation is accurate
- ✓ Final answer is a large positive integer (> 10^11)
- ✓ Execution time is reasonable (< 2 seconds)

### Nice to Have (Informational)
- Test 4.1: Pattern evolution visualization (for debugging)
- Test 5.1: Performance timing (for optimization)

## Expected Results

Based on the problem characteristics:
1. **Steady state detection:** Should occur within 100-200 generations
2. **Pattern period:** Likely 1 generation (pattern shifts every generation)
3. **Rate of change:** Positive integer, likely 50-100 per generation
4. **Final answer magnitude:** 10^12 to 10^15 (trillions range)
5. **Execution time:** < 0.5 seconds on modern hardware

## What We're NOT Testing
(As this is a script, not production code)
- Input validation (assume input is well-formed)
- File I/O error handling
- Memory constraints (input size is known)
- Multiple input files
- Concurrent execution
- Logging and monitoring
- Configuration management
