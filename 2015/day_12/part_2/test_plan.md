# Testing Plan: JSON Number Summation with Red Object Filtering

## Updates Based on Critique

This plan has been revised to address the following improvements:

1. **New Critical Test**: Added Test 2.17 for non-string "red" values (e.g., numeric representations)
2. **Boolean Test**: Added Test 2.14 to ensure booleans aren't treated as numbers
3. **Null Test**: Added Test 2.13 for explicit null value handling
4. **String Variation Tests**: Added Tests 2.15 and 2.16 for case sensitivity and exact matching
5. **Clarified Explanations**: Improved rationales for Tests 2.3 and 2.7
6. **Updated Test Script**: Enhanced automated test suite with 5 additional edge case tests
7. **Performance Threshold**: Changed from < 5 seconds to < 1 second (more realistic)
8. **Validation Note**: Added reminder to verify against Advent of Code's expected result

## Testing Philosophy
Since this is a script to solve a specific problem (not production code), testing focuses on:
1. Correctness for the given input
2. Verification against provided examples
3. Edge cases that might occur in JSON structures
4. Basic validation of the filtering logic

We do NOT need:
- Extensive error handling for malformed JSON
- Performance benchmarking beyond basic validation
- Testing every possible JSON structure variation
- Production-level robustness

## Test Categories

### 1. Example Validation Tests
**Purpose**: Verify the solution matches all provided examples exactly

#### Test 1.1: Simple Array
- **Input**: `[1,2,3]`
- **Expected Output**: `6`
- **Rationale**: Basic sum with no objects, no filtering
- **What It Tests**: Array processing, number summing

#### Test 1.2: Array with Red Object
- **Input**: `[1,{"c":"red","b":2},3]`
- **Expected Output**: `4`
- **Rationale**: Object with "red" property should be ignored (including the number 2)
- **What It Tests**: Object filtering, array continues processing

#### Test 1.3: Top-Level Object with Red
- **Input**: `{"d":"red","e":[1,2,3,4],"f":5}`
- **Expected Output**: `0`
- **Rationale**: Entire object ignored, including nested array
- **What It Tests**: Top-level filtering, nested structure ignored

#### Test 1.4: Red String in Array
- **Input**: `[1,"red",5]`
- **Expected Output**: `6`
- **Rationale**: String "red" in array has no effect
- **What It Tests**: Array vs object distinction

### 2. Edge Case Tests
**Purpose**: Test boundary conditions and special cases

#### Test 2.1: Empty Structures
- **Input**: `{}`
- **Expected Output**: `0`
- **What It Tests**: Empty object handling

- **Input**: `[]`
- **Expected Output**: `0`
- **What It Tests**: Empty array handling

#### Test 2.2: Negative Numbers
- **Input**: `[-5, 10, -3]`
- **Expected Output**: `2`
- **What It Tests**: Negative numbers are summed correctly

#### Test 2.3: Nested Red Objects
- **Input**: `{"a":{"b":"red","c":5},"d":10}`
- **Expected Output**: `10`
- **Rationale**: The inner object `{"b":"red","c":5}` is filtered and returns 0. The outer object processes 0 (from "a") + 10 (from "d") = 10.
- **What It Tests**: Nested filtering doesn't affect parent object unless parent also has "red"

#### Test 2.4: Red as Object Key (Not Value)
- **Input**: `{"red":10,"blue":5}`
- **Expected Output**: `15`
- **Rationale**: "red" as a key doesn't trigger filtering, only as a value
- **What It Tests**: Key vs value distinction

#### Test 2.5: Multiple Red Values in Same Object
- **Input**: `{"a":"red","b":"red","c":10}`
- **Expected Output**: `0`
- **Rationale**: Any "red" value filters the entire object
- **What It Tests**: Multiple red detection

#### Test 2.6: Deep Nesting
- **Input**: `{"a":{"b":{"c":{"d":1}}}}`
- **Expected Output**: `1`
- **What It Tests**: Deep recursion works correctly

#### Test 2.7: Deep Nesting with Red at Bottom
- **Input**: `{"a":{"b":{"c":{"d":"red","e":10}}}}`
- **Expected Output**: `0`
- **Rationale**: The innermost object `{"d":"red","e":10}` is filtered (returns 0). The parent objects have no other numbers, so the final sum is 0.
- **What It Tests**: Filtering at various depths, propagation of zero through parents

