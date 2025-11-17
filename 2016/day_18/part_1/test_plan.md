# Testing Plan: Safe Tile Counter

## Testing Strategy

We need to verify:
1. **Correctness**: The trap generation rules are implemented correctly
2. **Edge cases**: Boundary conditions are handled properly
3. **Integration**: All components work together to produce correct output
4. **Performance**: Solution runs efficiently for the given input

**Priority Levels**:
- **CRITICAL**: Tests 3, 4, 5 (the known examples with expected outputs)
- **HIGH**: Tests 1, 2, 6 (rule verification and boundary conditions)
- **MEDIUM**: Tests 7-11 (additional edge cases)
- **LOW**: Test 12 (range validation - nice to have)

## Test Cases

### Test 1: Rule Verification - Individual Trap Conditions

**Objective**: Verify each of the four trap conditions works correctly

**Test Data**:
```python
# Condition 1: Left and center are traps, right is safe
# ^^. → trap
assert is_trap('^', '^', '.') == True

# Condition 2: Center and right are traps, left is safe
# .^^ → trap
assert is_trap('.', '^', '^') == True

# Condition 3: Only left is a trap
# ^.. → trap
assert is_trap('^', '.', '.') == True

# Condition 4: Only right is a trap
# ..^ → trap
assert is_trap('.', '.', '^') == True
```

**Expected Results**: All four conditions should return True

### Test 2: Safe Tile Conditions

**Objective**: Verify tiles that should remain safe

**Test Data**:
```python
# All safe
assert is_trap('.', '.', '.') == False

# All traps
assert is_trap('^', '^', '^') == False

# Left and right are traps, center safe
assert is_trap('^', '.', '^') == False

# Left and right safe, center trap
# This is NOT one of the trap patterns
# Wait, need to check: .^. pattern
# Left safe, center trap, right safe - not in the 4 conditions
assert is_trap('.', '^', '.') == False
```

**Expected Results**: All should return False (safe tiles)

### Test 3: Simple Example from Problem

**Objective**: Verify the example given in problem statement

**Test Data**:
```
First row: ..^^.
Expected rows:
Row 1: ..^^.
Row 2: .^^^^
Row 3: ^^..^
```

**Test Steps**:
1. Start with `..^^.`
2. Generate row 2 manually:
   - Pos 0: left='.', center='.', right='.' → safe (.)
   - Pos 1: left='.', center='.', right='^' → trap (^)
   - Pos 2: left='.', center='^', right='^' → trap (^)
   - Pos 3: left='^', center='^', right='.' → trap (^)
   - Pos 4: left='^', center='.', right='.' → trap (^)
   - Result: `.^^^^` ✓
3. Generate row 3 from `.^^^^`:
   - Pos 0: left='.', center='.', right='^' → trap (^)
   - Pos 1: left='.', center='^', right='^' → trap (^)
   - Pos 2: left='^', center='^', right='^' → safe (.)
   - Pos 3: left='^', center='^', right='^' → safe (.)
   - Pos 4: left='^', center='^', right='.' → trap (^)
   - Result: `^^..^` ✓

**Expected Results**: Generated rows match expected output

### Test 4: Safe Tile Counting - Small Example

**Objective**: Verify safe tile counting works correctly

**Test Data**:
```
First row: ..^^.
Total rows: 3
```

**Test Steps**:
1. Row 1: `..^^.` → 3 safe tiles
2. Row 2: `.^^^^` → 1 safe tile
3. Row 3: `^^..^` → 2 safe tiles
4. Total: 3 + 1 + 2 = 6 safe tiles

**Expected Result**: 6

### Test 5: Extended Example (10 Rows)

**Objective**: Verify counting over more rows

**Test Data**:
```
First row: .^^.^.^^^^
Total rows: 10
```

**Test Steps**:
1. Generate all 10 rows
2. Count safe tiles in each
3. Sum total

**Expected Result**: 38 safe tiles (as mentioned in problem)

### Test 6: Boundary Conditions

**Objective**: Verify out-of-bounds handling

