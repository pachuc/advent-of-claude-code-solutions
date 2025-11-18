# Testing Plan: Memory Reallocation Cycle Detection

## Testing Strategy Overview

We need to verify that our solution correctly:
1. Parses input
2. Finds the maximum bank with proper tie-breaking
3. Redistributes blocks correctly with wraparound
4. Detects cycles and counts them accurately
5. Produces the correct answer for the given input

### Testing Approach
- **Unit tests** for individual functions
- **Integration test** for the complete example from problem statement
- **Validation test** for the actual input
- **Edge case tests** for boundary conditions

## Test Plan by Component

### Test 1: Input Parsing (`parse_input`)

**Purpose**: Verify input is correctly parsed into a list of integers

**Test Cases**:

1. **Simple input**
   - Input: `"0 2 7 0"`
   - Expected: `[0, 2, 7, 0]`

2. **Tab-separated input** (matching actual input format)
   - Input: `"11\t11\t13\t7\t0\t15\t5\t5\t4\t4\t1\t1\t7\t1\t15\t11"`
   - Expected: `[11, 11, 13, 7, 0, 15, 5, 5, 4, 4, 1, 1, 7, 1, 15, 11]`

3. **Mixed whitespace**
   - Input: `"  1  2   3  "`
   - Expected: `[1, 2, 3]`

**Verification Method**:
```python
assert parse_input("0 2 7 0") == [0, 2, 7, 0]
assert len(parse_input(actual_input)) == 16
```

### Test 2: Find Maximum Bank (`find_max_bank`)

**Purpose**: Verify correct identification of max bank with tie-breaking

**Test Cases**:

1. **Clear maximum**
   - Input: `[0, 2, 7, 0]`
   - Expected: `2` (bank at index 2 has 7 blocks)

2. **Tie at beginning**
   - Input: `[7, 2, 7, 0]`
   - Expected: `0` (tie between index 0 and 2, choose lower index)

3. **Tie at end**
   - Input: `[3, 1, 2, 3]`
   - Expected: `0` (tie between index 0 and 3, choose lower index)

4. **All same values**
   - Input: `[5, 5, 5, 5]`
   - Expected: `0` (all tied, choose lowest)

5. **Single bank**
   - Input: `[10]`
   - Expected: `0` (only one option)

6. **From example (Cycle 3)**
   - Input: `[3, 1, 2, 3]`
   - Expected: `0` (example explicitly states bank 0 wins tie)

**Verification Method**:
```python
assert find_max_bank([0, 2, 7, 0]) == 2
assert find_max_bank([7, 2, 7, 0]) == 0
assert find_max_bank([3, 1, 2, 3]) == 0
```

### Test 3: Redistribution (`redistribute`)

**Purpose**: Verify blocks are correctly redistributed with wraparound

**Test Cases**:

0. **Block Conservation** (sanity check)
   - Input: Any configuration, e.g., `[0, 2, 7, 0]`
   - After redistribution, total blocks must remain constant
   - Verification: `sum(banks_before) == sum(banks_after)`
   - This catches bugs where blocks are lost or created during redistribution

1. **Example Cycle 1**
   - Input: `[0, 2, 7, 0]`
   - Bank 2 selected (7 blocks)
   - Redistribute starting at bank 3: 0→1, 1→2, 2→3, 3→0, 4→1, 5→2, 6→3
   - Expected: `[2, 4, 1, 2]`

2. **Example Cycle 2**
   - Input: `[2, 4, 1, 2]`
   - Bank 1 selected (4 blocks)
   - Redistribute starting at bank 2: 0→2, 1→3, 2→0, 3→1
   - Expected: `[3, 1, 2, 3]`

3. **Example Cycle 3**
   - Input: `[3, 1, 2, 3]`
   - Bank 0 selected (3 blocks)
   - Redistribute starting at bank 1: 0→1, 1→2, 2→3
   - Expected: `[0, 2, 3, 4]`

4. **Example Cycle 4**
   - Input: `[0, 2, 3, 4]`
   - Bank 3 selected (4 blocks)
   - Redistribute starting at bank 0: 0→0, 1→1, 2→2, 3→3
   - Expected: `[1, 3, 4, 1]`

5. **Example Cycle 5**
   - Input: `[1, 3, 4, 1]`
   - Bank 2 selected (4 blocks)
   - Redistribute starting at bank 3: 0→3, 1→0, 2→1, 3→2
   - Expected: `[2, 4, 1, 2]`

