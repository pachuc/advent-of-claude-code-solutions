# Implementation Plan: Grid Computing Viable Pairs Count

## Problem Analysis

### Input Characteristics
- ~1,015 nodes in a grid (35 columns x 29 rows)
- Each node has: Size, Used, and Avail values in Terabytes
- Most nodes have used data in range 64-73T
- At least one large node exists (501T size, 495T used)
- At least one empty node exists (0T used)
- Total pairs to check: ~1,015 × 1,014 ≈ 1,029,210 pairs

### Complexity Analysis
- **Time Complexity Target**: O(n²) where n is number of nodes
- **Space Complexity Target**: O(n) for storing node data
- **Optimization Strategy**: Simple nested loop is acceptable given n ≈ 1,015
  - 1M+ comparisons is fast enough for modern hardware
  - No need for advanced data structures

### Algorithm Choice
A straightforward brute-force approach is optimal because:
1. The problem requires checking ALL pairs (can't skip any)
2. With ~1,015 nodes, O(n²) is perfectly acceptable
3. Each pair check is O(1) - just two integer comparisons
4. Total operations: ~1M comparisons (< 1 second runtime)

## Step-by-Step Implementation

### Step 1: Input Parsing
**File**: `solution.py`

Create a function to parse the df output:

```python
def parse_input(input_text):
    """
    Parse df output to extract node data.

    Returns:
        List of tuples: [(used, avail), (used, avail), ...]
    """
```

**Details**:
- Skip first two header lines (command prompt and column headers)
- For each data line:
  - Split by whitespace using `split()` which handles variable spacing
  - After splitting, the columns are at these indices:
    - Index 0: Filesystem (e.g., `/dev/grid/node-x0-y0`)
    - Index 1: Size (e.g., `89T`)
    - Index 2: Used (e.g., `65T`)
    - Index 3: Avail (e.g., `24T`)
    - Index 4: Use% (e.g., `73%`)
  - Extract Used (index 2) and Avail (index 3)
  - Parse integer values by removing 'T' suffix: `int(value[:-1])`
  - Store only (used, avail) - we don't need coordinates or size
- Return list of (used, avail) tuples

**Edge Cases**:
- Empty lines (skip them)
- Different spacing/formatting (split() handles variable whitespace)
- Values are always integers followed by 'T'

### Step 2: Count Viable Pairs
**File**: `solution.py`

Create a function to count viable pairs:

```python
def count_viable_pairs(nodes):
    """
    Count viable pairs where A's used data fits in B's available space.

    Args:
        nodes: List of (used, avail) tuples

    Returns:
        int: Count of viable pairs
    """
```

**Algorithm**:
```
count = 0
for i in range(len(nodes)):
    used_a, avail_a = nodes[i]

    # Skip if node A is empty
    if used_a == 0:
        continue

    for j in range(len(nodes)):
        # Skip if same node
        if i == j:
            continue

        used_b, avail_b = nodes[j]

        # Check if A's data fits in B's available space
        if used_a <= avail_b:
            count += 1

return count
```

**Optimization Notes**:
- No need to optimize further - O(n²) is fine for n=1,015
- Keep code simple and readable
- Each comparison is just two conditions and one integer comparison

### Step 3: Main Execution Flow
**File**: `solution.py`

Create main function:

```python
def main():
    # Read input file
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse nodes
    nodes = parse_input(input_text)

    # Count viable pairs
    result = count_viable_pairs(nodes)

    # Print result
    print(result)
```

### Step 4: Complete Program Structure

```python
def parse_input(input_text):
    # Implementation from Step 1
    pass

def count_viable_pairs(nodes):
    # Implementation from Step 2
    pass

def main():
    # Implementation from Step 3
    pass

if __name__ == "__main__":
    main()
```

## Data Structure Decisions

### Node Representation
**Choice**: Simple tuple `(used, avail)`

**Rationale**:
- We only need used and avail values for the algorithm
- Tuples are memory-efficient
- No need for node coordinates or size values
- No need for named fields (simple unpacking works fine)

**Alternatives Considered**:
- Dictionary with keys 'used', 'avail' - unnecessary overhead
- Custom class/namedtuple - overkill for 2 values
- Storing all fields - wastes memory for unused data

### Storage Container
**Choice**: Python list

**Rationale**:
- Order doesn't matter for the algorithm
- Simple indexing with i, j loops
- Memory efficient for ~1,015 elements
- Built-in, no imports needed

## Performance Expectations

### Time Complexity
- Parsing: O(n) where n = number of lines (~1,015)
- Counting: O(n²) where n = number of nodes (~1,015)
- Total: O(n²) ≈ 1,029,210 operations

### Expected Runtime
- Parsing: < 10ms
- Counting: < 100ms
- Total: < 200ms (well within acceptable range)

### Memory Usage
- Node storage: ~1,015 tuples × 2 integers × 8 bytes ≈ 16 KB
- Input text: ~25-30 KB
- Total: < 1 MB (negligible)

## Implementation Order

1. Create `solution.py` file
2. Implement `parse_input()` function
3. Implement `count_viable_pairs()` function
4. Implement `main()` function
5. Add `if __name__ == "__main__":` guard
6. Test with actual input

## Key Implementation Notes

1. **No need for optimization tricks** - straightforward O(n²) is fine
2. **Keep it simple** - readable code over clever optimizations
3. **Minimal error handling** - assume input is well-formed
4. **No external libraries** - use only Python builtins
5. **Direct file reading** - no need for command-line arguments
