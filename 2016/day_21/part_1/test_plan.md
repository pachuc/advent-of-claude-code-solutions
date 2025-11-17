# Testing Plan: Password Scrambler

## Testing Strategy Overview
Validate the password scrambler implementation through unit testing of individual operations, integration testing of operation sequences, and verification against the provided example.

## Test Levels

### Level 1: Unit Tests for Individual Operations

#### Test 1.1: Swap Position
**Objective**: Verify position-based character swapping

**Test cases**:
1. `swap_position('abcdefgh', 0, 7)` → `hbcdefga`
2. `swap_position('abcdefgh', 3, 3)` → `abcdefgh` (same position, no change)
3. `swap_position('abcdefgh', 1, 4)` → `aecdbfgh`
4. `swap_position('decab', 0, 2)` → `cedab`

**Verification method**: Assert output equals expected string

#### Test 1.2: Swap Letter
**Objective**: Verify letter-based character swapping

**Test cases**:
1. `swap_letter('abcdefgh', 'a', 'h')` → `hbcdefga`
2. `swap_letter('abcdefgh', 'e', 'd')` → `abcedfgh`
3. `swap_letter('aabbcc', 'a', 'c')` → `ccbbaa` (multiple occurrences)
4. `swap_letter('abcdefgh', 'x', 'y')` → `abcdefgh` (letters not present, no-op behavior)

**Verification method**: Assert output equals expected string

**Note**: When letters don't exist in string, operation should be a no-op (no change).

#### Test 1.3: Rotate Left
**Objective**: Verify left rotation with wraparound

**Test cases**:
1. `rotate_left('abcdefgh', 1)` → `bcdefgha`
2. `rotate_left('abcdefgh', 0)` → `abcdefgh` (no rotation)
3. `rotate_left('abcdefgh', 8)` → `abcdefgh` (full rotation)
4. `rotate_left('abcdefgh', 3)` → `defghabc`
5. `rotate_left('abcde', 1)` → `bcdea` (from example)

**Verification method**: Assert output equals expected string

#### Test 1.4: Rotate Right
**Objective**: Verify right rotation with wraparound

**Test cases**:
1. `rotate_right('abcdefgh', 1)` → `habcdefg`
2. `rotate_right('abcdefgh', 0)` → `abcdefgh` (no rotation)
3. `rotate_right('abcdefgh', 8)` → `abcdefgh` (full rotation)
4. `rotate_right('abcdefgh', 6)` → `cdefghab`
5. `rotate_right('abcd', 1)` → `dabc` (from problem description)

**Verification method**: Assert output equals expected string

#### Test 1.5: Rotate Based on Letter Position
**Objective**: Verify position-based rotation formula: 1 + index + (1 if index >= 4 else 0)

**Test cases**:
1. Letter at index 0: rotate 1 step (1 + 0 + 0)
   - `rotate_based_on_letter('abcde', 'a')` → index 0 → rotate right 1 → `eabcd`
2. Letter at index 1: rotate 2 steps (1 + 1 + 0)
   - `rotate_based_on_letter('ecabd', 'b')` → index 1 → rotate right 2 → `bdeca`
3. Letter at index 2: rotate 3 steps (1 + 2 + 0)
   - `rotate_based_on_letter('abcde', 'c')` → index 2 → rotate right 3 → `cdeab`
4. Letter at index 4: rotate 6 steps (1 + 4 + 1)
   - `rotate_based_on_letter('ecabd', 'd')` → index 4 → rotate right 6 → 6%5=1 → `decab`
5. Letter at index 5: rotate 7 steps (1 + 5 + 1)
   - `rotate_based_on_letter('abcdefgh', 'f')` → index 5 → rotate right 7 → `gabcdefh`
6. Letter at index 7: rotate 9 steps = 1 step (1 + 7 + 1 = 9, 9 % 8 = 1)
   - `rotate_based_on_letter('abcdefgh', 'h')` → index 7 → rotate right 9 → 9%8=1 → `habcdefg`

**Verification method**:
- Find index of letter in **current** string (not original)
- Calculate expected rotation: 1 + index + (1 if index >= 4 else 0)
- Apply rotate_right with calculated steps (use modulo for wraparound)
- Assert output matches

**Note**: Index is found in the current string state before rotation, not the original password.

#### Test 1.6: Reverse Positions
**Objective**: Verify substring reversal

