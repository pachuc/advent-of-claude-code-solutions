# Test Plan: JSON Number Summation

## Testing Strategy

We will verify the solution through:
1. **Example-based testing**: Validate against provided examples
2. **Edge case testing**: Test boundary conditions and special cases
3. **Integration testing**: Test with the actual input file
4. **Manual verification**: Spot-check results for correctness

## Test Cases

### 1. Provided Examples (Correctness Verification)

These examples are given in the problem statement and serve as our primary correctness tests:

| Input | Expected Output | Description |
|-------|----------------|-------------|
| `[1,2,3]` | `6` | Simple array |
| `{"a":2,"b":4}` | `6` | Simple object |
| `[[[3]]]` | `3` | Deeply nested array |
| `{"a":{"b":4},"c":-1}` | `3` | Nested object with negative |
| `{"a":[-1,1]}` | `0` | Array in object with canceling values |
| `[-1,{"a":1}]` | `0` | Mixed array and object with canceling values |
| `[]` | `0` | Empty array |
| `{}` | `0` | Empty object |

**Test Method**: Create a separate test file or add assertions to verify each example.

### 2. Edge Cases

#### 2.1 Empty Structures
- **Test**: `[]` → `0`
- **Test**: `{}` → `0`
- **Test**: `[[[]]]` → `0`
- **Test**: `{"a":{}}` → `0`
- **Rationale**: Ensure empty containers don't cause errors

#### 2.2 Negative Numbers
- **Test**: `[-5, -10, -3]` → `-18`
- **Test**: `{"a":-100}` → `-100`
- **Test**: `[5, -5]` → `0`
- **Rationale**: Verify correct handling of negative values and cancellation

#### 2.3 Zero Values
- **Test**: `[0, 0, 0]` → `0`
- **Test**: `{"a":0, "b":0}` → `0`
- **Test**: `[1, 0, -1]` → `0`
- **Rationale**: Ensure zeros are processed correctly

#### 2.4 Large Numbers
- **Test**: `[1000000, 2000000]` → `3000000`
- **Test**: `{"a":999999999}` → `999999999`
- **Rationale**: Verify no integer overflow (Python handles big ints automatically)

#### 2.5 Deep Nesting
- **Test**: Create JSON nested 50+ levels deep
- **Expected**: Correct sum without recursion errors
- **Rationale**: Verify recursion handles reasonable depths

#### 2.6 Boolean Values (CRITICAL TEST)
- **Test**: `[true, false, 5]` → `5`
- **Test**: `{"a":true, "b":false, "c":3}` → `3`
- **Test**: `[1, true, 2, false]` → `3` (booleans should NOT be counted as 1 and 0)
- **Rationale**: In Python, `bool` is a subclass of `int`, so we must explicitly exclude booleans from the sum. This is a critical edge case!

#### 2.7 Floating Point Numbers
- **Test**: `[1.5, 2.5]` → `4.0`
- **Test**: `{"a":3.14, "b":2}` → `5.14`
- **Test**: `[1, 2.5, -3.5]` → `0.0`
- **Test**: `{"x":[1.1, 2.2], "y":{"z":3.3}}` → `6.6`
- **Rationale**: JSON supports floating-point numbers. Even though the problem mentions "integers", we should handle floats if present.

#### 2.8 Mixed Types
- **Test**: `["string", 5, true, null, 10]` → `15`
- **Test**: `{"a":"text", "b":5, "c":null, "d":10}` → `15`
- **Test**: `[1, "text", 2.5, true, false, null, 3]` → `6.5`
- **Rationale**: Ensure non-numeric types are ignored correctly

#### 2.10 Complex Mixed Structures
- **Test**: `[1, [2, {"a":3, "b":[4, 5]}], 6]` → `21`
- **Test**: `{"x":[1,2], "y":{"z":3}}` → `6`
- **Test**: `[1.5, [true, {"a":2, "b":[false, 3.5]}], "text"]` → `7.0`
- **Rationale**: Verify complex nesting with mixed arrays/objects and various types

### 3. Actual Input Testing

#### 3.1 Run Against Real Input
```bash
python solution.py
```

**Verification Steps**:
1. Program runs without errors
2. Output is a single integer
3. Output completes in reasonable time (< 1 second for typical input)

#### 3.2 Result Validation
Since we don't have the expected answer beforehand, we'll validate by:
- **Sanity checks**:
  - Result should be a reasonable integer (not obviously wrong like 0 or negative millions)
  - Result should be proportional to input size
- **Manual spot-checking**:
  - Pick 5-10 random numbers from the input
  - Verify they contribute to the sum appropriately
  - Check a few deeply nested values are included

### 4. Performance Testing

#### 4.1 Execution Time
- **Test**: Time the execution with the actual input
- **Expected**: Complete in under 1 second
- **Command**:
  ```bash
  time python solution.py
  ```

