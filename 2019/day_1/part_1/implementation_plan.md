# Implementation Plan: Fuel Requirement Calculator

## Problem Summary
Calculate the total fuel requirement for 100 spacecraft modules. For each module mass, apply the formula `fuel = floor(mass / 3) - 2` and sum all results.

## Algorithm Analysis

### Time Complexity
- **O(n)** where n is the number of modules (100 in this case)
- We need to iterate through each mass exactly once
- Each fuel calculation is O(1) - simple arithmetic operations
- This is optimal since we must read each value at least once

### Space Complexity
- **O(n)** to store the input masses (or O(1) if we process line by line)
- No additional data structures needed beyond storing input

### Efficiency Considerations
- With only 100 modules, efficiency is not a concern
- Even with millions of modules, O(n) is optimal since we must read each value at least once
- Integer operations are extremely fast

## Implementation Steps

### Step 1: Read Input Data
- Read the file `input.md`
- Parse each line as an integer
- Store masses in a list or process them one by one
- Handle potential empty lines gracefully (trailing newline)

```python
def read_masses(filename):
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]
```

### Step 2: Implement Fuel Calculation Function
- Apply the formula: `floor(mass / 3) - 2`
- In Python, integer division `//` naturally performs floor division for positive numbers
- **Important for Part 1**: We do NOT clamp negative values to zero. The formula is applied directly as given.

```python
def calculate_fuel(mass):
    return mass // 3 - 2
```

### Step 3: Calculate Total Fuel
- Iterate through all masses
- Apply fuel formula to each
- Sum the results

```python
def calculate_total_fuel(masses):
    return sum(calculate_fuel(mass) for mass in masses)
```

### Step 4: Main Program Flow
1. Read masses from `input.md`
2. Calculate total fuel
3. Print the result

## Complete Implementation Outline

```python
def calculate_fuel(mass):
    """Calculate fuel required for a given mass.

    Formula: floor(mass / 3) - 2
    Uses integer division for floor behavior.

    Note: For Part 1, negative results are NOT clamped to zero.
    """
    return mass // 3 - 2

def read_masses(filename):
    """Read module masses from input file.

    Args:
        filename: Path to input file with one mass per line

    Returns:
        List of integer masses
    """
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]

def calculate_total_fuel(masses):
    """Calculate total fuel for all masses."""
    return sum(calculate_fuel(mass) for mass in masses)

def main():
    # Read input
    masses = read_masses('input.md')

    # Calculate total fuel
    total_fuel = calculate_total_fuel(masses)

    # Output result
    print(total_fuel)

if __name__ == '__main__':
    main()
```

## Key Implementation Details

### Integer Division in Python
- Python's `//` operator performs floor division
- For positive numbers, `mass // 3` gives the same result as `floor(mass / 3)`
- This is more efficient than using `math.floor()` with true division

### Input Parsing
- Each line contains a single integer
- Use `strip()` to handle any whitespace/newlines
- Filter out empty lines (though input appears clean)
- The input file uses `.md` extension (unconventional for data, but required by problem setup)

### Negative Fuel Handling (Clarification)
- The formula `mass // 3 - 2` yields negative results for masses < 9
- **For Part 1**: We do NOT clamp negative values to zero - we apply the formula exactly as given
- This is confirmed by the problem statement and examples (no mention of clamping)
- The actual input contains masses ranging from ~50,000 to ~150,000, so negative/zero fuel is not a practical concern
- If clamping were needed (potentially in Part 2 or variants), we would use: `max(0, mass // 3 - 2)`

### Error Handling Note
- For this script, we assume the input file exists and is well-formed
- No explicit try/except for FileNotFoundError since:
  - This is a one-off script solving a specific problem
  - The input file is guaranteed to exist in the problem setup
  - A natural Python exception would indicate the issue clearly if it occurred

## Verification Against Examples
Before running on full input, verify against the provided examples:
- Mass 12 → fuel = 12 // 3 - 2 = 4 - 2 = 2 ✓
- Mass 14 → fuel = 14 // 3 - 2 = 4 - 2 = 2 ✓
- Mass 1969 → fuel = 1969 // 3 - 2 = 656 - 2 = 654 ✓
- Mass 100756 → fuel = 100756 // 3 - 2 = 33585 - 2 = 33583 ✓

## Input Data Characteristics
Based on examining `input.md`:
- **Count**: 100 module masses
- **First value**: 80891
- **Second value**: 109412
- **Third value**: 149508
- **Last value**: 125521
- **Range**: Approximately 50,000 to 150,000
- **Expected output range**: ~1,600,000 to ~5,000,000

## Final Output
The program will output a single integer representing the sum of all 100 fuel requirements.
