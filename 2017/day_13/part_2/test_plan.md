# Test Plan - Part 2: Firewall Packet Scanner

## Testing Objectives
1. Verify the solution correctly finds the minimum delay to pass through firewall safely
2. Validate scanner position calculations with delay parameter
3. Ensure edge cases are handled properly
4. Confirm the solution works for both example and actual input

## Test Strategy Overview
- **Unit tests**: Test individual functions (is_caught with delay, parse_input)
- **Integration tests**: Test full delay-finding algorithm
- **Example validation**: Verify against known example from problem statement
- **Final validation**: Run on actual input and verify answer

## Test Cases

### Test 1: Example from Problem Statement
**Objective**: Validate against the provided example

**Input**:
```
0: 3
1: 2
4: 4
6: 4
```

**Expected Output**: `10`

**Verification Steps**:
1. Create a test file with the example input
2. Run the solution
3. Verify output is exactly `10`

**Why this works**:
- With delay=10, packet enters layers at times: 10, 11, 14, 16
- Layer 0: range=3, period=4, time=10, 10%4=2 ≠ 0 ✓
- Layer 1: range=2, period=2, time=11, 11%2=1 ≠ 0 ✓
- Layer 4: range=4, period=6, time=14, 14%6=2 ≠ 0 ✓
- Layer 6: range=4, period=6, time=16, 16%6=4 ≠ 0 ✓
- All safe, so delay=10 works

