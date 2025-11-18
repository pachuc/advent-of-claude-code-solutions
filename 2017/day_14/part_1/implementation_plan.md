# Implementation Plan: Disk Defragmentation Grid Analysis

## Overview
We need to count the total number of "used" squares (1s) in a 128x128 grid where each row is derived from a knot hash of the input key combined with the row number.

## Input/Output
- **Input**: Key string `jxqlasbh` (from input.md)
- **Output**: Single integer representing total count of used squares (1s) in the grid

## Algorithm Efficiency Analysis

### Time Complexity
- 128 rows × knot hash computation per row
- Knot hash: O(64 × 256) = O(1) constant time per hash
- Hex to binary conversion: O(32) = O(1) per hash
- Bit counting: O(128) per row
- **Total**: O(128 × (knot_hash + binary_conversion + counting)) = O(128) rows, each with constant-time operations
- **Overall**: O(1) - fixed size problem (128×128 grid)

### Space Complexity
- Sparse hash: 256 integers
- Dense hash: 16 integers
- Binary string: 128 bits per row
- We can process row-by-row without storing entire grid
- **Space**: O(1) - constant space if we don't store the grid, or O(128×128) = O(16,384) if we do

### Efficiency Strategy
Since the grid is fixed size (128×128), efficiency isn't critical. However, we can optimize by:
1. Not storing the entire grid - just accumulate the count
2. Using built-in `bin()` for hex-to-binary conversion
3. Using `count('1')` on binary strings for fast bit counting

## Step-by-Step Implementation Plan

### Step 1: Import and Setup
**What to do**: Import necessary modules and set up file reading
- No external dependencies needed (pure Python)
- Read input key from `input.md`
- Strip whitespace from the key

**Files to create**: `solution.py`

### Step 2: Implement Knot Hash Algorithm
**What to do**: Copy/adapt the knot hash implementation from Day 10

**Functions needed**:
1. `initialize_list(size=256)` - Create list [0, 1, ..., 255]
2. `reverse_circular(lst, start, length)` - Reverse circular section of list
3. `parse_input_as_ascii(input_string)` - Convert string to ASCII codes + suffix [17, 31, 73, 47, 23]
4. `knot_hash_rounds(lengths, num_rounds=64, list_size=256)` - Execute 64 rounds of knot hash
5. `create_dense_hash(sparse_hash)` - XOR every 16 elements to create dense hash (256 → 16 elements)
6. `to_hex_string(dense_hash)` - Convert 16 integers to 32-char hex string
7. `compute_knot_hash(input_string)` - Main function that orchestrates above steps

**Source**: `/app/agent_workspace/2017/day_10/part_2/solution.py` (already implemented and tested)

**Action**: Copy the knot hash functions directly from Day 10 solution

**Validation**: Verify knot hash correctness with known value:
- Empty string `''` should produce hash: `a2582a3a0e66e6e86e3812dcb672a272`
- This ensures the copied implementation is correct

### Step 3: Implement Hex to Binary Conversion
**What to do**: Convert hex string to binary string (4 bits per hex character)

**Function**: `hex_to_binary(hex_string)`
- Input: Hex string of any length (primarily 32-character strings for this problem)
- Output: Binary string with 4 bits per hex character
- Implementation (character-by-character approach):
  ```python
  def hex_to_binary(hex_string):
      return ''.join(format(int(c, 16), '04b') for c in hex_string)
  ```
- **Why this approach**:
  - Explicit conversion guarantees 4 bits per character
  - Preserves leading zeros correctly
  - For 32 hex chars, produces exactly 128 bits
  - Works for any hex string length (useful for testing)

**Example conversions**:
- `'0'` → `'0000'`
- `'f'` → `'1111'`
- `'a0'` → `'10100000'`
- 32-char hash → 128-bit binary string

### Step 4: Generate Row Hash Input
**What to do**: Create input strings for each row