#### Test 2.8: Mixed Arrays and Objects
- **Input**: `[1,{"a":2},3,[4,5],{"b":"red","c":6}]`
- **Expected Output**: `15` (1+2+3+4+5)
- **What It Tests**: Complex mixed structures

#### Test 2.9: Red in Nested Array Inside Object
- **Input**: `{"a":[1,"red",3],"b":5}`
- **Expected Output**: `9` (1+3+5)
- **Rationale**: Red in nested array doesn't affect parent object
- **What It Tests**: Red in array nested in object

#### Test 2.10: Case Sensitivity
- **Input**: `{"a":"Red","b":10}`
- **Expected Output**: `10`
- **Rationale**: "Red" (capital R) is not "red"
- **What It Tests**: Exact string matching

#### Test 2.11: Zero Values
- **Input**: `[0, 1, {"a":0}, 2]`
- **Expected Output**: `3` (0+1+0+2)
- **What It Tests**: Zeros are included in sum

#### Test 2.12: Floating Point Numbers
- **Input**: `[1.5, 2.5, 3.0]`
- **Expected Output**: `7.0`
- **What It Tests**: Float handling (if JSON contains floats)

#### Test 2.13: Null Values
- **Input**: `{"a": null, "b": 5, "c": null}`
- **Expected Output**: `5`
- **Rationale**: null values don't contribute to sum
- **What It Tests**: Handling of JSON null values

#### Test 2.14: Boolean Values
- **Input**: `{"a": true, "b": 5, "c": false}`
- **Expected Output**: `5`
- **Rationale**: Booleans should NOT be counted as numbers (true ≠ 1, false ≠ 0)
- **What It Tests**: Boolean handling, ensuring bool subclass of int doesn't cause issues

#### Test 2.15: Red with Spaces or Variants
- **Input**: `{"a": " red ", "b": 10}`
- **Expected Output**: `10`
- **Rationale**: Only exact string "red" triggers filtering, not variants with spaces
- **What It Tests**: Exact string matching (no fuzzy matching)

#### Test 2.16: Red with Different Case
- **Input**: `{"a": "RED", "b": 10, "c": "Red"}`
- **Expected Output**: `10`
- **Rationale**: Case-sensitive matching - only lowercase "red" filters
- **What It Tests**: Case sensitivity

#### Test 2.17: Non-String Red (Critical Test)
- **Input**: `{"a": 16711680, "b": 10}`
- **Expected Output**: `10` (the number 16711680 is 0xFF0000 in decimal - numeric representation of red)
- **Rationale**: Only the STRING "red" triggers filtering, not numeric or other representations
- **What It Tests**: Type-specific filtering - critical distinction

### 3. Main Input Validation
**Purpose**: Verify the solution works on the actual problem input

#### Test 3.1: Run on Actual Input
- **Input**: Content from `input.md`
- **Expected Output**: Unknown (must be calculated)
- **Validation Method**:
  1. Run the solution
  2. Manually verify a few sub-sections if possible
  3. Check that output is a reasonable integer
  4. Verify no errors occur during processing

#### Test 3.2: Input Structure Validation
- **Checks**:
  - JSON parses successfully
  - No exceptions during recursion
  - Completes in reasonable time (< 1 second for ~25K character JSON)
  - Output is an integer (or float that can be represented as int)

### 4. Logic Verification Tests
**Purpose**: Ensure core filtering logic is correct

#### Test 4.1: Object with Red Value Filters Everything
- **Manual Check**: An object like `{"x":"red","y":100,"z":{"a":50}}` should return 0
- **What It Tests**: Entire object and all children filtered

#### Test 4.2: Object without Red Processes Normally
- **Manual Check**: An object like `{"x":"blue","y":100}` should return 100
- **What It Tests**: Normal object processing

#### Test 4.3: Array Always Processes All Elements
- **Manual Check**: `["red","red","red",10]` should return 10
- **What It Tests**: Arrays never filter based on "red"
- **Note**: This is redundant with Test 1.4, but confirms the principle

#### Test 4.4: Only String "red" Matters
- **Manual Check**: `{"a": "red", "b": 10}` returns 0, but `{"a": 123, "b": 10}` returns 10
- **What It Tests**: Type-specific filtering - critical for correctness

## Test Execution Strategy

