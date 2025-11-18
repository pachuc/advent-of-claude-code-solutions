# Implementation Plan: Dueling Generators

## Problem Analysis

### Key Requirements
- Generate 40 million pairs of pseudo-random numbers from two generators
- Compare the lowest 16 bits of each pair
- Count matches
- Generator A: factor = 16807, start = 277
- Generator B: factor = 48271, start = 349
- Modulo: 2147483647 (2^31 - 1)

### Complexity Considerations
- **Time Complexity**: O(n) where n = 40,000,000 pairs
- **Space Complexity**: O(1) - no need to store generated values, process on-the-fly
- **Performance**: 40 million iterations is manageable in Python, but efficiency matters
  - Each iteration involves: 2 multiplications, 2 modulo operations, 1 bitwise comparison
  - Should complete in seconds on modern hardware

### Algorithm Efficiency Analysis
- **Optimizations to consider**:
  1. Use bitwise AND with 0xFFFF to extract lowest 16 bits (faster than modulo 65536)
  2. Avoid storing generated values - stream processing
  3. Pre-calculate constants
  4. Use integer operations only (no floating point)

## Step-by-Step Implementation Plan

### Step 1: Parse Input
**Goal**: Extract starting values for generators A and B

**Implementation**:
```python
def parse_input(filename):
    """
    Parse input file to extract starting values.
    Expected format:
      Generator A starts with <value>
      Generator B starts with <value>
    """
    - Read the file
    - Parse lines to extract integer values
    - Return tuple (start_a, start_b)
```

**Details**:
- Use `open()` and `readlines()` or `read()`
- Extract numbers using string parsing or regex
- Convert to integers

### Step 2: Implement Generator Function
**Goal**: Create a generator function that produces the sequence of values

**Implementation**:
```python
def generate_values(start, factor, modulo):
    """
    Generator function that yields infinite sequence of values.

    Args:
        start: Initial value
        factor: Multiplication factor (16807 for A, 48271 for B)
        modulo: Modulo value (2147483647)

    Yields:
        Next value in sequence
    """
    current = start
    while True:
        current = (current * factor) % modulo
        yield current
```

**Explanation**:
- Initialize `current` to the starting value
- In each iteration, calculate new value as `(current * factor) % modulo`
- Yield the new value and update `current` for next iteration
- The first yielded value is `(start * factor) % modulo`, NOT the start value itself

**Why generator**:
- Memory efficient - doesn't store all 40M values
- Lazy evaluation - generates on demand
- Clean, readable code with `zip()` for pairing

### Step 3: Implement Bit Comparison
**Goal**: Compare lowest 16 bits of two values

**Implementation Approach**:
We will inline the bit comparison directly in the main loop for simplicity and performance.

**Logic**:
```python
# In the counting loop:
if (value_a & 0xFFFF) == (value_b & 0xFFFF):
    count += 1
```

**Details**:
- `0xFFFF` is hexadecimal for 65535 (16 ones in binary)
- Bitwise AND extracts only the lowest 16 bits
- More efficient than `% 65536` or binary string conversion
- Inlining avoids function call overhead in tight loop

**Note**: For testing purposes, we can define a helper function `lowest_16_bits_match(a, b)` that returns `(a & 0xFFFF) == (b & 0xFFFF)` to enable unit testing of the comparison logic, but the main implementation will inline this operation.

### Step 4: Implement Main Counting Logic
**Goal**: Generate 40M pairs and count matches

**Implementation**:
```python
def count_matches(start_a, start_b, pairs=40_000_000):
    """
    Count how many pairs match in their lowest 16 bits.

    Args:
        start_a: Starting value for generator A
        start_b: Starting value for generator B
        pairs: Number of pairs to generate (default 40 million)

    Returns:
        Count of matching pairs
    """
    FACTOR_A = 16807
    FACTOR_B = 48271
    MODULO = 2147483647
    MASK_16_BIT = 0xFFFF

    gen_a = generate_values(start_a, FACTOR_A, MODULO)
    gen_b = generate_values(start_b, FACTOR_B, MODULO)

    count = 0
    for _ in range(pairs):
        value_a = next(gen_a)
        value_b = next(gen_b)
        if (value_a & MASK_16_BIT) == (value_b & MASK_16_BIT):
            count += 1

    return count
```

**Details**:
- Use `range(pairs)` for a simple counted loop
- Inline the bit comparison with `& 0xFFFF` for performance
- Simple and straightforward - no need for `zip()` or `itertools.islice()`

### Step 5: Implement Main Entry Point
**Goal**: Orchestrate the solution

**Implementation**:
```python
def main():
    """
    Main entry point for the solution.
    """
    # Read input from input.txt
    start_a, start_b = parse_input('input.txt')

    # Count matches
    result = count_matches(start_a, start_b, 40_000_000)

    # Print result
    print(result)

if __name__ == "__main__":
    main()
```

**Details**:
- Reads from hardcoded `input.txt` file (standard for Advent of Code)
- Simple, clean output of just the final count
- No need for elaborate error handling - assume well-formed input per AoC standards
- Optional: Can add timing with `time.time()` for performance monitoring during development

## Complete Solution Structure

```python
# Constants
FACTOR_A = 16807
FACTOR_B = 48271
MODULO = 2147483647
MASK_16_BIT = 0xFFFF

def parse_input(filename):
    # Implementation

def generate_values(start, factor, modulo):
    # Implementation

def count_matches(start_a, start_b, pairs=40_000_000):
    # Implementation

def main():
    # Implementation

if __name__ == "__main__":
    main()
```

## Optimization Considerations

### Current Approach Performance
- **Estimated runtime**: 5-15 seconds on modern hardware
- **Time Complexity**: O(n) where n = 40,000,000 - optimal, must check all pairs
- **Space Complexity**: O(1) - no storage of generated values

### Chosen Approach Justification
The pure Python generator-based approach is sufficient for this problem:
- Generators provide O(1) space complexity - critical for 40M values
- O(n) time complexity is optimal - we must check every pair
- Bitwise operations (`& 0xFFFF`) are efficient
- Clean, readable code that will run in acceptable time

**No further optimization needed** - this is a script to solve a specific problem, not production code requiring extreme performance tuning.

## Edge Cases Handled

1. **Integer overflow**: Python handles arbitrary precision integers automatically
2. **Modulo by zero**: Hardcoded constant, not an issue
3. **Division**: No division operations, only multiplication and modulo
4. **First value**: Each generator's first yielded value is calculated from the start value (not the start value itself)

## Expected Output
For input values A=277, B=349:
- A single integer representing the count of matches
- Should be deterministic - same input always produces same output
