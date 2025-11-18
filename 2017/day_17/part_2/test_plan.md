# Test Plan: Spinlock Part 2 - Optimized Solution

## Testing Strategy Overview

Since we're optimizing from Part 1, our main goals are:
1. Verify the optimized algorithm produces correct results
2. Ensure it handles the 50 million iteration requirement efficiently
3. Validate against small test cases we can manually verify
4. Cross-check with Part 1 logic where applicable

## Test Categories

### 1. Correctness Verification Tests

#### Test 1.1: Small-Scale Verification (Step size = 3, N = 10)
**Purpose:** Manually verify the algorithm with a small example

**Method:**
- Run both naive (Part 1 style) and optimized approaches with same parameters
- Use small N value (like 10) to manually trace the execution
- Verify both produce the same answer

**Expected behavior:**
```
Step size: 3
Iterations: 10

Manual trace:
- Start: [0], pos=0
- Insert 1: pos=(0+3)%1=0, insert at 1 → [0,1], value_after_zero=1
- Insert 2: pos=(1+3)%2=0, insert at 1 → [0,2,1], value_after_zero=2
- Insert 3: pos=(1+3)%3=1, insert at 2 → [0,2,3,1], value_after_zero=2
- Insert 4: pos=(2+3)%4=1, insert at 2 → [0,2,4,3,1], value_after_zero=2
- Insert 5: pos=(2+3)%5=0, insert at 1 → [0,5,2,4,3,1], value_after_zero=5
- ... continue

Final value_after_zero should match actual buffer[1]
```

**Pass criteria:** Optimized solution returns same value as naive solution

#### Test 1.2: Cross-Validate with Part 1 Logic (Step size = 355, N = 2017)
**Purpose:** Ensure optimized approach works for Part 1 problem size

**Method:**
- Run optimized solution with Part 1 parameters (step_size=355, iterations=2017)
- Modify Part 1 naive solution to also output `buffer[1]` after all insertions:
  ```python
  # After line that finds value after 2017, add:
  print(f"Value at position 1: {buffer[1]}")
  ```
- Compare the value at position 1 from both implementations
- Both should agree on the value at position 1

**Pass criteria:** Value at position 1 matches between naive and optimized implementations

#### Test 1.3: Example from Problem (Step size = 3, N = 2017)
**Purpose:** Validate against the provided example in Part 1 problem

**Method:**
- Run with step_size=3, iterations=2017
- Check that position 1 has a reasonable value
- Can verify with small-scale manual buffer building if needed

**Pass criteria:** Solution runs without errors and produces an integer result

### 2. Edge Case Tests

#### Test 2.1: Step Size of 1
**Purpose:** Test minimal step size

**Method:**
- Run with step_size=1, iterations=100
- Trace first few insertions manually:
  - Insert 1: pos=(0+1)%1=0, insert at 1 → value_after_zero=1
  - Insert 2: pos=(1+1)%2=0, insert at 1 → value_after_zero=2
  - Insert 3: pos=(1+1)%3=2, insert at 3 → value_after_zero=2
  - Pattern should be predictable

**Pass criteria:** Returns correct value for position 1

#### Test 2.2: Large Step Size
**Purpose:** Test when step size > buffer length initially

**Method:**
- Run with step_size=1000, iterations=100
- Verify modulo operation handles wrapping correctly

**Pass criteria:** No errors, returns valid result

#### Test 2.3: Step Size Zero
**Purpose:** Edge case where step size is 0

**Method:**
- Run with step_size=0, iterations=100
- With step_size=0, current_pos always stays at previous insert_pos
- After first iteration: insert at position 1, then always insert at position 1
- Expected: value_after_zero should equal iterations (final value inserted)

**Pass criteria:** Returns the correct value (should be 100 for this test)

### 3. Performance Tests

#### Test 3.1: Timing for 50 Million Iterations
**Purpose:** Ensure solution completes in reasonable time

**Method:**
- Run with step_size=355, iterations=50_000_000 (actual problem input)
- Measure execution time
- Monitor memory usage

**Expected performance:**
- Time: < 30 seconds (ideally < 10 seconds)
- Memory: Constant (no growth with iterations)

**Pass criteria:** Completes successfully within time limit

#### Test 3.2: Memory Efficiency Check
**Purpose:** Verify O(1) space complexity

**Method:**
- Run with increasing iteration counts: 1M, 10M, 50M
- Memory usage should remain constant

**Pass criteria:** Memory doesn't scale with iteration count

### 4. Algorithm Correctness Tests

#### Test 4.1: Position 1 Update Tracking
**Purpose:** Verify we catch all insertions at position 1

**Method:**
- Add debug counter to track how many times position 1 is updated
- Run with step_size=3, N=10
- Based on manual trace (see section 5 of test plan):
  - Position 1 is updated at i=1, i=2, i=5
  - Expected update count: 3
- Verify the counter matches this expected value

**Pass criteria:** Update count equals 3 for step_size=3, N=10

#### Test 4.2: Final Position Verification
**Purpose:** Ensure current_pos is correctly maintained

