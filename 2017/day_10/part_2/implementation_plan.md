# Implementation Plan: Knot Hash Algorithm - Full Implementation (Part 2)

## Overview
Part 2 extends Part 1's single-round knot hash algorithm into a complete hash function with 64 rounds, ASCII input conversion, and hexadecimal output. The core circular list reversal logic from Part 1 can be reused.

## Reusable Components from Part 1

The following functions from `part_1_solution.py` can be **directly reused**:
- `initialize_list(size=256)` - Creates the initial list [0-255]
- `reverse_circular(lst, start, length)` - Performs circular reversal (core algorithm)

The following function needs **modification**:
- `knot_hash()` - Must support multiple rounds and state persistence

The following functions are **no longer needed**:
- `parse_input()` - Replaced with ASCII conversion logic
- `compute_result()` - Part 2 returns hex string, not product

## Step-by-Step Implementation Plan

### Step 1: Input Parsing and Conversion
**Function**: `parse_input_as_ascii(input_string)`

1. Read the input string from `input.md`
2. Strip leading/trailing whitespace using `.strip()`
3. Convert each character to its ASCII code:
   - Use `ord(char)` for each character in the string
   - Example: '1' → 49, ',' → 44
4. Create a list of ASCII codes
5. Append the standard suffix: `[17, 31, 73, 47, 23]`
6. Return the complete length sequence

**Implementation details**:
```python
def parse_input_as_ascii(input_string):
    # Strip whitespace
    clean_input = input_string.strip()

    # Convert to ASCII codes
    ascii_codes = [ord(char) for char in clean_input]

    # Append standard suffix
    suffix = [17, 31, 73, 47, 23]
    ascii_codes.extend(suffix)

    return ascii_codes
```

**Complexity**: O(n) where n is input string length (~60 characters - negligible)

### Step 2: Multi-Round Knot Hash Function
**Function**: `knot_hash_rounds(lengths, num_rounds=64, list_size=256)`

Modify Part 1's `knot_hash()` function to:

1. Initialize the list, current_position=0, skip_size=0 (same as Part 1)
2. **Key difference**: Run the algorithm for `num_rounds` iterations (64)
3. For each round:
   - Process ALL lengths in the sequence
   - **Critical**: Do NOT reset current_position or skip_size between rounds
   - Apply the same logic from Part 1:
     - Reverse circular section
     - Update position: `(current_position + length + skip_size) % list_size`
     - Increment skip_size
4. After all 64 rounds, return the final sparse hash (256-element list)

**Implementation details**:
```python
def knot_hash_rounds(lengths, num_rounds=64, list_size=256):
    # Initialize (reuse from Part 1)
    lst = initialize_list(list_size)
    current_position = 0
    skip_size = 0

    # Run multiple rounds
    for round_num in range(num_rounds):
        for length in lengths:
            # Reverse section (reuse from Part 1)
            reverse_circular(lst, current_position, length)

            # Update position
            current_position = (current_position + length + skip_size) % list_size

            # Increment skip
            skip_size += 1

    return lst
```

**Complexity**: O(1) for fixed input size - completes in milliseconds

### Step 3: Dense Hash Creation
**Function**: `create_dense_hash(sparse_hash)`

Convert 256-element sparse hash to 16-element dense hash:

1. Initialize empty list for dense hash (will have 16 elements)
2. Divide sparse hash into 16 blocks of 16 elements each
3. For each block (i from 0 to 15):
   - Extract block: `sparse_hash[i*16 : (i+1)*16]`
   - XOR all 16 numbers together:
     - Start with first element
     - XOR with each subsequent element: `result ^= element`
   - Append XOR result to dense hash
4. Return dense hash (list of 16 numbers, each 0-255)

**Implementation details** (using Pythonic approach):
```python
from functools import reduce
import operator

def create_dense_hash(sparse_hash):
    dense_hash = []
    for i in range(16):
        block = sparse_hash[i*16:(i+1)*16]
        xor_result = reduce(operator.xor, block)
        dense_hash.append(xor_result)
    return dense_hash
```