#### 4.2 Memory Usage
- **Test**: Monitor memory consumption
- **Expected**: Reasonable memory usage (< 100MB for typical inputs)
- **Rationale**: Ensure efficient processing

### 5. Input/Output Testing

#### 5.1 File Reading
- **Test**: Verify input.md exists and is readable
- **Expected**: No file I/O errors
- **Error case**: If file missing, should show clear error message

#### 5.2 JSON Parsing
- **Test**: Verify JSON in input.md is valid
- **Expected**: No JSON parse errors
- **Error case**: Invalid JSON should raise json.JSONDecodeError

#### 5.3 Output Format
- **Test**: Verify output is single integer on one line
- **Expected**: Clean output, no extra whitespace or text
- **Rationale**: Match problem requirements

## Test Execution Plan

### Phase 1: Unit Testing (Quick validation)
1. Test all provided examples manually
2. **CRITICAL**: Test boolean handling (must return 0, not 1 or 0)
3. Test float handling (if applicable)
4. Test edge cases (empty, negatives, zeros)
5. Test type handling (strings, booleans, null)

**Success Criteria**: All examples produce correct output, especially boolean tests

### Phase 2: Integration Testing
1. Run solution against actual input.md
2. Verify output is produced without errors
3. Perform sanity checks on result

**Success Criteria**: Program executes successfully and produces reasonable result

### Phase 3: Validation
1. Manual spot-check values from input
2. Verify timing is acceptable
3. Cross-check result makes sense given input size

**Success Criteria**: Result appears correct based on manual verification

## Debugging Strategy

If tests fail:

1. **Wrong sum on examples**:
   - Add debug prints to trace recursion
   - Verify type checking logic
   - Check if all branches return correct values

2. **Type errors**:
   - Verify isinstance checks are correct
   - Ensure all JSON types are handled

3. **Performance issues**:
   - Check for infinite recursion
   - Verify no redundant traversals
   - Consider iteration instead of recursion if needed

4. **File I/O errors**:
   - Verify file path is correct
   - Check file permissions
   - Ensure input format is as expected

## Quick Test Script

Create a `test_solution.py` file:

```python
from solution import sum_numbers
import json

# Test provided examples and critical edge cases
test_cases = [
    # Provided examples
    ('[1,2,3]', 6),
    ('{"a":2,"b":4}', 6),
    ('[[[3]]]', 3),
    ('{"a":{"b":4},"c":-1}', 3),
    ('{"a":[-1,1]}', 0),
    ('[-1,{"a":1}]', 0),
    ('[]', 0),
    ('{}', 0),

    # CRITICAL: Boolean handling (bool is subclass of int in Python!)
    ('[true, false, 5]', 5),
    ('{"a":true, "b":false, "c":3}', 3),
    ('[1, true, 2, false]', 3),

    # Float handling
    ('[1.5, 2.5]', 4.0),
    ('{"a":3.14, "b":2}', 5.14),
    ('[1, 2.5, -3.5]', 0.0),

    # Mixed types
    ('["string", 5, true, null, 10]', 15),
    ('[1, "text", 2.5, true, false, null, 3]', 6.5),

    # Negative numbers
    ('[-5, -10, -3]', -18),
    ('[5, -5]', 0),
]

print("Running tests...")
passed = 0
failed = 0

for json_str, expected in test_cases:
    data = json.loads(json_str)
    result = sum_numbers(data)
    # Use approximate equality for floats
    is_correct = abs(result - expected) < 0.0001 if isinstance(expected, float) else result == expected
    status = "PASS" if is_correct else "FAIL"

    if is_correct:
        passed += 1
    else:
        failed += 1

    print(f"[{status}] Input: {json_str[:40]:40} | Expected: {expected:8} | Got: {result:8}")

print(f"\nResults: {passed} passed, {failed} failed")
```

## Success Criteria Summary

The solution is correct if:
- ✓ All 8 provided examples produce correct output
- ✓ **CRITICAL**: Boolean values are correctly excluded (not counted as 1/0)
- ✓ Floating-point numbers are correctly summed (if present in input)
- ✓ Edge cases (empty, negatives, mixed types) work correctly
- ✓ Actual input.md processes without errors
- ✓ Output is a single number (integer or float)
- ✓ Execution completes in reasonable time (< 1 second)
- ✓ Manual spot-checks validate the result

## Key Differences from Original Plan

Based on the critique, the following critical improvements were made:

1. **Boolean Handling**: Added explicit tests for boolean values, which are critical because `bool` is a subclass of `int` in Python. Without proper handling, `True` and `False` would be incorrectly counted as 1 and 0.

2. **Float Support**: Added comprehensive tests for floating-point numbers, even though the problem mentions "integers". This ensures robustness.

3. **Improved Test Script**: The quick test script now includes critical edge cases (booleans, floats, negatives) beyond just the provided examples, and uses proper float comparison with tolerance.

4. **Explicit Test Ordering**: Phase 1 now explicitly calls out testing booleans as a critical step, since this is the most likely source of bugs.