6. **Wraparound multiple times**
   - Input: `[0, 0, 10, 0]` (4 banks, 10 blocks)
   - Bank 2 selected, redistribute from bank 3
   - Each bank gets 2 extra blocks (10/4 = 2.5), banks 3,0 get 3rd block
   - Expected: `[3, 2, 0, 3]` (bank 3 gets 3, bank 0 gets 3, banks 1,2 get 2)
   - Wait, let me recalculate: start at 3, place 10 blocks one at a time
   - Positions: 3,0,1,2,3,0,1,2,3,0 → bank 0 gets 3, bank 1 gets 2, bank 2 gets 2, bank 3 gets 3
   - Expected: `[3, 2, 0, 3]`

7. **No redistribution** (bank with 0 blocks selected, edge case)
   - If all banks are 0: `[0, 0, 0, 0]`
   - Bank 0 selected (0 blocks)
   - Expected: `[0, 0, 0, 0]` (no change)

**Verification Method**:
```python
banks = [0, 2, 7, 0]
redistribute(banks)
assert banks == [2, 4, 1, 2]
```

**Important**: Verify that redistribution modifies in-place correctly

### Test 4: Complete Cycle Detection (`find_cycle_count`)

**Purpose**: Verify the complete algorithm including cycle detection

**Test Cases**:

1. **Full example from problem**
   - Input: `[0, 2, 7, 0]`
   - Expected: `5` cycles
   - Sequence verification:
     - Start: `[0, 2, 7, 0]`
     - Cycle 1: `[2, 4, 1, 2]`
     - Cycle 2: `[3, 1, 2, 3]`
     - Cycle 3: `[0, 2, 3, 4]`
     - Cycle 4: `[1, 3, 4, 1]`
     - Cycle 5: `[2, 4, 1, 2]` ← duplicate found

1a. **Full sequence trace test** (verify all intermediate states)
   - Input: `[0, 2, 7, 0]`
   - Manually step through each redistribution
   - Verify each intermediate configuration matches expected sequence
   - This catches subtle bugs in the redistribution logic

2. **Immediate cycle** (configuration repeats immediately)
   - Input: `[0, 0, 0, 0]`
   - After 1 cycle: `[0, 0, 0, 0]` (same as initial)
   - Expected: `1` cycle

3. **Two banks**
   - Input: `[0, 1]`
   - Cycle 1: redistribute 1 from bank 1 → `[1, 0]`
   - Cycle 2: redistribute 1 from bank 0 → `[0, 1]` ← duplicate
   - Expected: `2` cycles

**Verification Method**:
```python
assert find_cycle_count([0, 2, 7, 0]) == 5
```

**Detailed trace for example**:
```python
# Manual verification with print statements
banks = [0, 2, 7, 0]
seen = {tuple(banks)}
count = 0

# Cycle 1
redistribute(banks)  # [2, 4, 1, 2]
count += 1
assert tuple(banks) not in seen
seen.add(tuple(banks))

# Cycle 2
redistribute(banks)  # [3, 1, 2, 3]
count += 1
assert tuple(banks) not in seen
seen.add(tuple(banks))

# ... continue for all 5 cycles
# Cycle 5 should produce [2, 4, 1, 2] which is in seen
```

### Test 5: Actual Input Validation

**Purpose**: Verify the solution produces an answer for the actual input

**Test Case**:
- Input: `11	11	13	7	0	15	5	5	4	4	1	1	7	1	15	11`
- Expected: Unknown (we need to calculate this)
- Validation:
  - Result should be a positive integer
  - Result should be reasonable (e.g., < 100,000 cycles)
  - Execution should complete within reasonable time (< 1 second)

**Verification Method**:
```python
with open('input.md', 'r') as f:
    input_data = f.read()
banks = parse_input(input_data)
result = find_cycle_count(banks)
assert isinstance(result, int)
assert result > 0
print(f"Answer: {result}")
```

### Test 6: Edge Cases and Boundary Conditions

**Test Cases**:

1. **Single bank**
   - Input: `[5]`
   - Redistribute 5 from bank 0 to bank 0 (wraps to itself)
   - After cycle 1: `[5]` (same)
   - Expected: `1` cycle

2. **All zeros**
   - Input: `[0, 0, 0]`
   - Expected: `1` cycle (immediate repeat)

3. **Large block count**
   - Input: `[100, 0, 0, 0]`
   - Redistribute 100 blocks across 4 banks
   - Each bank gets 25 blocks
   - Expected: Calculate actual result

4. **Many banks with small values**
   - Input: `[1] * 16` (16 banks, each with 1 block)
   - Bank 0 selected (tie), redistribute to banks 1-16
   - After cycle: `[0, 2, 1, 1, ..., 1]` (bank 1 gets extra)
   - Verify no index errors

## Testing Execution Plan