### Phase 1: Example Tests (High Priority)
1. Create test file with all 4 provided examples
2. Run solution on each example
3. Compare outputs - all must match exactly
4. **Pass Criteria**: 4/4 examples correct

### Phase 2: Edge Case Tests (Medium Priority)
1. Create test file with edge cases (Tests 2.1-2.12)
2. Run solution on each test case
3. Verify outputs match expected values
4. **Pass Criteria**: All edge cases pass

### Phase 3: Main Input Test (High Priority)
1. Run solution on actual input
2. Verify no errors
3. Get result (the answer to submit)
4. **Pass Criteria**: Runs successfully, produces integer output
5. **Validation**: If possible, verify the answer against Advent of Code's expected result

### Phase 4: Manual Spot Checks (Low Priority)
1. Manually inspect a few sections of the input JSON
2. Calculate expected sum for small subsections
3. Verify logic is working as expected
4. **Pass Criteria**: Spot checks are consistent with algorithm

## Test Implementation

### Automated Test Script
Create `test_solution.py`:
```python
import json
from solution import sum_numbers

def test_examples():
    tests = [
        ([1,2,3], 6),
        ([1,{"c":"red","b":2},3], 4),
        ({"d":"red","e":[1,2,3,4],"f":5}, 0),
        ([1,"red",5], 6),
    ]

    for i, (input_data, expected) in enumerate(tests, 1):
        result = sum_numbers(input_data)
        status = "PASS" if result == expected else "FAIL"
        print(f"Example {i}: {status} (expected {expected}, got {result})")

def test_edge_cases():
    tests = [
        ({}, 0, "Empty object"),
        ([], 0, "Empty array"),
        ([-5, 10, -3], 2, "Negative numbers"),
        ({"a":{"b":"red","c":5},"d":10}, 10, "Nested red object"),
        ({"red":10,"blue":5}, 15, "Red as key"),
        ({"a":"red","b":"red","c":10}, 0, "Multiple red values"),
        ({"a":{"b":{"c":{"d":1}}}}, 1, "Deep nesting"),
        ([1,{"a":2},3,[4,5],{"b":"red","c":6}], 15, "Mixed structures"),
        ({"a":[1,"red",3],"b":5}, 9, "Red in nested array"),
        ({"a":"Red","b":10}, 10, "Case sensitivity"),
        ([0, 1, {"a":0}, 2], 3, "Zero values"),
        ({"a": None, "b": 5, "c": None}, 5, "Null values"),
        ({"a": True, "b": 5, "c": False}, 5, "Boolean values"),
        ({"a": " red ", "b": 10}, 10, "Red with spaces"),
        ({"a": "RED", "b": 10}, 10, "Red uppercase"),
        ({"a": 16711680, "b": 10}, 10, "Numeric red (NOT string)"),
    ]

    for input_data, expected, description in tests:
        result = sum_numbers(input_data)
        status = "PASS" if result == expected else "FAIL"
        print(f"{description}: {status} (expected {expected}, got {result})")

if __name__ == "__main__":
    print("Running Example Tests:")
    test_examples()
    print("\nRunning Edge Case Tests:")
    test_edge_cases()
```

### Manual Testing Steps
1. Run: `python test_solution.py`
2. Verify all tests pass
3. Run: `python solution.py` (on actual input)
4. Record the output as the answer

## Success Criteria

### Must Pass (Critical)
- ✓ All 4 provided examples produce correct output
- ✓ Solution runs successfully on actual input without errors
- ✓ Output is a reasonable integer value

### Should Pass (Important)
- ✓ All edge case tests pass
- ✓ Logic verification tests confirm filtering works correctly
- ✓ Executes in reasonable time (< 5 seconds)

### Nice to Have (Optional)
- Manual spot checks confirm correctness
- Code is readable and well-commented

## Debugging Strategy
If tests fail:
1. **Example tests fail**: Core logic error - review algorithm
2. **Edge cases fail**: Boundary condition issue - check base cases
3. **Main input fails**: Likely recursion depth or unexpected data type
4. **Inconsistent results**: Check object vs array distinction carefully

## Known Limitations
- Not testing malformed JSON (assume input is valid)
- Not testing extreme depth (assume reasonable nesting)
- Not testing performance at scale
- Not testing all possible JSON structures (only relevant ones)

These limitations are acceptable for a problem-solving script.
