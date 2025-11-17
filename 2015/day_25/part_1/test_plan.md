# Test Plan: Code Generation for Weather Machine

## Testing Objectives

1. Verify position calculation formula is correct
2. Verify code generation algorithm produces correct values
3. Validate against known sample values from the problem
4. Ensure the solution handles the actual input correctly
5. Test edge cases and boundary conditions

## Test Strategy

We'll use a bottom-up testing approach:
1. Unit tests for individual functions
2. Integration tests for combined functionality
3. Validation against problem examples
4. Final verification with actual input

## Test Cases

### 1. Position Calculation Tests

#### Test 1.1: First Position
**Input:** row=1, col=1
**Expected Position:** 1
**Rationale:** First cell in the grid

#### Test 1.2: Second Row, First Column
**Input:** row=2, col=1
**Expected Position:** 2
**Rationale:** Second position in diagonal 2

#### Test 1.3: First Row, Second Column
**Input:** row=1, col=2
**Expected Position:** 3
**Rationale:** Third position (top of diagonal 2)

#### Test 1.4: Diagonal Boundaries
**Inputs and Expected:**
- (1,5) → 15 (last of diagonal 5)
- (1,6) → 21 (last of diagonal 6)
- (6,1) → 16 (first of diagonal 6)

#### Test 1.5: Mid-Grid Position
**Input:** row=4, col=2
**Expected Position:** 12
**Rationale:** Verify formula works for interior cells

#### Test 1.6: Large Coordinates (Actual Input)
**Input:** row=2978, col=3083
**Expected Position:** 18,361,853
**Calculation:** (2978+3083-1)×(2978+3083-2)//2 + 3083 = 6060×6059//2 + 3083 = 18,358,770 + 3,083 = 18,361,853
**Rationale:** CRITICAL - Verify formula handles large numbers correctly and matches actual input

### 2. Code Generation Tests

#### Test 2.1: First Code
**Input:** position=1
**Expected Code:** 20151125
**Rationale:** Starting value

#### Test 2.2: Second Code
**Input:** position=2
**Expected Code:** 31916031
**Rationale:** (20151125 × 252533) % 33554393 = 31916031

#### Test 2.3: Sequential Generation Validation
**Verify the following sequence:**
- Position 1: 20151125
- Position 2: 31916031
- Position 3: 18749137
- Position 4: 16080970
- Position 5: 21629792

**Rationale:** Ensure iteration maintains correct order

#### Test 2.4: Grid Validation - Row 1
**Verify first row matches sample:**
- (1,1) → 20151125
- (1,2) → 18749137
- (1,3) → 17289845
- (1,4) → 30943339
- (1,5) → 10071777
- (1,6) → 33511524

#### Test 2.5: Grid Validation - Various Positions
**Verify sample grid values (practical subset):**
- (2,1) → 31916031 (position 2)
- (3,1) → 16080970 (position 4)
- (2,2) → 21629792 (position 5)
- (3,3) → 1601130 (position 13)
- (6,6) → 27995004 (position 21)

**Note:** Testing all positions from the sample grid would be comprehensive but time-consuming.
Focus on a representative subset for validation. These positions range from 2 to 21,
which execute quickly.

**Rationale:** Comprehensive validation across the grid without excessive computation time

### 3. Input Parsing Tests

#### Test 3.1: Standard Format
**Input:** "Enter the code at row 2978, column 3083."
**Expected:** (2978, 3083)
**Rationale:** Standard input format

#### Test 3.2: Format Variations
**Test with slight variations (if robust parsing desired):**
- Extra whitespace
- Newlines in input
- Period at end or not

**Note:** For this script, we only need to handle the exact format provided.

### 4. Integration Tests

#### Test 4.1: End-to-End Sample Test
**Input:** "Enter the code at row 6, column 6."
**Expected Output:** 27995004
**Rationale:** Complete flow from input to output

#### Test 4.2: Corner Case - (1,1)
**Input:** "Enter the code at row 1, column 1."
**Expected Output:** 20151125
**Rationale:** Simplest case

#### Test 4.3: Edge of Sample Grid
**Input:** "Enter the code at row 3, column 4."
**Expected Output:** 7981243
**Rationale:** Verify against known value

### 5. Performance Tests

#### Test 5.1: Large Position Performance
**Input:** row=2978, col=3083 (position = 18,361,853)
**Expected:** Completes in < 3 seconds
**Rationale:** Ensure algorithm is efficient enough for the actual input. Based on estimated 0.5-2 second runtime, 3 seconds provides reasonable margin while catching performance issues.

**Measurement approach:**
```python
import time
start = time.time()
result = solve(input_text)
elapsed = time.time() - start
print(f"Completed in {elapsed:.2f} seconds")
```

### 6. Edge Cases

#### Test 6.1: First Row (varying columns)
**Rationale:** Row=1 is a boundary condition

#### Test 6.2: First Column (varying rows)
**Rationale:** Col=1 is a boundary condition

