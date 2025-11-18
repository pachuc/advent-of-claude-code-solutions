# Testing Plan: Permutation Promenade

## Plan Updates (v2)

Based on the critique, the following corrections and improvements were made:

1. **Fixed Test Case 2.2**: Corrected expected result from `['a', 'b', 'c', 'd', 'e']` to `['b', 'c', 'd', 'e', 'a']` with step-by-step verification
2. **Completed Test Case 2.4**: Added fully calculated expected result `['d', 'e', 'f', 'a', 'b', 'c']` with detailed step-by-step breakdown
3. **Added Test Case 3.6**: New test to verify actual input file parsing (checks move count, first move, etc.)
4. **Enhanced test script**: Updated all test functions to match in-place modification behavior, added more comprehensive assertions
5. **Fixed Test Case 5.2**: Changed from testing large spin values (which we assume won't occur) to testing full rotation equivalence
6. **Added validation**: Multiple spins and complex sequence tests now included in test script

## Testing Strategy

We need to verify that our implementation correctly simulates the dance moves and produces the correct final arrangement. Testing will focus on:
1. Individual move operations
2. Sequence of moves
3. Edge cases
4. Full input validation

## Test Categories

### 1. Unit Tests for Individual Operations

#### 1.1 Spin Operation Tests

**Test Case 1.1.1: Basic spin**
- Input: `['a', 'b', 'c', 'd', 'e']`, spin 1
- Expected: `['e', 'a', 'b', 'c', 'd']`
- Rationale: Verify basic spin functionality

**Test Case 1.1.2: Spin multiple**
- Input: `['a', 'b', 'c', 'd', 'e']`, spin 3
- Expected: `['c', 'd', 'e', 'a', 'b']`
- Rationale: Verify spinning more than one element

**Test Case 1.1.3: Spin zero**
- Input: `['a', 'b', 'c', 'd', 'e']`, spin 0
- Expected: `['a', 'b', 'c', 'd', 'e']`
- Rationale: Edge case - no change

**Test Case 1.1.4: Spin entire list**
- Input: `['a', 'b', 'c', 'd', 'e']`, spin 5
- Expected: `['a', 'b', 'c', 'd', 'e']`
- Rationale: Edge case - full rotation returns to original

**Test Case 1.1.5: Spin with 16 programs**
- Input: `['a', ..., 'p']`, spin 11
- Expected: First element should be 'f' (the 11th from end)
- Rationale: Test with actual problem size

#### 1.2 Exchange Operation Tests

**Test Case 1.2.1: Basic exchange**
- Input: `['e', 'a', 'b', 'd', 'c']`, exchange positions 3 and 4
- Expected: `['e', 'a', 'b', 'c', 'd']`
- Rationale: Verify basic swap functionality

**Test Case 1.2.2: Exchange at boundaries**
- Input: `['a', 'b', 'c', 'd', 'e']`, exchange positions 0 and 4
- Expected: `['e', 'b', 'c', 'd', 'a']`
- Rationale: Test swapping first and last elements

**Test Case 1.2.3: Exchange adjacent positions**
- Input: `['a', 'b', 'c', 'd', 'e']`, exchange positions 1 and 2
- Expected: `['a', 'c', 'b', 'd', 'e']`
- Rationale: Test swapping adjacent elements

**Test Case 1.2.4: Exchange same position**
- Input: `['a', 'b', 'c', 'd', 'e']`, exchange positions 2 and 2
- Expected: `['a', 'b', 'c', 'd', 'e']`
- Rationale: Edge case - swapping element with itself

#### 1.3 Partner Operation Tests

**Test Case 1.3.1: Basic partner swap**
- Input: `['b', 'a', 'e', 'd', 'c']`, partner 'e' and 'b'
- Expected: `['e', 'a', 'b', 'd', 'c']`
- Rationale: Verify name-based swapping

**Test Case 1.3.2: Partner swap at boundaries**
- Input: `['a', 'b', 'c', 'd', 'e']`, partner 'a' and 'e'
- Expected: `['e', 'b', 'c', 'd', 'a']`
- Rationale: Test swapping programs at extremes

**Test Case 1.3.3: Partner swap same program**
- Input: `['a', 'b', 'c', 'd', 'e']`, partner 'c' and 'c'
- Expected: `['a', 'b', 'c', 'd', 'e']`
- Rationale: Edge case - swapping program with itself

**Test Case 1.3.4: Partner after position changes**
- Input: `['e', 'a', 'b', 'd', 'c']`, partner 'a' and 'd'
- Expected: `['e', 'd', 'b', 'a', 'c']`
- Rationale: Verify partner finds correct positions regardless of arrangement

### 2. Integration Tests - Move Sequences

#### Test Case 2.1: Example from problem statement
- Input: `['a', 'b', 'c', 'd', 'e']`
- Moves: `s1`, `x3/4`, `pe/b`
- Expected: `['b', 'a', 'e', 'd', 'c']`
- Rationale: Verify against provided example

**Step-by-step verification:**
1. After `s1`: `['e', 'a', 'b', 'c', 'd']`
2. After `x3/4`: `['e', 'a', 'b', 'd', 'c']`
3. After `pe/b`: `['b', 'a', 'e', 'd', 'c']`

#### Test Case 2.2: Multiple spins in sequence
- Input: `['a', 'b', 'c', 'd', 'e']`
- Moves: `s2`, `s2`
- Expected: `['b', 'c', 'd', 'e', 'a']`
- Rationale: Verify multiple spins compose correctly
- Step-by-step:
  1. After first `s2`: `['d', 'e', 'a', 'b', 'c']` (last 2 to front)
  2. After second `s2`: `['b', 'c', 'd', 'e', 'a']` (last 2 of previous result to front)

#### Test Case 2.3: Exchange then partner on swapped elements
- Input: `['a', 'b', 'c', 'd', 'e']`
- Moves: `x0/4`, `pa/e`
- Expected: `['a', 'b', 'c', 'd', 'e']`
- Rationale: Verify operations work correctly in sequence
- Steps: After `x0/4`: `['e', 'b', 'c', 'd', 'a']`, after `pa/e`: back to original

#### Test Case 2.4: Complex sequence
- Input: `['a', 'b', 'c', 'd', 'e', 'f']`
- Moves: `s2`, `x1/4`, `pc/f`, `s1`
- Expected: `['d', 'e', 'f', 'a', 'b', 'c']`
- Rationale: Test multiple operation types in sequence
- Step-by-step:
  1. Start: `['a', 'b', 'c', 'd', 'e', 'f']`
  2. After `s2`: `['e', 'f', 'a', 'b', 'c', 'd']` (last 2 to front)
  3. After `x1/4`: `['e', 'c', 'a', 'b', 'f', 'd']` (swap positions 1 and 4)
  4. After `pc/f`: `['e', 'f', 'a', 'b', 'c', 'd']` ('c' at pos 1, 'f' at pos 4, swap them)
  5. After `s1`: `['d', 'e', 'f', 'a', 'b', 'c']` (last 1 to front)

### 3. Input Parsing Tests

#### Test Case 3.1: Parse spin move
- Input string: `"s11"`
- Expected: Identify as spin, extract value 11
- Rationale: Verify single-digit and multi-digit parsing

#### Test Case 3.2: Parse exchange move
- Input string: `"x10/2"`
- Expected: Identify as exchange, extract positions 10 and 2
- Rationale: Verify multi-digit position parsing

#### Test Case 3.3: Parse partner move
- Input string: `"pl/d"`
- Expected: Identify as partner, extract names 'l' and 'd'
- Rationale: Verify character extraction

#### Test Case 3.4: Parse move sequence
- Input string: `"s1,x3/4,pe/b"`
- Expected: Split into 3 moves
- Rationale: Verify comma separation works

#### Test Case 3.5: Handle trailing comma or empty strings
- Input string: `"s1,x3/4,"`
- Expected: Process 2 valid moves, ignore empty string
- Rationale: Handle potential malformed input

#### Test Case 3.6: Verify actual input parsing
- Input: Read from `input.md`
- Verification:
  1. Count number of moves (should be > 1000)
  2. Verify first move is parsed correctly (should be `s11`)
  3. Verify no empty strings in move list (after filtering)
  4. Print total number of moves for visibility
- Rationale: Ensure entire input file is correctly parsed

### 4. Full Solution Tests

#### Test Case 4.1: Verify with actual input
- Input: Full `input.md` file
- Moves: All ~10,000+ moves
- Expected: Unknown (will be the answer)
- Verification method:
  1. Run the program
  2. Verify output is exactly 16 characters
  3. Verify all characters are unique
  4. Verify all characters are from 'a' to 'p'

#### Test Case 4.2: Identity check after processing
- After running full input, verify:
  - Length of result is 16
  - Result contains each letter a-p exactly once
  - No duplicates
  - No missing letters

### 5. Edge Case Tests

#### Test Case 5.1: Order preservation
- Verify that programs maintain their identity through transformations
- After any sequence, each program appears exactly once

#### Test Case 5.2: Full rotation equivalence
- Input: `['a', 'b', 'c', 'd', 'e']`, spin 5
- Expected: `['a', 'b', 'c', 'd', 'e']`
- Rationale: Spinning by the full length should return to original
- Note: Spin values exceeding array length are assumed not to occur in input

#### Test Case 5.3: Reverse operation order
- Verify that operations applied in different orders produce different results
- Example: `x0/1` then `pa/b` vs `pa/b` then `x0/1` should differ

## Testing Implementation Approach

### Phase 1: Manual Testing of Examples
1. Implement the example walkthrough from problem statement
2. Verify each step manually
3. Confirm final result matches expected output

### Phase 2: Unit Testing
1. Create small test functions for each operation
2. Test each operation independently with various inputs
3. Print intermediate results to verify correctness

### Phase 3: Integration Testing
1. Test sequences of moves
2. Verify composition of operations
3. Check that operations don't interfere with each other

### Phase 4: Full Input Validation
1. Run the complete program with actual input
2. Verify output format (16 characters, all unique, all from a-p)
3. Check runtime performance (should complete in reasonable time)

## Test Script Structure

```python
def test_spin():
    # Test spin operation (now modifies in-place)
    programs = list('abcde')
    spin(programs, 1)
    assert programs == list('eabcd'), f"Expected eabcd, got {''.join(programs)}"

    # Test multiple spin
    programs = list('abcde')
    spin(programs, 3)
    assert programs == list('cdeab'), f"Expected cdeab, got {''.join(programs)}"

    # Test spin zero
    programs = list('abcde')
    spin(programs, 0)
    assert programs == list('abcde'), f"Expected abcde, got {''.join(programs)}"

    print("✓ Spin tests passed")

def test_exchange():
    # Test exchange operation
    programs = list('eabcd')
    exchange(programs, 3, 4)
    assert programs == list('eabdc'), f"Expected eabdc, got {''.join(programs)}"

    # Test exchange at boundaries
    programs = list('abcde')
    exchange(programs, 0, 4)
    assert programs == list('ebcda'), f"Expected ebcda, got {''.join(programs)}"

    print("✓ Exchange tests passed")

def test_partner():
    # Test partner operation
    programs = list('eabdc')
    partner(programs, 'e', 'b')
    assert programs == list('baedc'), f"Expected baedc, got {''.join(programs)}"

    # Test partner after position changes
    programs = list('eadbc')
    partner(programs, 'a', 'd')
    assert programs == list('edabc'), f"Expected edabc, got {''.join(programs)}"

    print("✓ Partner tests passed")

def test_example_sequence():
    # Test full example from problem
    programs = list('abcde')
    spin(programs, 1)
    assert programs == list('eabcd'), f"Step 1: Expected eabcd, got {''.join(programs)}"

    exchange(programs, 3, 4)
    assert programs == list('eabdc'), f"Step 2: Expected eabdc, got {''.join(programs)}"

    partner(programs, 'e', 'b')
    assert programs == list('baedc'), f"Step 3: Expected baedc, got {''.join(programs)}"

    print("✓ Example sequence test passed")

def test_multiple_spins():
    # Test spin composition (Test Case 2.2)
    programs = list('abcde')
    spin(programs, 2)
    spin(programs, 2)
    assert programs == list('bcdea'), f"Expected bcdea, got {''.join(programs)}"
    print("✓ Multiple spins test passed")

def test_complex_sequence():
    # Test Case 2.4: Complex sequence
    programs = list('abcdef')
    spin(programs, 2)
    exchange(programs, 1, 4)
    partner(programs, 'c', 'f')
    spin(programs, 1)
    assert programs == list('defabc'), f"Expected defabc, got {''.join(programs)}"
    print("✓ Complex sequence test passed")

def test_input_parsing():
    # Test parsing of actual input file
    with open('input.md', 'r') as f:
        input_data = f.read().strip()

    moves = input_data.split(',')
    moves = [m for m in moves if m]  # Filter empty strings

    assert len(moves) > 1000, f"Expected >1000 moves, got {len(moves)}"
    assert moves[0] == 's11', f"Expected first move to be 's11', got {moves[0]}"
    print(f"✓ Input parsing test passed ({len(moves)} moves)")

def test_output_validity(result):
    # Validate final output
    assert len(result) == 16, f"Expected 16 characters, got {len(result)}"
    assert set(result) == set('abcdefghijklmnop'), "Missing or extra characters"
    assert len(set(result)) == 16, "Duplicate characters found"
    print("✓ Output validation passed")

def run_all_tests():
    print("Running unit tests...")
    test_spin()
    test_exchange()
    test_partner()
    test_example_sequence()
    test_multiple_spins()
    test_complex_sequence()
    test_input_parsing()
    print("\n✓ All unit tests passed!")
```

## Acceptance Criteria

The solution is correct if:
1. ✓ All unit tests pass for individual operations
2. ✓ Example sequence from problem produces correct output
3. ✓ Final output is exactly 16 characters
4. ✓ Final output contains each letter a-p exactly once
5. ✓ No errors or exceptions during execution
6. ✓ Execution completes in reasonable time (< 1 second expected)

## Additional Validation Tests

Beyond the unit tests, perform these validations:

1. **Input format validation**:
   - Verify no malformed moves in input (optional for AoC)
   - Check that all moves start with 's', 'x', or 'p'

2. **Performance testing**:
   - Time the execution with full input
   - Should complete well under 1 second (expected: ~0.1s for 10K+ moves)

3. **Invariant checking**:
   - After each move, verify length is still 16
   - After each move, verify all programs a-p are present
   - This can be enabled in debug mode

## Debugging Strategy

If tests fail:
1. **Print intermediate states**: After each operation, print the current arrangement
2. **Verify parsing**: Print parsed move parameters to ensure correct extraction
3. **Check indices**: Verify position calculations are correct (0-indexed)
4. **Trace example**: Step through the provided example line by line
5. **Isolate failing operation**: Identify which operation type is causing issues
6. **Check off-by-one errors**: Common issue with array indexing and slicing

## Test Execution Order

1. Run unit tests first (spin, exchange, partner individually)
2. Run example sequence test
3. Run full input with output validation
4. If all pass, solution is correct
