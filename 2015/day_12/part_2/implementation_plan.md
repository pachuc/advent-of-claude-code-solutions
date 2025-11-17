# Implementation Plan: JSON Number Summation with Red Object Filtering

## Updates Based on Critique

This plan has been revised to address the following key issues:

1. **Boolean Handling**: Added explicit check to prevent treating `True` as 1 and `False` as 0 (since bool is a subclass of int in Python)
2. **Type-Specific Filtering**: Emphasized that ONLY the string "red" triggers filtering, not numeric values or other types
3. **Error Handling**: Added basic try/except for file I/O and JSON parsing
4. **Return Type**: Changed to `float` to handle potential decimal numbers in JSON
5. **Case Sensitivity**: Clarified that only exact, case-sensitive "red" triggers filtering
6. **Additional Edge Cases**: Added edge cases for booleans, null values, and string variations of "red"

## Problem Summary
Calculate the sum of all numbers in a JSON document while ignoring any object (and all its children) that has any property with the value "red". The key distinction is that "red" in arrays has no effect - only objects with "red" property values are filtered.

## Algorithm Design

### High-Level Approach
Use a recursive depth-first traversal algorithm to process the JSON structure, applying filtering rules based on the container type (object vs array).

### Time Complexity: O(n)
- Where n is the total number of elements (objects, arrays, numbers, strings) in the JSON structure
- Each element is visited exactly once

### Space Complexity: O(d)
- Where d is the maximum depth of the JSON structure
- Space is used for the recursion call stack
- For the given input, this is reasonable as JSON structures typically don't have extreme depth

## Step-by-Step Implementation

### Step 1: Parse JSON Input
**Task**: Read and parse the JSON file
- Read the input from `input.md` (the file containing the JSON input)
- Use Python's `json.loads()` to parse the JSON string into native Python data structures
- This converts JSON objects to dicts, arrays to lists, numbers to int/float, strings to str, null to None, booleans to bool
- Basic error handling: wrap in try/except to provide clear error message if JSON is invalid

### Step 2: Design Core Recursive Function
**Task**: Create a function `sum_numbers(data)` that recursively processes JSON structures

**Function Signature**:
```python
def sum_numbers(data) -> float
# Returns float to handle potential decimal numbers in JSON
# Can be converted to int at the end if needed
```

**Logic Flow**:
```
1. If data is an integer or float:
   - Return the number

2. If data is a dict (JSON object):
   - First check if ANY value in the dict equals "red" (string comparison)
   - If "red" found: return 0 (skip entire object)
   - If no "red": recursively sum all values in the dict

3. If data is a list (JSON array):
   - Do NOT check for "red" values
   - Recursively sum all elements in the list

4. If data is any other type (string, boolean, null):
   - Return 0 (non-numeric, doesn't contribute to sum)
```

### Step 3: Implement Object Processing with Red Detection
**Task**: Handle dict (JSON object) processing

**Key Implementation Details**:
- Before processing any values, iterate through ALL values in the dict
- Check if any value equals the string "red" (exact string match, case-sensitive)
- Use: `if "red" in obj.values()` for efficient detection
  - This checks if the exact string "red" appears as any value
  - Only string "red" matters - numeric values, other types, or "Red" (capitalized) don't trigger filtering
- If found, return 0 immediately (short-circuit)
- If not found, recursively process all values and sum results

**Critical Points**:
- Only check direct property values for "red", not keys
- Only the string "red" triggers filtering, not other types with value "red"

### Step 4: Implement Array Processing
**Task**: Handle list (JSON array) processing

**Key Implementation Details**:
- No filtering needed - presence of "red" string in array is irrelevant
- Simply iterate through all elements
- Recursively process each element
- Sum all returned values

### Step 5: Implement Base Cases
**Task**: Handle primitive types

**Implementation**:
- Numbers (int, float): Return the value directly
  - **Important**: Check `not isinstance(data, bool)` first, since bool is a subclass of int in Python
  - This prevents treating True as 1 and False as 0
- Strings: Return 0 (including "red" strings in arrays)
- None (null): Return 0
- Booleans: Return 0 explicitly (should not be treated as numbers)

### Step 6: Main Program Structure
**Task**: Create the entry point

**Structure**:
```python
def main():
    try:
        # Read input file
        with open('input.md', 'r') as f:
            json_text = f.read().strip()

        # Parse JSON
        data = json.loads(json_text)

        # Calculate sum
        result = sum_numbers(data)

        # Output result (convert to int if it's a whole number)
        print(int(result) if result == int(result) else result)

    except FileNotFoundError:
        print("Error: input.md file not found")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
```

### Step 7: Handle Edge Cases
**Task**: Ensure robustness

**Edge Cases to Handle**:
- Empty objects: `{}` → sum = 0
- Empty arrays: `[]` → sum = 0
- Nested red objects: entire subtree ignored
- Red in array doesn't affect filtering
- Negative numbers: include in sum
- Deeply nested structures: recursion handles naturally
- Boolean values: should not be counted as numbers (True ≠ 1, False ≠ 0)
- Null values: contribute 0 to sum
- Only string "red" triggers filtering (case-sensitive, exact match)
- "Red", " red ", "réd", or numeric representations don't trigger filtering

## Code Structure

### File Organization
Single Python file: `solution.py`

### Function Breakdown
1. `sum_numbers(data)` - Main recursive function
2. `main()` - Entry point, handles I/O

## Pseudocode

```python
def sum_numbers(data):
    # Case 1: Number (but not boolean, since bool is subclass of int in Python)
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return data

    # Case 2: Dictionary (JSON object)
    elif isinstance(data, dict):
        # Check if any value is exactly the string "red"
        # Only string "red" triggers filtering, not other types
        if "red" in data.values():
            return 0  # Ignore entire object

        # No "red", sum all values recursively
        return sum(sum_numbers(value) for value in data.values())

    # Case 3: List (JSON array)
    elif isinstance(data, list):
        # No filtering, sum all elements recursively
        return sum(sum_numbers(item) for item in data)

    # Case 4: Other types (string, None, bool)
    else:
        return 0
```

## Optimization Considerations

### Why This Algorithm is Efficient
1. **Single Pass**: Each element visited exactly once - O(n) time
2. **Early Termination**: When "red" found in object, entire subtree skipped
3. **No Extra Storage**: Only recursion stack used - O(d) space
4. **Built-in Operations**: Uses Python's efficient `in` operator for value checking

### Input Size Analysis
- The input is a large nested JSON structure (~25K characters)
- Contains hundreds of nested objects and arrays
- Depth appears moderate (likely < 20 levels)
- O(n) time complexity handles this efficiently
- Recursion depth is manageable for typical Python stack limits

### Performance Characteristics
- **Best Case**: O(n) - must visit all elements to find sum
- **Worst Case**: O(n) - same, all elements must be checked
- **Space**: O(d) where d is depth - Python handles this well for reasonable depths
- **Expected Runtime**: < 1 second for input size

## Testing Strategy
See `test_plan.md` for comprehensive testing approach.

## Implementation Notes
- Use Python 3.x for better integer handling
- No external libraries needed beyond `json` (standard library)
- Code should be simple and readable - no premature optimization
- Type checking with `isinstance()` is clear and Pythonic
