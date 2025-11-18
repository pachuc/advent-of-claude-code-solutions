# Implementation Plan: Spreadsheet Corruption Checksum

## Problem Summary
Calculate a checksum for a spreadsheet by summing the difference between max and min values in each row.

## Algorithm Analysis

### Complexity
- **Time Complexity**: O(n * m) where n = number of rows, m = average values per row
- **Space Complexity**: O(m) for storing parsed values per row
- For the given input (16 rows × ~16 values), this is trivial and will execute instantly

### Approach
Simple iterative approach is optimal because:
1. We must examine every value at least once to find min/max
2. The input size is small (~256 total values)
3. No optimization opportunities exist for this problem structure

## Step-by-Step Implementation Plan

### Step 1: Read and Parse Input
**Goal**: Load the spreadsheet data from `input.md`

**Implementation**:
```python
# Read the file
with open('input.md', 'r') as f:
    lines = f.readlines()

# Filter out empty lines and parse
rows = []
for line in lines:
    line = line.strip()
    if line:  # Skip empty lines
        values = [int(x) for x in line.split()]
        rows.append(values)
```

**Why this approach**:
- Simple file reading handles the straightforward input format
- `strip()` handles any trailing whitespace
- `split()` without arguments handles any amount of whitespace between numbers
- Filter empty lines to avoid errors

### Step 2: Calculate Checksum
**Goal**: For each row, compute max - min and accumulate into checksum

**Implementation**:
```python
checksum = 0
for row in rows:
    max_val = max(row)
    min_val = min(row)
    checksum += (max_val - min_val)
```

**Why this approach**:
- Python's built-in `max()` and `min()` are optimized C implementations
- Direct accumulation avoids unnecessary intermediate list
- Clear and readable
- Each row is independent, making the logic straightforward

**Alternative considered**: Single pass to find both min and max
- Would save one iteration per row but adds complexity
- Not worth it for rows with ~16 values

**Alternative considered**: Build differences list then sum
```python
differences = [max(row) - min(row) for row in rows]
checksum = sum(differences)
```
- More functional style but creates unnecessary intermediate list
- Direct accumulation is more efficient

### Step 3: Complete Solution Structure

**Final code structure**:
```python
def calculate_checksum(filename):
    """Calculate spreadsheet checksum from file."""
    # Step 1: Read and parse
    rows = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                values = [int(x) for x in line.split()]
                rows.append(values)

    # Step 2: Calculate differences
    checksum = 0
    for row in rows:
        max_val = max(row)
        min_val = min(row)
        checksum += (max_val - min_val)

    return checksum

# Main execution
if __name__ == "__main__":
    result = calculate_checksum('input.md')
    print(result)
```

## Implementation Considerations

### Edge Cases Handled
1. **Empty lines**: Filtered with `if line:` check
2. **Whitespace**: Handled by `strip()` and `split()`
3. **Single value rows**: `max()` and `min()` both return the same value, difference = 0
4. **Empty file**: If the file is completely empty or has only blank lines, `rows` will be empty and checksum will be 0

### Edge Cases NOT Handled (unnecessary for this problem)
1. **Malformed input**: Assuming input is well-formed as per problem description
2. **File not found**: No special error handling needed for script
3. **Non-integer values**: Input guaranteed to be integers

### Performance Notes
- No optimization needed for this input size
- The algorithm is already optimal (must examine each value)
- Total operations: ~256 value reads + 16 max/min operations ≈ instant execution

## Alternative Approaches Considered

### Approach 1: One-liner functional style
```python
checksum = sum(max(row) - min(row) for row in rows)
```
- More concise but same complexity
- Equally valid approach

### Approach 2: Manual min/max in single pass
```python
for row in rows:
    row_min = row_max = row[0]
    for val in row[1:]:
        if val < row_min: row_min = val
        if val > row_max: row_max = val
```
- Avoids two passes but less readable
- Negligible performance difference for small rows

**Chosen approach**: Use built-in `max()` and `min()` for clarity and reliability

## Implementation Order

1. Create `solution.py` file
2. Implement file reading and parsing logic
3. Add checksum calculation with direct accumulation
4. Output final checksum
5. Test with provided example
6. Run on actual input
