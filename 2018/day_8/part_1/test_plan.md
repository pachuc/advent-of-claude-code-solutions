# Testing Plan: Tree License Number Calculator

## Testing Strategy Overview

Since this is a script to solve a specific problem (not production software):
- Focus on correctness verification, not exhaustive edge case testing
- Test with provided example first
- Validate algorithm logic with hand-crafted test cases
- Verify actual input produces reasonable output
- Check for common parsing errors

## Key Updates from Critique
This plan has been updated based on feedback to include:
1. **Verified input file size** (confirmed 18,992 integers)
2. **Improved assertion messages** with descriptive f-strings showing actual vs expected
3. **Tighter performance threshold** (< 100ms instead of < 1s for O(n) algorithm)
4. **Malformed input test** to verify bounds checking works correctly
5. **Explicit test code** for all edge cases with expected values

## Test Categories

### 1. Unit Tests - Individual Functions

#### Test 1.1: Input Parsing (`parse_input`)
**Purpose**: Verify input file is correctly parsed into integer list

**Test Case 1.1.a**: Example input
```python
# Create test file with example data
test_data = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
expected = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]

result = parse_input(test_file)
assert result == expected
assert len(result) == 16
```

**Test Case 1.1.b**: Whitespace handling
```python
# Test with various whitespace (spaces, tabs, newlines)
test_data = "2  3\n0 3\t10 11  12"
# Should correctly parse regardless of whitespace type
```

**Expected Outcome**: List of integers matching input numbers in order

#### Test 1.2: Node Parsing (`parse_node`)
**Purpose**: Verify recursive node parsing logic

**Test Case 1.2.a**: Leaf node (no children)
```python
# Data: 0 3 10 11 12 (no children, 3 metadata: 10, 11, 12)
data = [0, 3, 10, 11, 12]
index = 0
new_index, metadata_sum = parse_node(data, index)

assert new_index == 5  # Consumed all data
assert metadata_sum == 33  # 10 + 11 + 12
```

**Test Case 1.2.b**: Node with one child
```python
# Parent: 1 1 ... 2 (1 child, 1 metadata: 2)
# Child: 0 1 99 (0 children, 1 metadata: 99)
data = [1, 1, 0, 1, 99, 2]
index = 0
new_index, metadata_sum = parse_node(data, index)

assert new_index == 6
assert metadata_sum == 101  # 99 + 2
```

**Test Case 1.2.c**: Full example tree
```python
# The complete example from problem
data = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
index = 0
new_index, metadata_sum = parse_node(data, index)

assert new_index == 16  # All data consumed
assert metadata_sum == 138  # Expected from problem
```

**Expected Outcome**: Correct index advancement and metadata sum accumulation

### 2. Integration Tests - Full Pipeline

#### Test 2.1: Provided Example
**Purpose**: Verify complete solution against known correct answer

**Test Data**:
```
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
```

**Tree Structure Breakdown**:
```
Node A (2 children, 3 metadata)
├── Node B (0 children, 3 metadata: 10, 11, 12)
└── Node C (1 child, 1 metadata: 2)
    └── Node D (0 children, 1 metadata: 99)
Metadata for A: 1, 1, 2
```

**Metadata Sum Calculation**:
- Node B: 10 + 11 + 12 = 33
- Node D: 99
- Node C: 2
- Node A: 1 + 1 + 2 = 4
- **Total: 33 + 99 + 2 + 4 = 138**

**Test Execution**:
```python
result = calculate_license_sum(example_data)
assert result == 138, f"Expected 138, got {result}"
```

**Expected Outcome**: Output exactly 138

#### Test 2.2: Actual Input File
**Purpose**: Verify solution runs on real input without errors

**Test Execution**:
```python
data = parse_input('input.md')
result = calculate_license_sum(data)

# Validation checks:
assert isinstance(result, int), f"Result should be integer, got {type(result)}"
assert result > 0, f"Sum should be positive, got {result}"
assert len(data) == 18992, f"Expected 18992 integers (verified from input.md), got {len(data)}"

print(f"License sum for actual input: {result}")
```

**Expected Outcome**:
- No runtime errors
- Returns a positive integer
- Completes in reasonable time (< 100ms)
- Input file contains exactly 18,992 integers (verified)
- Result should be "reasonable" (exact value unknown, but should be 4-6 digits based on ~19K input)