**Alternative (manual loop)**: If you prefer not to import reduce, you can manually XOR elements:
```python
def create_dense_hash(sparse_hash):
    dense_hash = []
    for i in range(16):
        block = sparse_hash[i*16:(i+1)*16]
        xor_result = block[0]
        for j in range(1, 16):
            xor_result ^= block[j]
        dense_hash.append(xor_result)
    return dense_hash
```

**Complexity**: O(1) - constant time for fixed size (256 elements)

### Step 4: Hexadecimal Conversion
**Function**: `to_hex_string(dense_hash)`

Convert 16-element dense hash to 32-character hex string:

1. Initialize empty string for result
2. For each number in dense_hash:
   - Convert to 2-digit hexadecimal string
   - Use `format(num, '02x')` to get lowercase hex with leading zeros
     - '02x' means: 0-padded, 2 digits, lowercase hex
   - Concatenate to result string
3. Return final 32-character hex string

**Implementation details**:
```python
def to_hex_string(dense_hash):
    hex_string = ''.join(format(num, '02x') for num in dense_hash)
    return hex_string
```

**Complexity**: O(1) - constant time

### Step 5: Main Function Integration
**Function**: `compute_knot_hash(input_string)`

Orchestrate all steps:

1. Parse input as ASCII codes (Step 1)
2. Run 64 rounds of knot hash (Step 2)
3. Create dense hash from sparse hash (Step 3)
4. Convert to hexadecimal string (Step 4)
5. Return the 32-character hash

**Implementation details**:
```python
def compute_knot_hash(input_string):
    # Step 1: Parse and convert to ASCII
    lengths = parse_input_as_ascii(input_string)

    # Step 2: Run 64 rounds
    sparse_hash = knot_hash_rounds(lengths, num_rounds=64)

    # Step 3: Create dense hash
    dense_hash = create_dense_hash(sparse_hash)

    # Step 4: Convert to hex
    hex_hash = to_hex_string(dense_hash)

    return hex_hash
```

### Step 6: Main Execution
```python
def main():
    # Read input
    with open('input.md', 'r') as f:
        input_string = f.read()

    # Compute hash
    result = compute_knot_hash(input_string)

    # Output
    print(result)
    return result
```

**Development Tip**: When implementing, test with the 4 provided examples first (empty string, "AoC 2017", "1,2,3", "1,2,4") before running on actual input. This provides faster debug cycles since you know the expected outputs.

## File Structure

```
solution.py
├── # Reused from Part 1
│   ├── initialize_list(size=256)
│   └── reverse_circular(lst, start, length)
│
├── # New for Part 2
│   ├── parse_input_as_ascii(input_string)
│   ├── knot_hash_rounds(lengths, num_rounds=64, list_size=256)
│   ├── create_dense_hash(sparse_hash)
│   ├── to_hex_string(dense_hash)
│   └── compute_knot_hash(input_string)
│
└── # Main
    └── main()
```

**Note**: Test functions are detailed in test_plan.md and will be added to the solution file.

## Algorithm Efficiency Analysis

**Time Complexity**: O(1) for fixed input size
- All operations (64 rounds, XOR, hex conversion) complete in milliseconds
- No performance concerns for this puzzle input

**Space Complexity**: O(1)
- Uses constant space (256-element list, ~70-element length sequence)

**Performance Expectations**:
- Expected runtime: < 100ms
- No optimization needed beyond straightforward implementation

## Critical Implementation Notes

1. **State Persistence**: The most common bug is resetting `current_position` or `skip_size` between rounds. They must persist across all 64 rounds.

2. **ASCII Conversion**: Input is treated as raw string, NOT parsed as comma-separated integers in Part 2.

3. **Standard Suffix**: Always append `[17, 31, 73, 47, 23]` after ASCII conversion.

4. **XOR Operation**: Use Python's `^` operator for bitwise XOR.

5. **Hex Formatting**: Use `format(num, '02x')` to ensure:
   - Lowercase letters (a-f)
   - Exactly 2 digits with leading zeros

6. **Whitespace Handling**: Strip whitespace from input before processing.

## Code Reuse Strategy

1. **Copy** `initialize_list()` and `reverse_circular()` directly from Part 1
2. **Adapt** the knot hash logic to support multiple rounds
3. **Add** new functions for dense hash and hex conversion
4. **Replace** integer parsing with ASCII conversion

This approach maximizes code reuse while minimizing the chance of introducing bugs.