**Test Data**:
```python
# First position - left is out of bounds
row = "^.."
# Pos 0: left='.', center='^', right='.' → safe
next_row = generate_next_row(row)
assert next_row[0] == '.'

# Last position - right is out of bounds
row = "..^"
# Last pos: left='.', center='^', right='.' → safe
next_row = generate_next_row(row)
assert next_row[-1] == '.'
```

**Expected Results**: Out-of-bounds treated as safe tiles

### Test 7: Single Character Row

**Objective**: Edge case with minimal input

**Test Data**:
```
First row: .
```

**Test Steps**:
1. Generate next row
   - Pos 0: left='.', center='.', right='.' → safe
   - Result: `.`

**Expected Result**: Pattern should remain `.` for all rows

### Test 8: All Traps Row

**Objective**: Test with all traps

**Test Data**:
```
First row: ^^^^
```

**Test Steps**:
1. Generate next row
   - Pos 0: left='.', center='^', right='^' → trap (^)
   - Pos 1: left='^', center='^', right='^' → safe (.)
   - Pos 2: left='^', center='^', right='^' → safe (.)
   - Pos 3: left='^', center='^', right='.' → trap (^)
   - Result: `^..^`

**Expected Result**: Correctly generates pattern with interior safe tiles

### Test 9: All Safe Tiles Row

**Objective**: Test with all safe tiles

**Test Data**:
```
First row: ....
```

**Test Steps**:
1. Generate next row
   - All positions should be safe except possibly edges
   - Check manually for each position

**Expected Result**: Should generate appropriate pattern

### Test 10: Actual Input Validation

**Objective**: Verify solution with actual input

**Test Data**: Use the provided input from input.md
- The input is in input.md on the first line
- The pattern is: `.^^^^^.^^.^^^.^...^..^^.^.^..^^^^^^^^^^..^...^^.^..^^^^..^^^^...^.^.^^^^^^^^....^..^^^^^^.^^^.^^^.^^`
- Row length: 100 characters
- Total rows: 40

**Test Steps**:
1. Run the main script: `python solution.py`
2. Verify output is a single integer
3. Verify output is in valid range: 0 < result < 4000

**Expected Results**:
- Output is a positive integer
- Output ≤ 100 × 40 = 4000 (max possible safe tiles)
- Output > 0 (should have some safe tiles for typical patterns)
- No errors or exceptions raised

### Test 11: Row Length Consistency

**Objective**: Ensure all generated rows have same length as first row

**Test Data**: Any input row

**Test Steps**:
1. Generate multiple rows
2. Check length of each generated row
3. Compare to original row length

**Expected Result**: All rows have identical length

### Test 12: Output Range Validation

**Objective**: Verify output is within valid range

**Test Data**: Any input pattern with 40 rows

**Test Steps**:
1. Generate 40 rows from any starting pattern
2. Count safe tiles
3. Verify: 0 <= safe_count <= (row_length × 40)
4. Verify: safe_count > 0 (should have at least some safe tiles for typical patterns)

**Expected Result**: Output is a valid count within bounds

## Testing Procedure

### Manual Verification Steps

Since the main script reads from `input.md` with hardcoded 40 rows, we'll test by:
1. Creating a separate test function or temporarily modifying input.md
2. Or adding a flexible test harness that accepts parameters

**Option 1: Test harness approach (recommended)**
Create a test function that can accept any starting pattern and row count:

```python
def test_with_pattern(pattern, num_rows, expected=None):
    """Helper to test with custom patterns"""
    result = count_safe_tiles(pattern, num_rows)
    print(f"Pattern: {pattern}")
    print(f"Rows: {num_rows}")
    print(f"Safe tiles: {result}")
    if expected:
        assert result == expected, f"Expected {expected}, got {result}"
    return result
```

**Test cases to run**:

1. **3-row example**:
   ```python
   test_with_pattern("..^^.", 3, expected=6)
   ```

2. **10-row example**:
   ```python
   test_with_pattern(".^^.^.^^^^", 10, expected=38)
   ```