**Method:**
- Track current_pos throughout execution
- Verify it stays within [0, buffer_len) bounds
- Check final current_pos is reasonable

**Pass criteria:** No position out of bounds

#### Test 4.3: Buffer Length Consistency
**Purpose:** Verify buffer_len increases correctly

**Method:**
- After N iterations, buffer_len should equal N+1
- Verify this invariant holds

**Pass criteria:** buffer_len == iterations + 1

### 5. Analytical Verification Test

#### Test 5.1: Step Size = 1 Pattern Verification
**Purpose:** Verify behavior with minimal step size using analytical reasoning

**Method:**
- Run with step_size=1, iterations=20
- With step_size=1, we step forward 1 position each time
- Track when insert_pos == 1 occurs
- Pattern: insert_pos == 1 when current_pos == 0, which happens when (prev_current_pos + 1) % buffer_len == 0
- This occurs when prev_current_pos == buffer_len - 1 (at the end of buffer)

**Pass criteria:** Value at position 1 is reasonable and algorithm completes without errors

### 6. Input/Output Tests

#### Test 6.1: Actual Problem Input (355)
**Purpose:** Solve the actual problem

**Method:**
- Run with input "355"
- Iterations = 50,000,000
- Verify output is a single integer

**Pass criteria:**
- Produces integer output
- Completes in reasonable time
- No errors or exceptions

#### Test 6.2: Input Parsing
**Purpose:** Verify input is read correctly

**Method:**
- Test with various valid inputs
- Ensure strip() removes whitespace

**Pass criteria:** Step size correctly parsed

## Test Execution Order

1. **Start with small-scale tests (1.1):** Build confidence with manual verification
2. **Cross-validate with Part 1 (1.2):** Ensure algorithm is correct
3. **Run edge cases (2.x):** Check robustness
4. **Verify algorithm logic (4.x):** Ensure implementation matches design
5. **Analytical verification (5.1):** Check step_size=1 pattern
6. **Performance test (3.1):** Confirm efficiency for 50M iterations
7. **Final problem input (6.1):** Get the answer

## Manual Verification for Test 4.1 (Step size = 3, N = 10)

To verify the update count for Test 4.1:

```
For step_size=3, N=10, tracking position 1 updates:

Initial: buffer=[0], pos=0, len=1, value_after_zero=0

i=1: pos=(0+3)%1=0, insert_pos=1 → UPDATE (count=1), value_after_zero=1
i=2: pos=(1+3)%2=0, insert_pos=1 → UPDATE (count=2), value_after_zero=2
i=3: pos=(1+3)%3=1, insert_pos=2 → no update
i=4: pos=(2+3)%4=1, insert_pos=2 → no update
i=5: pos=(2+3)%5=0, insert_pos=1 → UPDATE (count=3), value_after_zero=5
i=6: pos=(1+3)%6=4, insert_pos=5 → no update
i=7: pos=(5+3)%7=1, insert_pos=2 → no update
i=8: pos=(2+3)%8=5, insert_pos=6 → no update
i=9: pos=(6+3)%9=0, insert_pos=1 → UPDATE (count=4), value_after_zero=9
i=10: pos=(1+3)%10=4, insert_pos=5 → no update

Expected update count: 4
Expected final value_after_zero: 9
```

## Manual Verification Example (Step size = 3, N = 5)

Let's trace manually to verify our understanding:

```
Initial: buffer=[0], pos=0, len=1, value_after_zero=0

i=1:
  pos = (0+3)%1 = 0
  insert_pos = 1
  insert_pos == 1 → value_after_zero = 1
  buffer=[0,1], pos=1, len=2

i=2:
  pos = (1+3)%2 = 0
  insert_pos = 1
  insert_pos == 1 → value_after_zero = 2
  buffer=[0,2,1], pos=1, len=3

i=3:
  pos = (1+3)%3 = 1
  insert_pos = 2
  insert_pos != 1 → value_after_zero = 2 (unchanged)
  buffer=[0,2,3,1], pos=2, len=4

i=4:
  pos = (2+3)%4 = 1
  insert_pos = 2
  insert_pos != 1 → value_after_zero = 2 (unchanged)
  buffer=[0,2,4,3,1], pos=2, len=5

i=5:
  pos = (2+3)%5 = 0
  insert_pos = 1
  insert_pos == 1 → value_after_zero = 5
  buffer=[0,5,2,4,3,1], pos=1, len=6

Final: value_after_zero = 5
```

We can verify this by building the actual buffer and checking buffer[1] == 5.

## Success Criteria Summary

**The solution is correct if:**
1. It produces the same value at position 1 as the naive approach for small N
2. It completes 50 million iterations in < 30 seconds
3. It uses constant memory regardless of iteration count
4. It correctly handles edge cases (small/large step sizes)
5. It produces a valid integer output for the actual input (355)

**Red flags to watch for:**
- Execution time > 1 minute for 50M iterations
- Memory usage growing with iteration count
- Mismatch with naive approach for same parameters
- Position tracking errors (out of bounds)
- Incorrect final buffer_len (should be iterations + 1)