**Test cases**:
1. `reverse_positions('abcdefgh', 0, 7)` → `hgfedcba` (full reversal)
2. `reverse_positions('abcdefgh', 0, 0)` → `abcdefgh` (single character)
3. `reverse_positions('abcdefgh', 2, 5)` → `abfedcgh`
4. `reverse_positions('abcde', 0, 4)` → `edcba` (from example)
5. `reverse_positions('abcdefgh', 3, 7)` → `abchgfed`

**Verification method**: Assert output equals expected string

#### Test 1.7: Move Position
**Objective**: Verify remove and insert operation

**Test cases**:
1. `move_position('abcdefgh', 0, 7)` → `bcdefgha` (move first to last)
2. `move_position('abcdefgh', 7, 0)` → `habcdefg` (move last to first)
3. `move_position('abcdefgh', 2, 5)` → `abdefcgh`
4. `move_position('bcdea', 1, 4)` → `bdeac` (from example)
5. `move_position('bdeac', 3, 0)` → `abdec` (from example)
6. `move_position('abcdefgh', 3, 3)` → `abcdefgh` (same position)

**Verification method**: Assert output equals expected string

### Level 2: Operation Parsing Tests

#### Test 2.1: Parse Each Operation Type
**Objective**: Ensure parser correctly extracts operation types and parameters

**Test cases**:
1. `"swap position 7 with position 1"` → `('swap_position', (7, 1))`
2. `"swap letter e with letter d"` → `('swap_letter', ('e', 'd'))`
3. `"rotate left 2 steps"` → `('rotate_left', 2)`
4. `"rotate right 6 steps"` → `('rotate_right', 6)`
5. `"rotate based on position of letter a"` → `('rotate_based', 'a')`
6. `"reverse positions 3 through 7"` → `('reverse', (3, 7))`
7. `"move position 4 to position 0"` → `('move', (4, 0))`

**Verification method**:
- Call parse_operation() for each
- Assert returned tuple matches expected format

#### Test 2.2: Edge Cases in Parsing
**Test cases**:
1. Extra whitespace: `"  swap position 1 with position 2  "`
2. Different step counts: `"rotate left 0 steps"`, `"rotate right 10 steps"`

**Verification method**: Parser should handle gracefully

### Level 3: Integration Tests

#### Test 3.1: Example Walkthrough
**Objective**: Verify against provided example in problem statement

**Input**: `abcde`
**Operations**:
1. `swap position 4 with position 0` → `ebcda`
2. `swap letter d with letter b` → `edcba`
3. `reverse positions 0 through 4` → `abcde`
4. `rotate left 1 step` → `bcdea`
5. `move position 1 to position 4` → `bdeac`
6. `move position 3 to position 0` → `abdec`
7. `rotate based on position of letter b` → `ecabd`
8. `rotate based on position of letter d` → `decab`

**Verification method**:
- Apply each operation step by step
- After each step, assert intermediate result matches expected
- Final result should be `decab`

#### Test 3.2: Sequential Operation Application
**Objective**: Test that operations are applied in correct order (order matters!)

**Test case**:
```
Initial: abcdefgh
Operation 1: swap position 0 with position 7 → hbcdefga
Operation 2: rotate left 2 steps → cdefgahb
Operation 3: reverse positions 0 through 3 → fedc gahb → fedcgahb
Expected: fedcgahb
```

**Verification method**:
- Manually trace execution step by step
- Verify intermediate states
- Assert final output matches expected
- Ensures operations aren't accidentally batched or reordered

### Level 4: Full Solution Validation

#### Test 4.1: Run Against Actual Input
**Objective**: Execute complete solution with all 100 operations

**Method**:
1. Run solution with `abcdefgh` as initial password
2. Apply all 100 operations from input.md
3. Capture final output

