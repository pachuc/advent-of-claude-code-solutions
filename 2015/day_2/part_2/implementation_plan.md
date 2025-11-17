# Implementation Plan: Gift Ribbon Calculator

## Updates Based on Critique

This plan has been enhanced based on review feedback:

1. **Integrated testing**: Added `run_tests()` function directly in the solution for easy verification
2. **Dimension order independence**: Added explicit test to validate sorting optimization
3. **Flexible input handling**: Support command-line arguments for custom input files
4. **Clearer usage instructions**: Added explicit usage examples
5. **Acknowledged trade-offs**: Noted that sorting has overhead but provides cleaner code
6. **Python version specification**: Explicitly stated Python 3.x requirement

## Problem Analysis

Calculate the total feet of ribbon needed to wrap all presents, where each present requires:
1. **Wrapping ribbon**: Smallest perimeter of any face of the rectangular box
2. **Bow ribbon**: Volume of the box (length × width × height)

Input: 1000 lines of dimensions in format `LxWxH`

## Algorithm Complexity Analysis

### Time Complexity: O(n)
- Parse each line: O(1) per line
- Calculate 3 perimeters and find minimum: O(1) per present
- Calculate volume: O(1) per present
- Total: O(n) where n = number of presents

### Space Complexity: O(1)
- No additional data structures needed
- Process line by line, accumulate total
- Constant space regardless of input size

### Efficiency Considerations
- Input size: 1000 presents - very manageable
- Simple arithmetic operations only
- No sorting, searching, or complex data structures needed
- Linear algorithm is optimal for this problem

## Implementation Steps

### Step 1: Set up the main function structure
- Create a main function to orchestrate the solution
- Set up input file reading mechanism
- Initialize accumulator for total ribbon needed

### Step 2: Implement dimension parsing
- Read input file line by line
- Split each line by 'x' character
- Convert string values to integers
- Handle any whitespace trimming if needed
- Extract length, width, and height for each present

### Step 3: Implement wrapping ribbon calculation
- For each present, calculate three face perimeters:
  - Perimeter 1: 2 * (length + width)
  - Perimeter 2: 2 * (width + height)
  - Perimeter 3: 2 * (length + height)
- Find the minimum of these three perimeters
- This is the wrapping ribbon needed

**Optimization note**: Instead of calculating all 3 perimeters, we can find the 2 smallest dimensions and use: 2 * (smallest + second_smallest). This is mathematically equivalent and more efficient.

### Step 4: Implement bow ribbon calculation
- Calculate the volume: length × width × height
- This gives the bow ribbon needed

### Step 5: Calculate total per present
- For each present: total = wrapping_ribbon + bow_ribbon
- Accumulate this to running total

### Step 6: Output the result
- After processing all presents, output the total ribbon needed
- Format as single integer

## Code Structure

```python
def calculate_ribbon_for_present(length, width, height):
    """
    Calculate ribbon needed for a single present.

    Args:
        length, width, height: dimensions of the present

    Returns:
        Total ribbon needed (wrapping + bow)
    """
    # Wrapping ribbon: smallest perimeter
    # Optimization: use 2 smallest dimensions
    dimensions = sorted([length, width, height])
    wrapping_ribbon = 2 * (dimensions[0] + dimensions[1])

    # Bow ribbon: volume
    bow_ribbon = length * width * height

    return wrapping_ribbon + bow_ribbon

def parse_line(line):
    """
    Parse a line to extract dimensions.

    Args:
        line: string in format "LxWxH"

    Returns:
        Tuple of (length, width, height)
    """
    parts = line.strip().split('x')
    return int(parts[0]), int(parts[1]), int(parts[2])

def calculate_total_ribbon(input_file):
    """
    Calculate total ribbon needed for all presents.

    Args:
        input_file: path to input file

    Returns:
        Total feet of ribbon needed
    """
    total_ribbon = 0

    with open(input_file, 'r') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                length, width, height = parse_line(line)
                ribbon = calculate_ribbon_for_present(length, width, height)
                total_ribbon += ribbon

    return total_ribbon

def run_tests():
    """Run basic tests to verify correctness."""
    # Test example 1: 2x3x4
    assert calculate_ribbon_for_present(2, 3, 4) == 34, "Example 1 failed"

    # Test example 2: 1x1x10
    assert calculate_ribbon_for_present(1, 1, 10) == 14, "Example 2 failed"

    # Test dimension order independence
    assert calculate_ribbon_for_present(2, 3, 4) == calculate_ribbon_for_present(3, 4, 2), "Order independence failed"
    assert calculate_ribbon_for_present(2, 3, 4) == calculate_ribbon_for_present(4, 2, 3), "Order independence failed"

    # Test first three lines of actual input
    result = 0
    result += calculate_ribbon_for_present(29, 13, 26)  # 9880
    result += calculate_ribbon_for_present(11, 11, 14)  # 1738
    result += calculate_ribbon_for_present(27, 2, 5)    # 284
    assert result == 11902, f"First 3 lines failed: expected 11902, got {result}"

    print("All tests passed!")

def main():
    """Main entry point."""
    import sys

    # Check if running tests
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_tests()
        return

    # Determine input file (default or command-line argument)
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.md'

    result = calculate_total_ribbon(input_file)
    print(result)

if __name__ == '__main__':
    main()
```

## Key Implementation Details

1. **Sorting optimization**: By sorting the three dimensions, we automatically get the two smallest, which form the smallest perimeter. This eliminates the need to calculate all three perimeters. While sorting 3 elements has overhead, it provides cleaner, more maintainable code with negligible performance difference for this problem size.

2. **Single pass processing**: We read and process each present once, maintaining only a running total.

3. **Robustness**: Handle empty lines to avoid errors if the input has trailing newlines.

4. **Separation of concerns**: Split into logical functions for testability and clarity.

5. **Built-in testing**: Include a `run_tests()` function that verifies correctness with examples and first few lines of actual input. Run with `python solution.py test`.

6. **Flexible input**: Support command-line argument for input file path for easier testing with different files.

## Expected Behavior

- Parse 1000 lines of input
- For each present:
  - Extract dimensions
  - Calculate smallest perimeter (wrapping ribbon)
  - Calculate volume (bow ribbon)
  - Sum these two values
- Return total ribbon for all presents

## Performance Expectations

- Should execute in < 1 millisecond for 1000 presents
- Memory usage: negligible (constant space)
- No performance concerns with this input size

## Usage

1. **Run solution**: `python solution.py` (uses default `input.md`)
2. **Run with custom input**: `python solution.py custom_input.txt`
3. **Run tests**: `python solution.py test`

## Python Version

- Requires Python 3.x
- No external dependencies (uses only standard library)
