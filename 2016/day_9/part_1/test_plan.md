# Test Plan: Decompression Length Calculator

## Testing Objectives

1. Verify correctness of the decompression algorithm
2. Ensure proper handling of all edge cases
3. Validate marker parsing logic
4. Confirm whitespace is ignored correctly
5. Verify non-recursive processing of nested-looking markers
6. Test performance with large inputs

## Test Categories

### 1. Basic Functionality Tests

#### Test 1.1: No Compression (Plain Text)
**Input**: `ADVENT`
**Expected Output**: `6`
**Purpose**: Verify basic character counting without any markers

#### Test 1.2: Simple Marker
**Input**: `A(1x5)BC`
**Expected Output**: `7`
**Purpose**: Test basic marker parsing and repetition calculation
**Breakdown**: 'A' (1) + 'B' repeated 5 times (5) + 'C' (1) = 7

#### Test 1.3: Marker at Start
**Input**: `(3x3)XYZ`
**Expected Output**: `9`
**Purpose**: Test marker at the beginning of string
**Breakdown**: 'XYZ' repeated 3 times = 9

#### Test 1.4: Multiple Markers
**Input**: `A(2x2)BCD(2x2)EFG`
**Expected Output**: `11`
**Purpose**: Test multiple sequential markers
**Breakdown**:
- 'A' (1)
- 'BC' repeated 2 times (4)
- 'D' (1)
- 'EF' repeated 2 times (4)
- 'G' (1)
- Total: 1+4+1+4+1 = 11

### 2. Non-Recursive Processing Tests

#### Test 2.1: Marker Within Data Section (Simple)
**Input**: `(6x1)(1x3)A`
**Expected Output**: `6`
**Purpose**: Verify that markers within data sections are treated as literals
**Breakdown**: The 6 characters '(1x3)A' are repeated 1 time = 6 characters
**Key Point**: The `(1x3)` is NOT processed as a marker

#### Test 2.2: Marker Within Data Section (Complex)
**Input**: `X(8x2)(3x3)ABCY`
**Expected Output**: `18`
**Purpose**: Verify non-recursive processing with repetition > 1
**Breakdown**:
- 'X' (1)
- '(3x3)ABC' (8 chars) repeated 2 times (16)
- 'Y' (1)
- Total: 1+16+1 = 18
**Key Point**: The `(3x3)` markers in output are NOT processed

#### Test 2.3: Nested-Looking Structure
**Input**: `(10x2)(5x2)ABCDE`
**Expected Output**: `20`
**Purpose**: Test deeply nested-looking markers
**Breakdown**: '(5x2)ABCDE' (10 chars) repeated 2 times = 20
**Key Point**: Inner marker `(5x2)` is treated as literal text

### 3. Whitespace Handling Tests

#### Test 3.1: Whitespace in Input
**Input**: `A B C`
**Expected Output**: `3`
**Purpose**: Verify spaces are ignored

#### Test 3.2: Whitespace Around Markers
**Input**: `A(2x2)BCD`
**Expected Output**: `5`
**Purpose**: Verify basic marker parsing works correctly
**Breakdown**: 'A' (1) + 'BC' repeated 2 times (4) = 5
**Note**: Simplified to avoid whitespace ambiguity. If testing whitespace specifically, it should be tested in data sections where behavior is well-defined.

#### Test 3.3: Multiple Whitespace Types
**Input**: `A\t\nB\r\nC`
**Expected Output**: `3`
**Purpose**: Test tabs, newlines, carriage returns are all ignored

### 4. Marker Parsing Edge Cases

#### Test 4.1: Large Numbers in Markers
**Input**: `(100x50)` followed by 100 'A' characters
**Expected Output**: `5000`
**Purpose**: Test parsing of multi-digit numbers
**Breakdown**: 100 characters repeated 50 times = 5000

#### Test 4.2: Single Digit Marker
**Input**: `(1x1)A`
**Expected Output**: `1`
**Purpose**: Test minimal marker values

#### Test 4.3: Marker with Repetition of 1
**Input**: `(5x1)ABCDE`
**Expected Output**: `5`
**Purpose**: Verify repetition count of 1 works correctly

#### Test 4.4: Consecutive Markers Without Text
**Input**: `(2x2)AB(3x2)CDE`
**Expected Output**: `10`
**Purpose**: Test markers immediately following data sections
**Breakdown**: 'AB' repeated 2 times (4) + 'CDE' repeated 2 times (6) = 10

### 5. Empty and Minimal Input Tests

#### Test 5.1: Empty String
**Input**: ``
**Expected Output**: `0`
**Purpose**: Test empty input handling

#### Test 5.2: Only Whitespace
**Input**: `   \n\t  `
**Expected Output**: `0`
**Purpose**: Test input containing only whitespace

#### Test 5.3: Single Character
**Input**: `A`
**Expected Output**: `1`
**Purpose**: Test minimal valid input

#### Test 5.4: Single Marker Only
**Input**: `(2x3)AB`
**Expected Output**: `6`
**Purpose**: Test input with only one marker

### 6. Complex Scenario Tests

#### Test 6.1: Long Chain of Markers
**Input**: `(1x2)A(1x2)B(1x2)C(1x2)D(1x2)E`
**Expected Output**: `10`
**Purpose**: Test many small markers in sequence
**Breakdown**: Each letter repeated 2 times = 5 * 2 = 10

#### Test 6.2: Marker at End
**Input**: `ABC(3x4)XYZ`
**Expected Output**: `15`
**Purpose**: Test marker at the end of input
**Breakdown**: 'ABC' (3) + 'XYZ' repeated 4 times (12) = 15

