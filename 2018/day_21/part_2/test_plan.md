# Test Plan: Chronal Conversion Part 2

## Testing Objectives
1. Verify the program correctly detects cycles in the register 5 value sequence
2. Ensure we capture the last unique value before the cycle repeats
3. Validate that the solution is different from Part 1 (should be larger)
4. Confirm the algorithm doesn't have off-by-one errors

## Test Categories

### 1. Basic Functionality Tests

#### Test 1.1: Parse Input Correctly
**Purpose**: Ensure input parsing works (inherited from Part 1)

**Steps**:
1. Run the program on the provided `input.md`
2. Verify it parses IP register = 2
3. Verify it parses instructions correctly (should be > 0 instructions)

**Expected Result**: No parsing errors, correct IP register and instruction count

**Pass Criteria**: Program runs without exceptions during parsing and reports valid instruction count

---

#### Test 1.2: Instruction Execution Works
**Purpose**: Verify all opcodes execute correctly (inherited from Part 1)

**Steps**:
1. Program should execute without crashes
2. Should reach instruction 29 multiple times

**Expected Result**: No execution errors

**Pass Criteria**: Program completes without runtime exceptions

---

### 2. Algorithm Correctness Tests

#### Test 2.1: Cycle Detection Works
**Purpose**: Verify we correctly detect when a value repeats

**Steps**:
1. Run the program and observe the sequence tracking
2. Add debug output showing:
   - Number of unique values found
   - The value that triggered cycle detection (the first repeat)
   - The last unique value (our answer)

**Expected Result**:
- Program should find multiple unique values (likely hundreds to thousands)
- Should detect a repeated value
- Should return the value immediately before the repeat

**Pass Criteria**: Program terminates with a result

---

#### Test 2.2: Sequence Order Preservation
**Purpose**: Ensure we return the LAST unique value, not just any value

