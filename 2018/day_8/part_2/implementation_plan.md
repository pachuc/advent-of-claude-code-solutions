# Implementation Plan: Tree Node Value Calculator (Part 2)

## Overview
Part 2 builds directly on Part 1's tree parsing logic. The core difference is that instead of summing all metadata entries, we need to calculate the "value" of the root node based on special rules that treat metadata as child node indexes when a node has children.

## Code Reuse Strategy
**Reuse from part_1_solution.py:**
- `parse_input()` function - completely reusable, no changes needed
- Tree parsing structure and recursion pattern - adaptable with modifications
- Input validation and bounds checking logic - reusable

**What needs to change:**
- `parse_node()` must return the node's value instead of metadata sum
- Need to track child node values in a list to support indexing
- Value calculation logic differs based on whether node has children

## Step-by-Step Implementation Plan

### Step 1: Copy and Adapt Input Parsing
- Reuse `parse_input()` function from Part 1 exactly as-is
- No changes needed - same input format

### Step 2: Redesign parse_node() Function
Modify the recursive node parser with new return semantics:

**Function signature:**
```python
def parse_node(data, index):
    """
    Returns: (new_index, node_value)
    """
```

**Algorithm within parse_node:**

1. **Read header** (same as Part 1):
   - Extract `num_children = data[index]`
   - Extract `num_metadata = data[index + 1]`
   - Advance index by 2

2. **Process children** (MODIFIED from Part 1):
   - Create empty list `child_values = []`
   - For each child (0 to num_children):
     - Recursively call `parse_node(data, index)`
     - Capture returned `(index, child_value)`
     - Append `child_value` to `child_values` list
     - Update index to new position

3. **Read metadata entries** (same as Part 1):
   - Extract metadata: `metadata = data[index:index + num_metadata]`
   - Advance index by num_metadata

4. **Calculate node value** (NEW logic):
   ```python
   if num_children == 0:
       # Leaf node: value = sum of metadata
       node_value = sum(metadata)
   else:
       # Internal node: metadata are 1-based child indexes
       node_value = 0
       for meta in metadata:
           # meta is 1-based index, convert to 0-based
           child_index = meta - 1
           # Only add if valid index (0-based)
           # This handles: meta=0 (becomes -1), meta > num_children (out of bounds)
           if 0 <= child_index < len(child_values):
               node_value += child_values[child_index]
           # Invalid indexes are skipped (metadata < 1 or > num_children)
   ```

   **Important Note:** This is a semantic change from Part 1:
   - Part 1: `parse_node` returned `(index, metadata_sum)` where metadata_sum was the sum of ALL metadata in the entire subtree
   - Part 2: `parse_node` returns `(index, node_value)` where node_value is the computed value of THIS node only, calculated according to the rules above

5. **Return** `(index, node_value)`

### Step 3: Create Main Calculation Function
Replace `calculate_license_sum()` with new function:

```python
def calculate_root_value(data):
    """
    Calculate the value of the root node.

    Args:
        data: List of integers representing the tree

    Returns:
        int: Value of the root node
    """
    final_index, root_value = parse_node(data, 0)

    # Verify all data consumed (same validation as Part 1)
    if final_index != len(data):
        raise ValueError(f"Data not fully consumed: {final_index}/{len(data)} integers processed")

    return root_value
```

### Step 4: Update main() Function
Nearly identical to Part 1, just calling the new function:
```python
def main():
    data = parse_input('input.md')
    result = calculate_root_value(data)
    print(result)
    return result
```

### Step 5: Add Docstrings and Comments
- Update all docstrings to reflect new value calculation semantics
- Add comments explaining the 1-based to 0-based index conversion
- Document the two cases (leaf vs internal node)

## Complexity Analysis

**Time Complexity:** O(n)
- Each number in input is processed exactly once
- Metadata lookups are O(1) per entry (direct list indexing)
- Total: O(n) where n is the number of integers in input (~19k)

**Space Complexity:** O(h * c)
- h = tree height (recursion depth)
- c = maximum children per node
- Need to store child values list at each recursive level
- In worst case (unbalanced tree), could be O(n) for pathological inputs
- In practice, much smaller due to balanced tree structure

**Performance Considerations:**
- Input has ~19k integers - very manageable
- Recursion depth should be reasonable (likely < 1000 levels)
- No need for optimization beyond clean recursive solution
- Python's default recursion limit (1000) should be sufficient

## Error Handling
Reuse Part 1's validation:
- Bounds checking before reading header
- Bounds checking before reading metadata
- Verify all data consumed at end
- Clear error messages for debugging (include actual values in error messages)

**Edge Cases Handled:**
- Metadata < 1 (e.g., 0): Safely ignored by index validation (becomes negative after -1 conversion)
- Metadata > num_children: Safely ignored by bounds check
- Node with 0 metadata: Returns 0 for value (sum of empty list or no valid references)

## Testing Strategy
See test_plan.md for comprehensive testing approach.

## Expected Behavior
- Should efficiently process the 19k integer input
- Calculate root node value in single pass
- Return a single integer result
- Complete in under 1 second