### 3. Edge Case Tests

#### Test 3.1: Single Leaf Node
**Purpose**: Simplest possible valid tree

**Test Data**: `0 1 42` (no children, 1 metadata: 42)

**Expected**: Sum = 42, all data consumed

```python
data = [0, 1, 42]
result = calculate_license_sum(data)
assert result == 42, f"Expected 42, got {result}"
```

#### Test 3.2: Node with Zero Metadata
**Purpose**: Verify handling of nodes with no metadata

**Test Data**: `0 0` (no children, no metadata)

**Expected**: Sum = 0, index advances by 2

```python
data = [0, 0]
result = calculate_license_sum(data)
assert result == 0, f"Expected 0, got {result}"
```

#### Test 3.3: Node with Many Metadata Entries
**Purpose**: Test metadata accumulation

**Test Data**: `0 5 1 2 3 4 5` (no children, 5 metadata entries)

**Expected**: Sum = 15 (1+2+3+4+5)

```python
data = [0, 5, 1, 2, 3, 4, 5]
result = calculate_license_sum(data)
assert result == 15, f"Expected 15, got {result}"
```

#### Test 3.4: Deep Tree (Linear Chain)
**Purpose**: Test recursion depth handling

**Test Data**:
```
1 1 1 1 1 1 0 1 10 9 8 7 6
# Chain of nodes, each with 1 child and 1 metadata
```

**Expected**: Sum = 10 + 9 + 8 + 7 + 6 = 40, no stack overflow

```python
data = [1, 1, 1, 1, 1, 1, 0, 1, 10, 9, 8, 7, 6]
result = calculate_license_sum(data)
assert result == 40, f"Expected 40, got {result}"
```

#### Test 3.5: Wide Tree (Many Children)
**Purpose**: Test handling of multiple children

**Test Data**:
```
3 1 0 1 5 0 1 10 0 1 15 20
# Parent with 3 children, each a leaf
```

**Expected**: Sum = 5 + 10 + 15 + 20 = 50

```python
data = [3, 1, 0, 1, 5, 0, 1, 10, 0, 1, 15, 20]
result = calculate_license_sum(data)
assert result == 50, f"Expected 50, got {result}"
```

#### Test 3.6: Malformed Input (Bounds Check)
**Purpose**: Verify bounds checking provides clear error messages

**Test Data**: `1 1` (claims 1 child but no child data follows)

**Expected**: Should raise ValueError with clear message

```python
data = [1, 1]
try:
    result = calculate_license_sum(data)
    assert False, "Should have raised ValueError for malformed input"
except ValueError as e:
    assert "Unexpected end of data" in str(e), f"Expected clear error message, got: {e}"
    print("✓ Bounds check works correctly")
```

### 4. Correctness Verification

#### Test 4.1: Data Consumption Check
**Purpose**: Ensure all input data is processed (no data left over or underflow)

**Implementation**:
```python
def parse_node_with_validation(data, index):
    start_index = index
    new_index, metadata_sum = parse_node(data, index)

    # Optional: track how much data this node consumed
    consumed = new_index - start_index

    return new_index, metadata_sum

# In main test:
final_index, total_sum = parse_node(data, 0)
assert final_index == len(data), f"Not all data consumed: {final_index}/{len(data)}"
```

**Expected**: For valid input, should consume exactly all data

#### Test 4.2: Manual Trace for Small Example
**Purpose**: Hand-verify the parsing logic step-by-step

**Test Data**: `1 2 0 1 10 5 7`

**Manual Trace**:
1. Index 0: Read header (1 child, 2 metadata)
2. Index 2: Parse child: `0 1 10`
   - Header: 0 children, 1 metadata
   - Metadata: 10
   - Sum: 10
   - New index: 5
3. Index 5: Read parent metadata: 5, 7
4. Parent sum: 10 (child) + 5 + 7 = 22

**Test Execution**:
```python
data = [1, 2, 0, 1, 10, 5, 7]
result = calculate_license_sum(data)
assert result == 22
```

### 5. Performance Tests

#### Test 5.1: Timing Test
**Purpose**: Ensure solution runs efficiently on large input