#### Test 6.3: Mixed Content
**Input**: `START(5x2)ABCDE(2x3)XY(1x10)ZEND`
**Expected Output**: `34`
**Purpose**: Test realistic mixed content
**Breakdown**:
- 'START' = 5 characters
- Marker `(5x2)`: next 5 chars 'ABCDE' repeated 2 times = 10
- Marker `(2x3)`: next 2 chars 'XY' repeated 3 times = 6
- Marker `(1x10)`: next 1 char 'Z' repeated 10 times = 10
- 'END' = 3 characters
- Total: 5 + 10 + 6 + 10 + 3 = **34**

### 7. Actual Input Test

#### Test 7.1: Provided Input File
**Input**: Content from `input.md`
**Expected Output**: Unknown (to be calculated)
**Purpose**: Verify solution works on actual problem input
**Validation Method**:
- Manual verification of first few markers
- Check that output is reasonable (should be significantly larger than input due to decompression)
- Can partially verify by hand-calculating first 100 characters

### 8. Additional Edge Cases

#### Test 8.0: Marker with Zero Characters
**Input**: `ABC(0x5)DEFGH`
**Expected Output**: `8`
**Purpose**: Test marker with A=0 (zero characters to repeat)
**Breakdown**: 'ABC' (3) + 0 chars × 5 times (0) + 'DEFGH' (5) = 8

#### Test 8.1: Parentheses as Literal Characters
**Input**: `(2x1)()`
**Expected Output**: `2`
**Purpose**: Test that parentheses in data section are treated as literals
**Breakdown**: '()' (2 chars) repeated 1 time = 2

#### Test 8.2: 'x' as Literal Character
**Input**: `(3x2)xYZ`
**Expected Output**: `6`
**Purpose**: Verify lowercase 'x' in data section doesn't confuse parser
**Breakdown**: 'xYZ' (3 chars) repeated 2 times = 6

#### Test 8.3: Numbers as Literal Characters
**Input**: `(5x2)12345`
**Expected Output**: `10`
**Purpose**: Test digits in data section
**Breakdown**: '12345' (5 chars) repeated 2 times = 10

#### Test 8.4: Marker Data Section Extends to End
**Input**: `ABC(5x2)DEFGH`
**Expected Output**: `13`
**Purpose**: Test marker whose data section goes to end of string
**Breakdown**: 'ABC' (3) + 'DEFGH' (5 chars) × 2 times (10) = 13

#### Test 8.5: Truly Adjacent Markers (Marker in Data)
**Input**: `(10x1)(3x2)ABCXYZ`
**Expected Output**: `10`
**Purpose**: Test that marker-like text in data section is not processed
**Breakdown**: Next 10 chars '(3x2)ABCXY' repeated 1 time = 10 chars (the '(3x2)' is literal)

## Testing Implementation Strategy

### Unit Testing Approach

Create a Python test file (`test_solution.py`) with:

```python
import pytest
from solution import calculate_decompressed_length

class TestDecompressionLength:

    def test_no_compression(self):
        assert calculate_decompressed_length('ADVENT') == 6

    def test_simple_marker(self):
        assert calculate_decompressed_length('A(1x5)BC') == 7

    # ... more test methods

    @pytest.mark.parametrize("input_str,expected", [
        ('ADVENT', 6),
        ('A(1x5)BC', 7),
        ('(3x3)XYZ', 9),
        # ... more cases
    ])
    def test_multiple_cases(self, input_str, expected):
        assert calculate_decompressed_length(input_str) == expected
```

### Manual Verification Strategy

For the actual input file:

1. **Partial Hand Calculation**
   - Calculate first 200 characters by hand
   - Verify implementation matches for this substring

2. **Sanity Checks**
   - Count number of markers in input
   - Estimate rough output size based on average repetition
   - Verify final output is in expected range

3. **Marker Validation**
   - Extract all markers using regex
   - Verify each marker is well-formed
   - Check for any malformed markers that might break parsing

### Test Execution Plan

1. **Run all unit tests**: Should all pass
2. **Run with example inputs**: Verify against provided expected outputs
3. **Run with actual input**: Get the final answer
4. **Performance check**: Verify executes in < 1 second

### Running the Tests

To execute the test suite:

```bash
# Run all tests with verbose output
pytest test_solution.py -v

# Run specific test category
pytest test_solution.py::TestDecompressionLength::test_no_compression -v

# Run the actual solution
python solution.py
```

**File structure**:
```
/app/agent_workspace/2016/day_9/part_1/
├── solution.py          # Main implementation
├── test_solution.py     # Unit tests
├── input.md            # Actual puzzle input
└── problem.md          # Problem description
```

## Expected Issues and Validation

### Potential Issues to Watch For

1. **Off-by-one errors** in position advancement
2. **Integer overflow** (unlikely in Python, but verify with large markers)
3. **Marker parsing errors** with multi-digit numbers
4. **Whitespace inside vs outside data sections**

### Success Criteria

- All provided examples produce correct output
- Edge cases handled correctly
- Actual input produces a reasonable result (likely 70,000-150,000 based on compression ratio estimation)
- No errors or exceptions during execution
- Code runs efficiently (< 100ms for actual input)

## Post-Test Validation

After getting the result for the actual input:

1. **Reasonableness Check**:
   - Input is ~5KB = ~5,000 characters
   - Based on visible markers, average expansion seems to be 10-20x
   - Expected output range: 50,000 - 100,000 characters

2. **Spot Verification**:
   - Pick 3-5 random markers from input
   - Manually verify their contribution to total length

3. **Boundary Verification**:
   - Verify first and last characters/markers are processed correctly
   - Check that all input is consumed

## Test Documentation

For each test that fails:
- Document the input
- Document expected vs actual output
- Analyze the root cause
- Document the fix applied