**Function**: `generate_row_input(key, row_number)`
- Input: key string, row number (0-127)
- Output: formatted string `{key}-{row_number}`
- Example: `jxqlasbh-0`, `jxqlasbh-1`, etc.
- Implementation:
  ```python
  def generate_row_input(key, row_number):
      return f"{key}-{row_number}"
  ```

### Step 5: Count Used Squares in Binary String
**What to do**: Count number of '1' bits in binary string

**Function**: `count_used_bits(binary_string)`
- Input: 128-character binary string
- Output: count of '1' characters
- Implementation:
  ```python
  def count_used_bits(binary_string):
      return binary_string.count('1')
  ```

**Optimization**: Python's `str.count()` is implemented in C and very fast

### Step 6: Main Computation Function
**What to do**: Orchestrate the entire computation

**Function**: `calculate_used_squares(key)`
- Pseudocode:
  ```
  total_used = 0
  for row in range(128):
      row_input = generate_row_input(key, row)
      hash_hex = compute_knot_hash(row_input)
      hash_binary = hex_to_binary(hash_hex)
      used_count = count_used_bits(hash_binary)
      total_used += used_count
  return total_used
  ```

**Why not store grid**:
- We only need the final count, not the grid itself
- Saves memory and is simpler
- If we needed the grid later (for part 2), we could refactor

### Step 7: Main Execution Block
**What to do**: Read input, run tests, and execute solution

**Implementation**:
```python
def main():
    # Read input
    with open('input.md', 'r') as f:
        key = f.read().strip()

    # Calculate result
    result = calculate_used_squares(key)

    # Output result
    print(result)
    return result

if __name__ == "__main__":
    # Run tests first to validate implementation
    print("Running tests...")
    test_knot_hash()
    test_hex_to_binary()
    test_generate_row_input()
    test_count_used_bits()
    test_example_case()
    print("\nAll tests passed!\n")

    # Compute and print final answer
    print("Computing answer for actual input...")
    result = main()
    print(f"\nFINAL ANSWER: {result}")
```

**Execution flow**:
1. Run unit tests to verify each component
2. Run integration test with example case
3. If all tests pass, compute actual answer
4. Print final answer to stdout

## Implementation Order

1. **First**: Copy knot hash functions from Day 10 (Step 2)
2. **Second**: Implement helper functions (Steps 3, 4, 5)
3. **Third**: Implement main computation function (Step 6)
4. **Fourth**: Add main execution block (Step 7)
5. **Fifth**: Add test functions (covered in test plan)

## Code Structure

```
solution.py
├── Knot Hash Functions (from Day 10)
│   ├── initialize_list()
│   ├── reverse_circular()
│   ├── parse_input_as_ascii()
│   ├── knot_hash_rounds()
│   ├── create_dense_hash()
│   ├── to_hex_string()
│   └── compute_knot_hash()
├── New Functions for Day 14
│   ├── hex_to_binary()
│   ├── generate_row_input()
│   ├── count_used_bits()
│   └── calculate_used_squares()
├── Test Functions
│   ├── test_hex_to_binary()
│   ├── test_example_case()
│   └── test_generate_row_input()
└── main()
```

## Expected Validation
- Test key `flqrgnkx` should produce `8108` used squares
- Actual input `jxqlasbh` will produce the puzzle answer

## Potential Pitfalls to Avoid

1. **Hex to binary conversion**: Ensure leading zeros are preserved (use `zfill(128)` or format with '04b')
2. **Row numbering**: Rows are 0-indexed (0 to 127, not 1 to 128)
3. **String format**: Ensure format is `{key}-{row}` with hyphen, not underscore or other delimiter
4. **Hash input**: Don't add extra whitespace or newlines to hash input
5. **Counting**: Make sure to count '1' characters, not total length
6. **Key reading**: Strip whitespace from input file

## Performance Expectations
- 128 hash computations
- Each hash takes ~1-5ms
- Total runtime: <1 second
- This is acceptable for a one-time computation