### Phase 1: Unit Tests (Bottom-up)
1. Test `parse_input()` with various formats
2. Test `find_max_bank()` with all tie-breaking scenarios
3. Test `redistribute()` with manual verification of each cycle

### Phase 2: Integration Test
1. Run complete example `[0, 2, 7, 0]` and verify result is `5`
2. Manually trace through first 2-3 cycles to verify correctness
3. Print intermediate states if needed for debugging

### Phase 3: Production Run
1. Run with actual input from `input.md`
2. Verify result is reasonable
3. Time the execution to ensure efficiency

### Phase 4: Edge Case Validation
1. Test boundary conditions
2. Verify no crashes or infinite loops
3. Confirm all edge cases produce sensible results

## Success Criteria

The solution is correct if:
1. ✅ All unit tests pass
2. ✅ Example case returns `5` cycles
3. ✅ Actual input produces a result in < 1 second
4. ✅ No runtime errors or crashes
5. ✅ Manual trace of first few cycles matches expected behavior

## Testing Implementation

Create a test file `test_solution.py`:

```python
from solution import parse_input, find_max_bank, redistribute, find_cycle_count

def test_parse_input():
    assert parse_input("0 2 7 0") == [0, 2, 7, 0]
    assert parse_input("11\t11\t13") == [11, 11, 13]
    print("✓ parse_input tests passed")

def test_find_max_bank():
    assert find_max_bank([0, 2, 7, 0]) == 2
    assert find_max_bank([7, 2, 7, 0]) == 0
    assert find_max_bank([3, 1, 2, 3]) == 0
    assert find_max_bank([5, 5, 5, 5]) == 0
    print("✓ find_max_bank tests passed")

def test_redistribute():
    # Test block conservation
    banks = [0, 2, 7, 0]
    total_before = sum(banks)
    redistribute(banks)
    assert sum(banks) == total_before, "Blocks not conserved!"
    assert banks == [2, 4, 1, 2], f"Expected [2, 4, 1, 2], got {banks}"

    redistribute(banks)
    assert sum(banks) == total_before, "Blocks not conserved!"
    assert banks == [3, 1, 2, 3], f"Expected [3, 1, 2, 3], got {banks}"

    print("✓ redistribute tests passed")

def test_example_trace():
    """Verify all intermediate states match the example sequence."""
    banks = [0, 2, 7, 0]
    expected_sequence = [
        [2, 4, 1, 2],
        [3, 1, 2, 3],
        [0, 2, 3, 4],
        [1, 3, 4, 1],
        [2, 4, 1, 2]
    ]
    for i, expected in enumerate(expected_sequence, 1):
        redistribute(banks)
        assert banks == expected, f"Cycle {i}: expected {expected}, got {banks}"
    print("✓ example trace test passed")

def test_full_example():
    result = find_cycle_count([0, 2, 7, 0])
    assert result == 5, f"Expected 5, got {result}"
    print("✓ full example test passed")

def test_actual_input():
    with open('input.md', 'r') as f:
        input_data = f.read()
    banks = parse_input(input_data)
    result = find_cycle_count(banks)
    assert isinstance(result, int) and result > 0
    print(f"✓ actual input result: {result}")

if __name__ == "__main__":
    test_parse_input()
    test_find_max_bank()
    test_redistribute()
    test_example_trace()
    test_full_example()
    test_actual_input()
    print("\n✅ All tests passed!")
```

## Manual Verification Checklist

Before submitting the solution, manually verify:

- [ ] Example trace matches problem statement exactly
- [ ] Tie-breaking works correctly (lowest index wins)
- [ ] Wraparound indexing works correctly
- [ ] Initial configuration is included in seen set
- [ ] Cycle count is correct (not off-by-one)
- [ ] Solution runs in reasonable time (< 1 second)
- [ ] Output is a single integer
- [ ] No debugging print statements in final code

## Debugging Strategy

If tests fail:

1. **Parse error**: Print parsed list, check whitespace handling
2. **Wrong max bank**: Print all bank values and indices, verify comparison logic
3. **Wrong redistribution**: Print before/after states, manually count blocks
4. **Wrong cycle count**: Print each configuration and check against seen set
5. **Infinite loop**: Add max iteration limit, print cycle count periodically

## Performance Verification

Expected performance characteristics:
- **Time**: O(C × N) where C = cycles, N = banks
- **Space**: O(C × N) for storing configurations
- **For actual input**: Should complete in < 100ms
- **Maximum cycles**: Unlikely to exceed 10,000 for this problem size

If execution is slow:
- Check for infinite loops (duplicate detection failing)
- Verify set operations are being used (not list scanning)
- Profile to find bottleneck