**Test Method**:
- Verify that `value_sequence[-1]` is used (last element)
- Check that the answer is NOT the first value (which would be Part 1's answer)

**Expected Result**:
- Answer ≠ 15615244 (Part 1 answer), unless the sequence has only 1 unique value (extremely unlikely)
- The answer can be any value in the sequence; it doesn't have to be larger than Part 1's answer

**Note**: The sequence order is determined by program logic, not numerical order. The last unique value could be smaller or larger than the first.

**Pass Criteria**: Result differs from Part 1 (unless sequence length is 1)

---

### 3. Edge Case Tests

#### Test 3.1: First Value Check
**Purpose**: Verify the first value matches Part 1's answer

**Steps**:
1. Add logging to capture the first value in the sequence
2. Compare to Part 1 answer (15615244)

**Expected Result**: First value in sequence should be 15615244

**Pass Criteria**: `value_sequence[0] == 15615244`

---

#### Test 3.2: No Premature Halting
**Purpose**: Ensure the program doesn't halt before finding the cycle

**Steps**:
1. Monitor the main loop condition
2. Ensure we reach instruction 29 many times (at least 2+)

**Expected Result**: Instruction 29 reached multiple times

**Pass Criteria**: `len(value_sequence) > 1`

---

#### Test 3.3: Set vs List Consistency
**Purpose**: Verify seen_values set and value_sequence list stay synchronized

**Test Method**:
- After completion, verify `len(seen_values) == len(value_sequence)`
- This ensures we didn't accidentally add duplicates to the list

**Expected Result**: Lengths match exactly

**Pass Criteria**: `len(seen_values) == len(value_sequence)`

---

### 4. Performance Tests

#### Test 4.1: Reasonable Runtime
**Purpose**: Ensure the program completes in acceptable time

**Steps**:
1. Time the execution using shell command: `time python solution.py`
2. Monitor for infinite loops
3. Observe progress indicators (should print every 10M instructions)

**Expected Result**: Completion within 10 minutes (estimated 30 seconds to 5 minutes based on implementation plan)

**Pass Criteria**: Program terminates with an answer within reasonable time

**Debug Actions if Fails**:
- Check that progress indicators are appearing
- Verify we're actually detecting cycles, not running infinitely
- Add more frequent progress output (every 1M instructions) to diagnose

---

#### Test 4.2: Memory Usage
**Purpose**: Ensure memory usage is reasonable

**Test Method**:
- Use `time -v python solution.py` on Linux to see maximum resident set size
- Alternatively, use Activity Monitor (macOS) or Task Manager (Windows) during execution
- Should not exceed 1 GB

**Expected Result**: Low memory usage (< 100 MB likely)

**Pass Criteria**: No out-of-memory errors, memory usage stays reasonable

---

### 5. Output Validation Tests

#### Test 5.1: Output Format
**Purpose**: Verify output is a single integer

**Steps**:
1. Run program
2. Check that final output is a non-negative integer

**Expected Result**: Single integer printed

**Pass Criteria**: Output can be parsed as int and is > 0

---

#### Test 5.2: Answer Sanity Check
**Purpose**: Verify answer is reasonable

**Checks**:
- Answer is a valid non-negative integer
- Answer ≠ Part 1 answer (15615244) unless sequence has only 1 value (extremely unlikely)
- Answer fits in a reasonable range (likely < 2^24 based on bitwise operations in program using 16777215 = 0xFFFFFF)

**Expected Result**: Reasonable integer value

**Pass Criteria**: Answer is a valid non-negative integer and differs from Part 1 answer

---

### 6. Debug and Diagnostic Tests

#### Test 6.1: Sequence Length Analysis
**Purpose**: Understand the sequence structure

**Add Diagnostic Output**:
```python
print(f"Total unique values found: {len(value_sequence)}")
print(f"First value (Part 1 answer): {value_sequence[0]}")
print(f"Last value (Part 2 answer): {value_sequence[-1]}")
print(f"Value that repeated: {current_value}")
```

**Purpose**: Help understand the problem structure and verify correctness

---

#### Test 6.2: Instruction 29 Hit Count
**Purpose**: Track how many times we evaluate the halting condition

**Add Counter**: Count times instruction 29 is reached

**Expected Result**: Should equal `len(value_sequence) + 1`
- The +1 accounts for the repeated value that triggers cycle detection
- This assumes we count the hit that detects the repeat before returning

**Note**: The exact count depends on when the counter increments relative to the cycle detection. The key is that it should be `len(value_sequence)` or `len(value_sequence) + 1`.

**Pass Criteria**: Counter is either `len(value_sequence)` or `len(value_sequence) + 1`

---

#### Test 6.3: First Repeat Detection
**Purpose**: Verify we stop at the first repeated value

**Test Method**:
- Log the value that triggers cycle detection (the repeated value)
- Verify this is the first value to appear twice in the sequence

**Expected Result**: The algorithm stops on the **first** repeated value, not some later repeat

**Note**: This is the correct behavior. Once any value repeats, we know the sequence is cycling, and the last unique value before that repeat is our answer.

**Pass Criteria**: Cycle detection triggers on first repeat

---

### 7. Regression Tests

#### Test 7.1: Part 1 Compatibility
**Purpose**: Ensure Part 1 logic still works with our codebase

**Steps**:
1. The first value in our sequence should match Part 1's answer
2. This validates that our simulation is correct

**Expected Result**: `value_sequence[0] == 15615244`

**Pass Criteria**: Match confirmed

---

## Testing Checklist

- [ ] Program parses input without errors
- [ ] Program executes without runtime exceptions
- [ ] Cycle detection triggers (program terminates)
- [ ] Answer differs from Part 1 answer (or sequence length is 1)
- [ ] First value in sequence matches Part 1 answer (15615244) - **CRITICAL VALIDATION**
- [ ] `len(seen_values) == len(value_sequence)` (no duplicates)
- [ ] Program completes in reasonable time (< 10 minutes)
- [ ] Output is a single non-negative integer
- [ ] Sequence length > 1 (found multiple unique values)
- [ ] Diagnostic output shows reasonable sequence length
- [ ] Progress indicators appear during long-running execution

## Debugging Strategy

If the program fails or produces incorrect results:

1. **Infinite Loop**: Add instruction counter with periodic output every 1M instructions
2. **Wrong Answer**: Print first 10 and last 10 values in sequence
3. **Cycle Not Detected**: Add logging every time instruction 29 is reached
4. **Crashes**: Check boundary conditions in register access

## Manual Verification Steps

Since full verification (running the program with register 0 set to our answer) would take too long:

1. **Partial Verification**: Run for 1M instructions and verify we haven't halted yet
2. **Sequence Validation**: Confirm the value appears in our tracked sequence
3. **Logic Validation**: The last unique value MUST cause maximum instructions because all previous values would cause earlier halting

## Success Criteria

The solution is correct if:
1. ✅ Program terminates with a single integer answer
2. ✅ Answer ≠ Part 1 answer (15615244), unless sequence has only 1 unique value (extremely unlikely)
3. ✅ First value in detected sequence == 15615244 (**CRITICAL VALIDATION**)
4. ✅ Cycle detection triggered (found a repeated value)
5. ✅ Sequence contains multiple unique values (> 1)
6. ✅ No runtime errors or infinite loops
7. ✅ Progress indicators appear during execution (if runtime > 10 seconds)
