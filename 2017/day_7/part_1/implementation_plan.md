# Implementation Plan: Recursive Circus - Finding the Bottom Program

## Problem Analysis

We need to find the root node of a tree structure where:
- Each program can hold other programs (children)
- The bottom program (root) is not held by any other program
- Input is unordered list of program descriptions
- Each line format: `name (weight)` or `name (weight) -> child1, child2, ...`

## Algorithm Strategy

**Approach: Set Difference**
- Time Complexity: O(n) where n is number of programs
- Space Complexity: O(n) for storing program names

The most efficient approach is to use set operations:
1. Collect all program names (potential roots)
2. Collect all children names (programs that are held by others)
3. The root is in set(all_programs) - set(all_children)

## Implementation Steps

### Step 1: Input Preprocessing
- Read input (either from file or as string parameter)
- Strip leading/trailing whitespace from entire input
- Split into lines
- Filter out empty lines and whitespace-only lines
- Result: Clean list of non-empty program description lines

### Step 2: Input Parsing Setup
- Handle both line formats:
  - Simple: `name (weight)`
  - With children: `name (weight) -> child1, child2, child3`

### Step 3: Data Extraction
Create two collections:
- **all_programs**: Set of all program names encountered
- **all_children**: Set of all programs that appear as children

### Step 4: Parse Each Line
For each line:
1. Split on `->` to separate parent from children
2. Extract parent name (before the `(` character)
3. Strip whitespace from parent name
4. Add parent to `all_programs` set
5. If children exist (line contains `->` and has content after it):
   - Split the right side by commas
   - Strip whitespace from each child name
   - Add each child to `all_children` set
   - Handle edge case: `program (50) ->` with no children (treat as no children)

### Step 5: Find Root
- Compute set difference: `root_set = all_programs - all_children`
- This gives us the single program that is never a child
- Assert that exactly 1 root exists (basic sanity check)
- Extract the single element from the resulting set using `next(iter(root_set))`

### Step 6: Return Result
- Return the root program name as a string

## Edge Cases Handled

1. **Single program**: If only one program exists with no children, it's the root
2. **Whitespace variations**: Strip extra spaces from names and lines
3. **Empty lines**: Filter out before processing
4. **Different line formats**: Handle both with and without children
5. **Empty children list**: Handle `program (50) ->` (arrow but no children)
6. **Large input**: Set operations are O(n), efficient for large inputs

## Code Structure

```
Function: find_bottom_program(input_data: str) -> str
    Input: String containing all input lines (from file or direct)
    Output: String (name of bottom program)

    1. Preprocess input:
        a. Strip whitespace from input
        b. Split into lines
        c. Filter out empty/whitespace-only lines

    2. Initialize empty sets: all_programs, all_children

    3. For each line in cleaned input:
        a. Split by '->' to check for children
        b. Extract parent name (text before '(')
        c. Strip whitespace from parent name
        d. Add parent to all_programs
        e. If children exist (has '->' and content after):
            - Split children by ','
            - Strip whitespace from each child
            - Add each non-empty child to all_children

    4. Calculate root_set = all_programs - all_children

    5. Assert len(root_set) == 1 (sanity check)

    6. Extract and return: next(iter(root_set))
```

## Implementation Details

### Input Preprocessing
```python
def preprocess_input(raw_input: str) -> list[str]:
    """Clean and filter input lines."""
    lines = raw_input.strip().split('\n')
    # Filter out empty/whitespace-only lines
    lines = [line.strip() for line in lines if line.strip()]
    return lines
```

### Parsing Pattern
```python
# Split line on '->'
parts = line.split('->')

# Extract parent name: everything before '('
parent_part = parts[0]
parent_name = parent_part.split('(')[0].strip()

# If children exist (len(parts) > 1 and has content):
if len(parts) > 1 and parts[1].strip():
    children_part = parts[1]
    children = [child.strip() for child in children_part.split(',') if child.strip()]
```

### Set Operations and Root Extraction
```python
# Use sets for O(1) add and O(n) difference
all_programs = set()
all_children = set()

# After parsing
root_set = all_programs - all_children

# Sanity check: expect exactly 1 root
assert len(root_set) == 1, f"Expected 1 root, found {len(root_set)}"

# Extract the single root
root = next(iter(root_set))
```

## Performance Considerations

**Input Size**: The actual input has ~1337 lines

**Efficiency Analysis**:
- Reading lines: O(n)
- Parsing each line: O(1) average (line length is bounded)
- Set operations: O(n) for difference operation
- **Total: O(n) - optimal solution**

**Memory**: O(n) to store all program names and children names

## Alternative Approaches (Not Chosen)

1. **Build full tree structure**: O(n) time but unnecessary overhead
2. **Count references**: O(n) but requires additional bookkeeping
3. **Graph traversal**: O(n) but more complex than needed

The set difference approach is optimal because:
- Minimal data structures needed
- Single pass through data
- Clear and simple logic
- Efficient for any input size