#### Test 6.3: Equal Row and Column
**Test positions like (1,1), (2,2), (3,3), etc.**
**Rationale:** Diagonal positions may have special behavior

## Testing Implementation Approach

### Method 1: Assert-Based Testing (Recommended)
Create a test file `test_solution.py`:

```python
from solution import parse_input, calculate_position, generate_code, solve
import time

def test_position_calculations():
    """Test position calculation formula."""
    assert calculate_position(1, 1) == 1
    assert calculate_position(2, 1) == 2
    assert calculate_position(1, 2) == 3
    assert calculate_position(4, 2) == 12
    assert calculate_position(1, 5) == 15
    assert calculate_position(1, 6) == 21
    # CRITICAL: Test actual input position
    assert calculate_position(2978, 3083) == 18361853
    print("✓ Position calculation tests passed")

def test_code_generation():
    """Test code generation for small positions."""
    assert generate_code(1) == 20151125
    assert generate_code(2) == 31916031
    assert generate_code(3) == 18749137
    print("✓ Code generation tests passed")

def test_grid_values():
    """Test code generation matches sample grid values."""
    # Test multiple grid positions (practical subset)
    test_cases = [
        ((1, 1), 20151125),
        ((1, 2), 18749137),
        ((1, 3), 17289845),
        ((2, 1), 31916031),
        ((3, 3), 1601130),
        ((6, 6), 27995004),
    ]

    for (row, col), expected in test_cases:
        pos = calculate_position(row, col)
        code = generate_code(pos)
        assert code == expected, f"Failed for ({row},{col}): got {code}, expected {expected}"

    print("✓ Grid validation tests passed")

def test_input_parsing():
    """Test parsing of input format."""
    input_text = "To continue, please consult the code grid in the manual.  Enter the code at row 2978, column 3083."
    row, col = parse_input(input_text)
    assert row == 2978, f"Expected row 2978, got {row}"
    assert col == 3083, f"Expected col 3083, got {col}"
    print("✓ Input parsing test passed")

def test_performance():
    """Test that solution completes in reasonable time."""
    input_text = "Enter the code at row 2978, column 3083."
    start = time.time()
    result = solve(input_text)
    elapsed = time.time() - start
    print(f"✓ Performance test passed: {elapsed:.2f} seconds")
    assert elapsed < 3.0, f"Too slow: {elapsed:.2f} seconds (threshold: 3.0s)"
    assert isinstance(result, int), f"Result should be integer, got {type(result)}"
    print(f"  Result: {result}")

if __name__ == "__main__":
    print("Running tests...\n")
    test_position_calculations()
    test_code_generation()
    test_grid_values()
    test_input_parsing()
    test_performance()
    print("\n✓ All tests passed!")
```

### Method 2: Manual Verification (Quick Smoke Test)
Run a quick verification script for immediate feedback:

```python
# Quick smoke test - verifies basic functionality
from solution import calculate_position, generate_code

print("Quick verification:")
print(f"Position (1,1): {calculate_position(1,1)} (expected 1)")
print(f"Position (2978,3083): {calculate_position(2978,3083)} (expected 18361853)")
print(f"Code at pos 1: {generate_code(1)} (expected 20151125)")
print(f"Code at (6,6): {generate_code(calculate_position(6,6))} (expected 27995004)")
```

## Verification Checklist

- [ ] Position formula correctly maps (row, col) to sequential position
- [ ] Position (2978, 3083) calculates to exactly 18,361,853
- [ ] Position calculation verified against at least 6 sample values
- [ ] Code generation produces correct sequence for first 3 codes
- [ ] Sample grid values are correctly generated (tested 6 positions)
- [ ] Input parsing extracts correct row and column from actual input
- [ ] End-to-end test works for at least one sample input
- [ ] Solution runs in reasonable time (< 3 seconds) for actual input
- [ ] Output is a single integer (can have trailing newline from print())

## Final Validation

Before submitting the answer:

1. **Position Calculation:** Verify position for (2978, 3083) is exactly 18,361,853
2. **Sample Grid Check:** Verify at least 3 positions: (1,1)→20151125, (1,6)→33511524, (6,6)→27995004
3. **Actual Input:** Run with row=2978, col=3083 and verify:
   - Output is a positive integer
   - Completes in under 3 seconds
   - No errors or exceptions
4. **Format Check:** Ensure output is just the number (trailing newline from print() is acceptable)

## Known Good Values (Reference)

For quick validation during development:

| Row | Col | Position | Code |
|-----|-----|----------|----------|
| 1 | 1 | 1 | 20151125 |
| 1 | 2 | 3 | 18749137 |
| 2 | 1 | 2 | 31916031 |
| 4 | 2 | 12 | 32451966 |
| 6 | 6 | 21 | 27995004 |

## Success Criteria

Tests pass if:
1. All position calculations match expected values (including critical test: position 2978,3083 = 18,361,853)
2. Code generation matches all tested sample grid values (minimum 6 positions)
3. Solution completes in < 3 seconds for actual input (2978, 3083)
4. Output is a valid positive integer
5. No runtime errors or exceptions occur