**Verification approach**:
1. **Primary validation**: Ensure example walkthrough produces `decab` (if it doesn't, implementation is wrong)
2. **Secondary validation** for full solution:
   - Length is still 8 characters
   - Contains same characters as initial (just scrambled): a, b, c, d, e, f, g, h
   - No duplicates or missing characters
   - Use `sorted(result) == sorted(initial)` to verify character set preservation
3. **Additional validation**: Manually trace through first 3-5 operations to spot-check correctness
4. **Optional**: Search online or use reference implementation to verify final answer if available

#### Test 4.2: Character Set Preservation
**Objective**: Ensure all operations preserve the original character set

**Test case**:
```python
initial = 'abcdefgh'
result = scramble_password(initial, all_operations)
assert sorted(initial) == sorted(result)
```

**Verification method**: Sort both strings and compare

#### Test 4.3: Idempotency Checks (Optional - Low Priority)
**Objective**: Test behavior with repeated operations

**Test cases**:
1. Apply rotate right 8 steps (should return to original)
2. Apply reverse twice on same range (should return to original)
3. Apply swap position twice with same indices (should return to original)

**Verification method**: Assert double application returns original

**Note**: This is optional for a script solution and not critical to solving the problem.

### Level 5: Edge Case Testing

#### Test 5.1: Boundary Positions
**Test cases**:
- Operations at position 0
- Operations at position 7 (last index)
- Operations spanning full string (0 through 7)

#### Test 5.2: Zero Step Rotations
**Test cases**:
- `rotate_left('abcdefgh', 0)` → `abcdefgh` (no change)
- `rotate_right('abcdefgh', 0)` → `abcdefgh` (no change)

**Critical**: Ensure rotate_right handles steps=0 correctly (avoid `s[:-0]` bug)

#### Test 5.3: Large Rotation Values
**Test cases**:
- `rotate_left('abcdefgh', 100)` → normalize to 100 % 8 = 4 → `efghabcd`
- `rotate_right('abcdefgh', 16)` → normalize to 16 % 8 = 0 → `abcdefgh` (no change)
- `rotate_left('abcdefgh', 10)` → normalize to 10 % 8 = 2 → `cdefghab`

**Verification method**: Modulo arithmetic should normalize large values correctly

## Testing Execution Plan

### Phase 1: Unit Testing (Priority: High)
1. Implement each operation function
2. Write unit test for that function immediately
3. Run test and verify
4. Fix any issues before moving to next function

### Phase 2: Integration Testing (Priority: High)
1. Implement parser and main orchestrator
2. Run example walkthrough test
3. Debug any discrepancies
4. Verify step-by-step execution matches expected

### Phase 3: Full Solution Testing (Priority: Medium)
1. Run complete solution with actual input
2. Verify character set preservation
3. Check output format and length

### Phase 4: Edge Case Testing (Priority: Low)
1. Test boundary conditions
2. Test edge cases if time permits
3. Optional for simple script solution

## Test Implementation Structure

**Note**: Tests can be implemented as part of the main script file or in a separate test file. For a simple script solution, including test functions in the same file is acceptable.

```python
def test_operations():
    # Unit tests for each operation
    assert swap_position('abcdefgh', 0, 7) == 'hbcdefga'
    assert swap_letter('abcdefgh', 'a', 'h') == 'hbcdefga'
    assert rotate_left('abcdefgh', 0) == 'abcdefgh'  # Zero step edge case
    assert rotate_right('abcdefgh', 0) == 'abcdefgh'  # Critical: s[:-0] bug test
    # ... more tests

def test_example_walkthrough():
    password = 'abcde'
    password = swap_position(password, 4, 0)
    assert password == 'ebcda', f"Expected 'ebcda', got '{password}'"
    # ... continue through example
    # Final check
    assert password == 'decab', f"Expected 'decab', got '{password}'"

def test_full_solution():
    initial = 'abcdefgh'
    operations = read_operations('input.md')
    result = scramble_password(initial, operations)
    assert len(result) == 8, f"Result length is {len(result)}, expected 8"
    assert sorted(result) == sorted(initial), "Character set not preserved"
    print(f"Final scrambled password: {result}")

if __name__ == '__main__':
    test_operations()
    print("✓ Unit tests passed")
    test_example_walkthrough()
    print("✓ Example walkthrough passed")
    test_full_solution()
    print("✓ Full solution completed")
```

## Success Criteria

1. **Critical**: Example walkthrough produces correct final result: `decab` from `abcde`
2. All unit tests pass for individual operations (especially rotate_right with steps=0)
3. Full solution runs without errors on all 100 operations
4. Output is 8 characters containing exactly {a,b,c,d,e,f,g,h}
5. Character set is preserved throughout all operations (verified via sorted comparison)
6. Manual spot-check of first 3-5 operations confirms correct behavior

## Debugging Strategy

If tests fail:
1. Add intermediate print statements in scramble_password to see state after each operation
2. Compare intermediate states with manual calculation
3. Verify parser is extracting correct parameters
4. Check for off-by-one errors in indexing
5. Verify rotation direction and modulo arithmetic
