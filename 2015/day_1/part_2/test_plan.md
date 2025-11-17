# Test Plan: Santa's Basement Entry Position

## Testing Strategy Overview
Verify the solution correctly identifies the 1-indexed position of the first character that causes Santa to reach floor -1, using a combination of unit tests for edge cases and validation against known examples.

## Test Categories

### 1. Example-Based Tests (Specification Validation)
Test against the provided examples to ensure basic correctness.

#### Test 1.1: Single Character Immediate Basement
- **Input**: `)`
- **Expected Output**: `1`
- **Rationale**: First character immediately takes Santa from floor 0 to floor -1
- **Validates**: Immediate basement entry, 1-indexed positioning

#### Test 1.2: Multiple Steps Before Basement
- **Input**: `()())`
- **Expected Output**: `5`
- **Rationale**:
  - Position 1 `(`: floor 0→1
  - Position 2 `)`: floor 1→0
  - Position 3 `(`: floor 0→1
  - Position 4 `)`: floor 1→0
  - Position 5 `)`: floor 0→-1 (first basement)
- **Validates**: Multiple floor changes, correct position tracking

### 2. Edge Case Tests

#### Test 2.1: Never Reaching Basement
- **Input**: `((((`
- **Expected Output**: `None` or error indicator
- **Rationale**: Santa only goes up, never reaches floor -1
- **Validates**: Handling case where basement is never reached

#### Test 2.2: Immediate Basement After Multiple Ups
- **Input**: `(((())))`
- **Expected Output**: `8`
- **Manual Trace**:
  - Pos 1 `(`: floor 1
  - Pos 2 `(`: floor 2
  - Pos 3 `(`: floor 3
  - Pos 4 `(`: floor 4
  - Pos 5 `)`: floor 3
  - Pos 6 `)`: floor 2
  - Pos 7 `)`: floor 1
  - Pos 8 `)`: floor 0
  - Pos 9 `)`: floor -1 ✓
- **Corrected Expected Output**: `9`
- **Rationale**: After going up 4 floors, it takes 5 down movements to reach basement
- **Validates**: Deep floor changes before basement entry

#### Test 2.3: Alternating Pattern
- **Input**: `()()()())`
- **Expected Output**: `9`
- **Rationale**: Eight characters keep returning to floor 0, ninth enters basement
- **Validates**: Repeated patterns with eventual basement entry

#### Test 2.4: Long Upward Then Quick Descent
- **Input**: `(` * 100 + `)` * 101
- **Expected Output**: `201`
- **Rationale**:
  - First 100 chars go up to floor 100
  - Next 100 chars return to floor 0
  - 201st char enters basement
- **Validates**: Handling longer inputs, deep floors before basement

#### Test 2.5: Basement Multiple Times
- **Input**: `)(`
- **Expected Output**: `1`
- **Rationale**: First char enters basement at position 1, second char would exit but we stop at first entry
- **Validates**: Early exit, not returning all basement entries

### 3. Boundary and Special Cases

#### Test 3.1: Empty String
- **Input**: ``
- **Expected Output**: `None` or appropriate handling
- **Rationale**: Edge case for empty input
- **Validates**: Empty input handling (though unlikely in problem context)

#### Test 3.2: Very Long Input (Performance Test)
- **Input**: Input from `input.md` (~7000 characters)
- **Expected Output**: Some positive integer ≤ 7000
- **Rationale**: Validates performance on actual problem input
- **Validates**: Algorithm efficiency, correct parsing of long strings
- **Performance Check**: Should complete in < 10ms (likely < 1ms on modern hardware)

#### Test 3.3: Basement at Last Position
- **Input**: `(` * 100 + `)` * 100 + `)`
- **Expected Output**: `201`
- **Rationale**: Basement entry at very last character
- **Validates**: Full string traversal, last position handling

### 4. Algorithm Correctness Tests

#### Test 4.1: Floor Tracking Accuracy
- **Input**: `((()))`
- **Manual Trace**:
  - Start: floor 0
  - Pos 1 `(`: floor 1
  - Pos 2 `(`: floor 2
  - Pos 3 `(`: floor 3
  - Pos 4 `)`: floor 2
  - Pos 5 `)`: floor 1
  - Pos 6 `)`: floor 0
- **Expected Output**: `None` (never reaches -1)
- **Validates**: Correct floor increment/decrement logic

#### Test 4.2: Immediate After Zero
- **Input**: `())))`
- **Manual Trace**:
  - Start: floor 0
  - Pos 1 `(`: floor 1
  - Pos 2 `)`: floor 0
  - Pos 3 `)`: floor -1 ✓
- **Expected Output**: `3`
- **Validates**: Basement entry from floor 0

#### Test 4.3: Deep Negative (Should Stop at First -1)
- **Input**: `))))`
- **Manual Trace**:
  - Start: floor 0
  - Pos 1 `)`: floor -1 ✓ (should return here)
