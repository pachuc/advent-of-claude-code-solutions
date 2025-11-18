# Implementation Plan: Firewall Packet Scanner

## Problem Analysis

The core challenge is simulating a packet traveling through a firewall with oscillating scanners. The packet gets caught when it enters a layer exactly when the scanner is at position 0 (top).

### Key Insights:
1. **Scanner Oscillation Pattern**: A scanner with range `r` oscillates with a period of `2(r-1)`. It visits positions: 0, 1, ..., r-1, r-2, ..., 1, 0 (repeating).
2. **Timing**: The packet enters layer `d` at picosecond `d`.
3. **Caught Condition**: At layer depth `d`, the scanner is at position 0 if `d % (2 * (range - 1)) == 0`.
4. **Efficiency**: The input has ~40 layers with max depth 96, so O(n) solution is sufficient.

## Implementation Steps

### Step 1: Input Parsing
- Read input file line by line
- Parse each line with format "depth: range"
- Store as list of tuples: `[(depth, range), ...]`
- Handle edge cases:
  - Empty lines (skip them)
  - Whitespace around colons

**Data Structure**: `List[Tuple[int, int]]`

**Code approach**:
```python
def parse_input(filename):
    layers = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                depth, range_val = line.split(':')
                layers.append((int(depth), int(range_val)))
    return layers
```

We only need to know if the scanner is at position 0 when the packet enters, not the exact position.

**Key Insight**:
- Scanner is at position 0 when `time % (2 * (range - 1)) == 0`
- This is much faster than computing exact position

**Function signature**:
```python
def is_caught(depth: int, range_val: int) -> bool
```

**Algorithm**:
1. **CRITICAL**: Handle edge case FIRST: if `range_val == 1`, return True (always caught)
   - This avoids division by zero since period would be 0
2. Calculate period: `period = 2 * (range_val - 1)`
3. Return `depth % period == 0`

**Example**:
- Layer with depth=6, range=4: period = 2*(4-1) = 6, check: 6 % 6 == 0 → True (caught)
- Layer with depth=4, range=4: period = 6, check: 4 % 6 == 0 → False (not caught)

### Step 3: Severity Calculation
Calculate total severity by checking each layer.

**Function signature**:
```python
def calculate_severity(layers: List[Tuple[int, int]]) -> int
```

**Algorithm**:
1. Initialize `total_severity = 0`
2. For each `(depth, range_val)` in layers:
   - Check if packet is caught: `is_caught(depth, range_val)`
   - If caught: `total_severity += depth * range_val`
3. Return `total_severity`

### Step 4: Main Function
Orchestrate the solution.

**Code structure**:
```python
def main():
    # Parse input
    layers = parse_input('input.md')

    # Calculate severity
    severity = calculate_severity(layers)

    # Output result
    print(severity)

if __name__ == '__main__':
    main()
```

## Complete Algorithm Flow

1. **Read and parse input** → List of (depth, range) tuples
2. **For each layer**:
   - Determine if packet enters when scanner is at position 0
   - If yes, add `depth × range` to total severity
3. **Output total severity**

## Time Complexity Analysis

- **Parsing**: O(n) where n = number of layers (~40)
- **Severity calculation**: O(n)
- **Per-layer check**: O(1) using modulo operation
- **Overall**: O(n) - highly efficient even for large inputs

## Space Complexity

- O(n) to store the layer data
- No additional data structures needed

## Edge Cases to Handle

1. **Range = 1**: Scanner never moves, always at position 0
   - **CRITICAL**: Must check this BEFORE modulo operation to avoid division by zero (period = 0)
2. **Empty input**: Should return severity 0
3. **Depth = 0**: Packet always caught if layer exists at depth 0 (all scanners start at position 0)
   - Severity contribution is 0 × range = 0 (not special handling needed, just multiplication)
4. **Large depths/ranges**: Modulo arithmetic handles this efficiently
5. **Malformed input**: Lines without colons or non-numeric values (basic validation recommended)

## Code Organization

```
solution.py
├── parse_input(filename) → List[Tuple[int, int]]
├── is_caught(depth, range_val) → bool
├── calculate_severity(layers) → int
└── main()
```

## Optional: Scanner Position Calculator (for testing/verification only)

While not needed for the solution (since we use the optimized `is_caught`), you may want to implement this for verification:

**Function signature**:
```python
def get_scanner_position(time: int, range_val: int) -> int
```

**Algorithm**:
1. Handle edge case: if `range_val == 1`, return 0 (always at position 0)
2. Calculate period: `period = 2 * (range_val - 1)`
3. Calculate position in cycle: `t_in_cycle = time % period`
4. Determine position based on direction:
   - If `t_in_cycle < range_val`: moving down, position = `t_in_cycle`
   - Else: moving up, position = `period - t_in_cycle`

**Example verification** (range = 4, period = 6):
- t=0: 0 % 6 = 0, 0 < 4 → position 0
- t=1: 1 % 6 = 1, 1 < 4 → position 1
- t=2: 2 % 6 = 2, 2 < 4 → position 2
- t=3: 3 % 6 = 3, 3 < 4 → position 3
- t=4: 4 % 6 = 4, 4 >= 4 → position = 6-4 = 2
- t=5: 5 % 6 = 5, 5 >= 4 → position = 6-5 = 1
- t=6: 6 % 6 = 0, 0 < 4 → position 0

This matches the expected pattern: 0,1,2,3,2,1,0,...

## Important Implementation Notes

1. **Movement Timing**: The problem states "packet enters layer, then scanners move". Our solution checks scanner position at time `t` before scanners move at time `t`. Since the packet enters layer `d` at time `d`, and all scanners start at position 0 at time 0, our model is correct: we check the scanner's position at the moment of entry.

2. **Division by Zero**: Always check `range_val == 1` BEFORE computing `period` and using modulo.

3. **File Input**: The solution assumes `input.md` exists and is properly formatted. Basic error handling is recommended but not critical for this problem.

## Final Notes

- The solution is mathematically optimized using the scanner oscillation period
- No simulation needed - direct calculation for each layer
- Efficient O(n) time complexity suitable for any reasonable input size
- Clean separation of concerns: parsing, logic, and orchestration
- Critical edge case handling for range=1 prevents division by zero errors