**Manual check for delays 0-9** (to verify they don't work):
- delay=0: Layer 0 time=0, 0%4=0 → caught ✗
- delay=1: Layer 1 time=2, 2%2=0 → caught ✗
- delay=2: Layer 0 time=2, 2%4=2 ✓; Layer 1 time=3, 3%2=1 ✓; Layer 4 time=6, 6%6=0 → caught ✗
- delay=3: Layer 1 time=4, 4%2=0 → caught ✗
- delay=4: Layer 0 time=4, 4%4=0 → caught ✗
- delay=5: Layer 1 time=6, 6%2=0 → caught ✗
- delay=6: Layer 0 time=6, 6%4=2 ✓; Layer 1 time=7, 7%2=1 ✓; Layer 4 time=10, 10%6=4 ✓; Layer 6 time=12, 12%6=0 → caught ✗
- delay=7: Layer 1 time=8, 8%2=0 → caught ✗
- delay=8: Layer 0 time=8, 8%4=0 → caught ✗
- delay=9: Layer 1 time=10, 10%2=0 → caught ✗

**Automated verification** (preferred method):
```python
# Verify that delays 0-9 all result in at least one catch
for d in range(10):
    assert not verify_delay(layers, d), f"delay={d} should not work"
# Verify that delay=10 works
assert verify_delay(layers, 10), "delay=10 should work"
```

### Test 2: Scanner Position Calculation with Delay
**Objective**: Verify the is_caught() function works correctly with delay parameter

**Test Cases**:

#### Test 2a: Basic calculation
```python
depth = 0, range = 3, delay = 0
period = 2 * (3-1) = 4
time = 0 + 0 = 0
0 % 4 == 0 → should return True (caught)
```

#### Test 2b: Safe passage with delay
```python
depth = 0, range = 3, delay = 1
period = 4
time = 0 + 1 = 1
1 % 4 == 1 → should return False (safe)
```

#### Test 2c: Different depth
```python
depth = 6, range = 4, delay = 0
period = 2 * (4-1) = 6
time = 6 + 0 = 6
6 % 6 == 0 → should return True (caught)
```

#### Test 2d: Different depth with delay
```python
depth = 6, range = 4, delay = 2
period = 6
time = 6 + 2 = 8
8 % 6 == 2 → should return False (safe)
```

**Verification Method**:
- Create a simple test script that calls is_caught() with these parameters
- Print results and compare with expected values
- All should match expected behavior

### Test 3: Edge Case - range = 1
**Objective**: Verify handling of scanners that never move

**Input**: Layer with range=1 (e.g., "5: 1")

**Expected Behavior**:
- is_caught(5, 1, any_delay) should always return True
- If input contains ANY layer with range=1, no delay will work
- The algorithm will run indefinitely (this is expected behavior given input constraints)

**Verification**:
1. Check actual input.md for any "X: 1" entries
2. Looking at input.md, smallest range is 2, so this shouldn't be an issue
3. If needed, we could add a pre-check to warn about impossible cases

### Test 4: Edge Case - depth = 0
**Objective**: Verify first layer is handled correctly

**Test Case**:
```python
depth = 0, range = 4, delay = 3
period = 6
time = 0 + 3 = 3
3 % 6 == 3 → should return False (safe)
```

**Verification**: Confirm first layer in actual input (0: 3) works correctly with various delays

### Test 5: Multiple Layers at Different Delays
**Objective**: Verify that a delay must work for ALL layers simultaneously

**Custom Test Input**:
```
0: 2
2: 3
```

**Analysis**:
- Layer 0: period=2, need (delay+0) % 2 ≠ 0 → delay must be odd
- Layer 2: period=4, need (delay+2) % 4 ≠ 0 → delay+2 must not be multiple of 4

**Check delays**:
- delay=0: 0%2=0 → caught at layer 0 ✗
- delay=1: 1%2=1 ✓, (1+2)%4=3 ✓ → SAFE!

**Expected**: Minimum delay should be 1

**Verification Method**:
- Option 1: Create a file `test_custom.md` with this input and run the solution with modified filename
- Option 2 (preferred): Create a unit test that directly calls `find_minimum_delay()` with these layers:
```python
custom_layers = [(0, 2), (2, 3)]
result = find_minimum_delay(custom_layers)
assert result == 1, f"Expected 1, got {result}"
```

### Test 6: Actual Input Validation
**Objective**: Solve the actual puzzle input

**Input**: input.md (44 layers)

**Verification Steps**:
1. Run solution on actual input.md
2. Record the computed minimum delay (let's call it `answer`)
3. **Automated verification** (preferred over manual spot-checking):
```python
def verify_delay(layers, delay):
    """Returns True if delay allows safe passage through all layers"""
    for depth, range_val in layers:
        if is_caught(depth, range_val, delay):
            return False
    return True

# Verify the answer works
assert verify_delay(layers, answer) == True, "Answer should allow safe passage"

# Verify minimality (answer-1 should not work)
assert verify_delay(layers, answer - 1) == False, "Answer-1 should result in at least one catch"
```
4. Performance check: Should complete in reasonable time (< 1 minute preferred)

**Success Criteria**:
- Solution completes without errors
- Returns a positive integer
- Automated verification confirms the delay works for all 44 layers
- Automated verification confirms previous delay (answer-1) would cause at least one catch
- This proves both correctness and minimality

### Test 7: Performance Test
**Objective**: Ensure solution runs efficiently

**Test Method**:
1. Measure execution time on actual input
2. Monitor progress output (if implemented)
3. Count number of delays checked before finding answer

**Expected Performance**:
- **Acceptable**: Completes in under 1 minute
- **Good**: Completes in under 30 seconds
- **Needs optimization**: Takes longer than 5 minutes
- If answer is around 10,000-100,000, checking ~44 layers per delay is very fast
- If answer is in millions, may take longer but should still be manageable

**Monitoring**:
- Progress output should show current delay being checked (every 10,000 iterations)
- This helps estimate completion time and verify the solution is not stuck
- If too slow (> 5 minutes), consider optimizations from implementation plan

**Decision Point**:
- If runtime < 1 minute: Solution is acceptable, no optimization needed
- If runtime 1-5 minutes: Solution works, optimization optional
- If runtime > 5 minutes: Consider implementing optimizations

### Test 8: Parse Input Validation
**Objective**: Verify input parsing works correctly

**Verification**:
1. Count number of layers parsed from input.md
2. Verify first layer: (0, 3)
3. Verify last layer: (96, 26)
4. Confirm total layers = 44

**Method**:
```python
layers = parse_input('input.md')
print(f"Total layers: {len(layers)}")
print(f"First layer: {layers[0]}")
print(f"Last layer: {layers[-1]}")
```

**Expected Output**:
```
Total layers: 44
First layer: (0, 3)
Last layer: (96, 26)
```

## Testing Execution Order

1. **First**: Test 8 (Parse Input) - Ensure we're reading data correctly
2. **Second**: Test 2 (is_caught function) - Validate core logic
3. **Third**: Test 1 (Example) - Verify against known answer
4. **Fourth**: Test 5 (Multiple layers) - Verify all-layers logic
5. **Fifth**: Tests 3, 4 (Edge cases) - Ensure robustness
6. **Finally**: Test 6 & 7 (Actual input + performance) - Get the answer

## Validation Checklist

- [ ] Example input produces correct output (10)
- [ ] Automated verification confirms delays 0-9 don't work for example
- [ ] is_caught() function works with delay parameter (Test 2)
- [ ] Parsing extracts correct number of layers (44)
- [ ] First layer (0, 3) and last layer (96, 26) parsed correctly
- [ ] Edge cases handled (range=1 if present, depth=0)
- [ ] Actual input runs without errors
- [ ] Performance is acceptable (< 1 minute)
- [ ] Automated verification confirms final answer allows safe passage through all layers
- [ ] Automated verification confirms answer-1 would cause at least one catch

## Expected Final Answer
The final answer for the actual input will be a positive integer representing the minimum delay in picoseconds. This should be submitted as the solution to Part 2 of the puzzle.

## Debugging Strategy (If Tests Fail)

### If example test fails:
1. Print scanner positions at each time step for delay=10
2. Manually trace packet journey
3. Verify period calculations
4. Check modulo arithmetic

### If actual input gives wrong answer:
1. Run automated verification to see if answer actually works
2. If verification fails, add debug output showing which layer catches packet
3. Use automated checks for delays near the computed answer (answer-5 to answer+5)
4. Check for off-by-one errors in time calculation
5. Verify delay is being applied correctly (delay+depth, not depth+delay)
6. Use the verification function to systematically test delays

### If performance is too slow (> 5 minutes):
1. Check progress output to estimate completion time
2. If answer will be extremely large, consider optimizations
3. Verify early termination is working (breaks out of loop on first catch)
4. Consider implementing optimizations from implementation plan:
   - Step size intelligence
   - Pre-filtering
   - More advanced algorithms (CRT)

## Success Criteria Summary
All tests pass, example produces 10, actual input produces a valid answer in reasonable time (< 1 minute), and automated verification confirms both correctness (answer works) and minimality (answer-1 doesn't work).

## Additional Test: Empty/Malformed Input (Optional)
While the puzzle input is guaranteed to be well-formed, for robustness:

**Test Case**: Empty input file
- Expected: Should return delay=0 (no layers to avoid)

**Test Case**: Malformed line (e.g., "invalid data")
- Expected: Should raise appropriate error or skip invalid lines

**Note**: These tests are optional since we're writing a script for a specific, known input format, not a production system.