3. **Actual input** (40 rows):
   ```python
   # Run the main script normally
   python solution.py
   # Check output is a positive integer < 4000
   ```

### Automated Testing (Optional)

For a one-off AoC solution script, comprehensive automated tests may be overkill.
However, if desired, create a test file `test_solution.py`:

```python
def test_trap_conditions():
    """Test all 4 trap conditions return True"""
    assert is_trap('^', '^', '.') == True  # Condition 1
    assert is_trap('.', '^', '^') == True  # Condition 2
    assert is_trap('^', '.', '.') == True  # Condition 3
    assert is_trap('.', '.', '^') == True  # Condition 4

def test_safe_conditions():
    """Test conditions that should produce safe tiles"""
    assert is_trap('.', '.', '.') == False  # All safe
    assert is_trap('^', '^', '^') == False  # All traps
    assert is_trap('^', '.', '^') == False  # Left and right match
    assert is_trap('.', '^', '.') == False  # Left and right match

def test_row_generation():
    """Test row generation with known example"""
    row1 = "..^^."
    row2 = generate_next_row(row1)
    assert row2 == ".^^^^", f"Expected .^^^^ but got {row2}"
    row3 = generate_next_row(row2)
    assert row3 == "^^..^", f"Expected ^^..^ but got {row3}"

def test_counting():
    """Test safe tile counting with 3-row example"""
    result = count_safe_tiles("..^^.", 3)
    assert result == 6, f"Expected 6 but got {result}"

def test_10_row_example():
    """Test the 10-row example from problem"""
    result = count_safe_tiles(".^^.^.^^^^", 10)
    assert result == 38, f"Expected 38 but got {result}"
```

**Note**: The most critical tests are the 3-row and 10-row examples, as these validate
the entire solution end-to-end with known expected outputs.

## Validation Checklist

- [ ] All four trap conditions correctly identified
- [ ] All safe conditions correctly identified
- [ ] Boundary handling (out of bounds = safe)
- [ ] Simple example `..^^.` over 3 rows produces 6 safe tiles
- [ ] 10-row example with `.^^.^.^^^^` produces 38 safe tiles
- [ ] Row length remains consistent across all generated rows
- [ ] Actual input from input.md produces valid output (0 < result < 4000)
- [ ] Code runs in reasonable time (<1 second)
- [ ] Output is single integer printed to stdout
- [ ] No crashes or errors

## Performance Verification

**Expected Performance**:
- Input size: ~100 characters
- Rows: 40
- Operations: ~4,000 character comparisons
- Expected runtime: <10ms

**Test**:
```python
import time
start = time.time()
result = count_safe_tiles(first_row, 40)
elapsed = time.time() - start
assert elapsed < 1.0  # Should be much faster
print(f"Runtime: {elapsed*1000:.2f}ms")
```

## Debugging Strategy

If tests fail:

1. **Print intermediate rows**: Display first 5-10 rows to verify pattern
2. **Manual calculation**: Verify first few rows by hand
3. **Check rule logic**: Ensure XOR or explicit conditions are correct
4. **Boundary check**: Print left/center/right for edge positions
5. **Count verification**: Print safe count for each row individually

## Success Criteria

The solution is considered correct if:
1. All manual test cases pass
2. The 3-row example (`..^^.`) produces 6 safe tiles
3. The 10-row example (`.^^.^.^^^^`) produces 38 safe tiles
4. The actual input produces a valid integer output (0 < result < 4000)
5. Performance is acceptable (<1 second)
6. Code is readable and maintainable

## Recommended Testing Workflow

For this Advent of Code solution, use this streamlined testing approach:

1. **Implement the solution** following the implementation plan
2. **Add test harness** to easily test with different patterns and row counts
3. **Verify critical examples**:
   - Test 3-row example: `..^^.` → 6 safe tiles
   - Test 10-row example: `.^^.^.^^^^` → 38 safe tiles
4. **If tests pass**: Run on actual input and submit answer
5. **If tests fail**: Debug using the debugging strategy section

This approach balances thoroughness with practicality for a single-purpose script.