**Test Execution**:
```python
import time

data = parse_input('input.md')
start = time.time()
result = calculate_license_sum(data)
end = time.time()

elapsed = end - start
elapsed_ms = elapsed * 1000
print(f"Processed {len(data)} integers in {elapsed_ms:.2f}ms")

# Performance threshold: O(n) algorithm should complete in < 100ms for 19K integers
assert elapsed < 0.1, f"Performance issue: {elapsed_ms:.2f}ms (expected < 100ms)"
```

**Expected**: Complete in well under 100ms (likely 5-20ms for O(n) algorithm)

#### Test 5.2: Memory Test (Optional)
**Purpose**: Verify reasonable memory usage

**Note**: For a script, this is less critical. Just verify no obvious memory leaks or excessive allocation.

## Test Execution Order

1. **First**: Test `parse_input` with example data
2. **Second**: Test `parse_node` with simple leaf node
3. **Third**: Test `parse_node` with single-child example
4. **Fourth**: Test full example (expected: 138)
5. **Fifth**: Run edge cases (single node, zero metadata, etc.)
6. **Sixth**: Run on actual input file
7. **Finally**: Performance timing test

## Success Criteria

### Must Pass:
✓ Example test returns exactly 138
✓ All data consumed (index equals length)
✓ No runtime errors on actual input
✓ Actual input returns positive integer result

### Should Pass:
✓ Individual unit tests for parse functions
✓ Edge cases handle correctly
✓ Runs in under 1 second

### Nice to Have:
✓ Manual trace verification
✓ Data consumption validation

## Debugging Strategy

If tests fail:

1. **Wrong sum on example**:
   - Add print statements in `parse_node` to trace execution
   - Print index, header values, metadata values
   - Verify tree structure matches expected

2. **Index mismatch** (not all data consumed):
   - Track index advancement at each step
   - Verify child count and metadata count are read correctly
   - Check off-by-one errors

3. **Runtime error on actual input**:
   - Check for index out of bounds
   - Verify recursion depth isn't exceeded
   - Add assertions to catch malformed data early

## Test Implementation

Create a simple test file `test_solution.py`:

```python
from solution import parse_input, parse_node, calculate_license_sum

def test_example():
    """Test with the provided example."""
    data = [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
    result = calculate_license_sum(data)
    assert result == 138, f"Expected 138, got {result}"
    print("✓ Example test passed")

def test_leaf_node():
    """Test simple leaf node."""
    data = [0, 3, 10, 11, 12]
    result = calculate_license_sum(data)
    assert result == 33, f"Expected 33, got {result}"
    print("✓ Leaf node test passed")

def test_single_node():
    """Test single node with one metadata."""
    data = [0, 1, 42]
    result = calculate_license_sum(data)
    assert result == 42, f"Expected 42, got {result}"
    print("✓ Single node test passed")

def test_actual_input():
    """Test with actual input file."""
    data = parse_input('input.md')
    assert len(data) == 18992, f"Expected 18992 integers (verified from input.md), got {len(data)}"

    result = calculate_license_sum(data)
    assert isinstance(result, int), f"Result should be integer, got {type(result)}"
    assert result > 0, f"Result should be positive, got {result}"

    print(f"✓ Actual input test passed: {result}")

def test_malformed_input():
    """Test bounds checking on malformed input."""
    data = [1, 1]  # Claims 1 child but no child data
    try:
        result = calculate_license_sum(data)
        assert False, "Should have raised ValueError for malformed input"
    except ValueError as e:
        assert "Unexpected end of data" in str(e), f"Expected clear error message, got: {e}"
        print("✓ Malformed input test passed")

if __name__ == '__main__':
    test_example()
    test_leaf_node()
    test_single_node()
    test_malformed_input()
    test_actual_input()
    print("\nAll tests passed!")
```

## Final Verification Checklist

- [ ] Example input produces 138
- [ ] Leaf node test passes
- [ ] Single node test passes
- [ ] All edge cases pass (zero metadata, many metadata, deep tree, wide tree)
- [ ] Malformed input test passes (bounds checking works)
- [ ] Actual input runs without errors
- [ ] Actual input has exactly 18,992 integers (verified)
- [ ] Result is reasonable (positive integer)
- [ ] Performance is acceptable (< 100ms for 19K integers)
- [ ] All input data consumed (validation check in calculate_license_sum)
- [ ] Clear error messages on malformed input