- **Expected Output**: `1`
- **Validates**: Early exit, not continuing to deeper floors

## Test Execution Plan

### Phase 1: Manual Unit Tests
Create a test script `test_solution.py` with the following structure:

```python
from solution import find_basement_position

def test_examples():
    """Test provided examples"""
    assert find_basement_position(')') == 1
    assert find_basement_position('()())') == 5
    print("✓ Example tests passed")

def test_edge_cases():
    """Test edge cases"""
    assert find_basement_position('((())))') == 7  # 3 ups, 4 downs -> basement at pos 7
    assert find_basement_position('()()()())') == 9
    assert find_basement_position(')') == 1
    assert find_basement_position('))))') == 1
    print("✓ Edge case tests passed")

def test_boundaries():
    """Test boundary conditions"""
    # Never reaching basement
    assert find_basement_position('((((') is None
    assert find_basement_position('((()))') is None

    # Basement at various positions
    assert find_basement_position('())))') == 3
    print("✓ Boundary tests passed")

def test_actual_input():
    """Test with actual problem input"""
    with open('input.md', 'r') as f:
        instructions = f.read().strip()

    result = find_basement_position(instructions)
    assert result is not None
    assert isinstance(result, int)
    assert result > 0
    assert result <= len(instructions)
    print(f"✓ Actual input test passed: position = {result}")

if __name__ == "__main__":
    test_examples()
    test_edge_cases()
    test_boundaries()
    test_actual_input()
    print("\n✅ All tests passed!")
```

### Phase 2: Manual Verification Tests

#### Verification Test 1: Small Custom Examples
Create several small inputs manually and trace through them:
- Verify floor calculation by hand
- Confirm position indexing (1-indexed vs 0-indexed)
- Check early exit behavior

#### Verification Test 2: Pattern Validation
- Test with predictable patterns: `()()()...`
- Verify position calculation: if pattern breaks at position N, result should be N

#### Verification Test 3: Actual Input Validation
- Run solution on `input.md`
- Manually verify the result by:
  1. Extracting substring from start to result position
  2. Counting `(` and `)` characters
  3. Confirming: count(`)`) - count(`(`) == 1 (to be at floor -1)
  4. Verifying previous position wouldn't give floor -1

### Phase 3: Output Validation

#### Check 1: Result Type and Range
```python
result = find_basement_position(instructions)
assert isinstance(result, int), "Result should be integer"
assert result >= 1, "Position should be at least 1 (1-indexed)"
assert result <= len(instructions), "Position can't exceed input length"
```

#### Check 2: Floor Verification at Result Position
```python
def verify_result(instructions, position):
    """Verify the result is correct"""
    floor = 0
    for i, char in enumerate(instructions[:position], 1):
        if char == '(':
            floor += 1
        else:
            floor -= 1

    # At the result position, we should be at floor -1
    assert floor == -1, f"At position {position}, floor should be -1, got {floor}"

    # At position-1, we should NOT be at floor -1 (if position > 1)
    if position > 1:
        floor = 0
        for char in instructions[:position-1]:
            floor += 1 if char == '(' else -1
        assert floor != -1, f"Floor -1 reached before position {position}"

    print(f"✓ Result {position} verified correct")
```

## Success Criteria

### Correctness Criteria
1. ✅ All example tests pass
2. ✅ Edge cases handled appropriately
3. ✅ Result is 1-indexed integer
4. ✅ Floor calculation is accurate (verified independently)
5. ✅ First occurrence detection works (not a later occurrence)

### Performance Criteria
1. ✅ Completes actual input (~7000 chars) in < 10ms (typically < 1ms)
2. ✅ Linear time complexity O(n) observed
3. ✅ Constant space usage observed

### Validation Criteria
1. ✅ Manual trace of result position confirms floor -1
2. ✅ Previous position (result-1) does not have floor -1
3. ✅ Count verification: at position P, count(`)`) - count(`(`) = 1

## Test Execution Steps

1. **Run unit tests**: Execute `test_solution.py`
2. **Verify examples**: Manually check provided examples work
3. **Run actual input**: Execute main solution with `input.md`
4. **Validate result**: Use verification function to confirm answer
5. **Performance check**: Time the execution (should be near-instantaneous)

## Expected Test Results Summary

- **Example tests**: 2 tests, both passing
- **Edge case tests**: ~5 tests covering various scenarios
- **Boundary tests**: ~3 tests for special conditions
- **Actual input test**: 1 test, returns valid integer position
- **Verification**: Manual confirmation of final result accuracy

## Notes

- Since this is a script for solving a specific problem (not production code), we focus on:
  - Correctness for the given input
  - Validation of algorithmic logic
  - Verification that answer is right
- We don't need:
  - Extensive error handling for malformed input
  - Testing every possible input combination
  - Performance testing beyond confirming efficiency
  - Input sanitization (input is trusted from problem source)
