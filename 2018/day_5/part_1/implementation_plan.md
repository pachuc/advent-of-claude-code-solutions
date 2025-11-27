# Implementation Plan: Polymer Reaction Simulation

## Updates from Critique

This plan has been updated to address the following key points from the critique:

1. **Enhanced Input Handling**: Added explicit filtering for non-alphabetic characters to handle markdown formatting and whitespace
2. **Return Value Flexibility**: Modified `react_polymer()` to optionally return both length and final polymer string for testing/debugging
3. **Input Assumptions**: Clarified assumptions about `input.md` format and character filtering
4. **Complete Code Example**: Added full integrated solution showing all components together
5. **Algorithm Walkthrough**: Added detailed table showing stack operation for example case
6. **Error Handling Note**: Explicitly stated that error handling is omitted for simplicity

## Problem Summary
Given a polymer string of ~50,000 characters containing uppercase and lowercase letters, simulate chemical reactions where adjacent units of the same letter but opposite case (polarity) destroy each other. Continue until no more reactions are possible and return the final polymer length.

## Algorithm Analysis

### Approach Options

#### Option 1: Naive Iteration (Not Recommended)
- Repeatedly scan the string from start to end
- Remove reactive pairs and restart scanning
- **Time Complexity**: O(n²) - could require n passes over the string
- **Space Complexity**: O(n) - string copies
- **Problem**: Too slow for 50,000 character input

#### Option 2: Stack-Based Solution (Recommended)
- Use a stack to track non-reacting units
- Single pass through the polymer
- **Time Complexity**: O(n) - each character processed once
- **Space Complexity**: O(n) - worst case stack size
- **Advantage**: Optimal performance for large inputs

### Selected Algorithm: Stack-Based Solution

**Key Insight**: When we encounter a new unit, we only need to check if it reacts with the most recent non-destroyed unit (top of stack). This is because:
1. All previously processed units on the stack have already been verified to not react with each other
2. Removing a reactive pair naturally brings the next potential reactive pair together

**Algorithm Steps**:
1. Initialize an empty stack
2. Iterate through each character in the polymer
3. For each character:
   - If stack is empty, push character onto stack
   - If stack is not empty, check if top of stack reacts with current character
     - If they react (same letter, different case): pop from stack (destroying both)
     - If they don't react: push current character onto stack
4. After processing all characters, the stack contains the final polymer
5. Return the size of the stack

**Reaction Check Logic**:
Two characters react if:
- They are different (one uppercase, one lowercase) AND
- They are the same letter (same when both converted to same case)

This can be implemented as:
```python
def reacts(char1, char2):
    return char1 != char2 and char1.lower() == char2.lower()
```

## Implementation Steps

### Step 1: Set Up File Structure
- Create main solution file: `solution.py`
- Import necessary modules (minimal - likely none needed)

### Step 2: Implement Helper Function
```python
def reacts(a, b):
    """
    Check if two characters react with each other.

    Args:
        a: First character
        b: Second character

    Returns:
        True if characters react (same letter, opposite polarity), False otherwise
    """
    return a != b and a.lower() == b.lower()
```

### Step 3: Implement Core Reaction Function
```python
def react_polymer(polymer, return_polymer=False):
    """
    Simulate polymer reactions until stable.

    Args:
        polymer: String representing the polymer
        return_polymer: If True, return (length, final_polymer_string), else just length

    Returns:
        Integer representing the length of the final polymer, or
        Tuple of (length, final_polymer_string) if return_polymer=True
    """
    stack = []

    for unit in polymer:
        if stack and reacts(stack[-1], unit):
            stack.pop()
        else:
            stack.append(unit)

    if return_polymer:
        return len(stack), ''.join(stack)
    return len(stack)
```

### Step 4: Implement Input Reading
```python
def read_input(filename='input.md'):
    """
    Read polymer string from input file.

    Handles markdown files by reading all content and stripping whitespace.
    Filters to only alphabetic characters to handle any formatting.

    Args:
        filename: Path to input file

    Returns:
        String containing the polymer (only alphabetic characters)
    """
    with open(filename, 'r') as f:
        content = f.read()
    # Remove all whitespace and non-alphabetic characters
    # This handles markdown formatting, newlines, etc.
    polymer = ''.join(c for c in content if c.isalpha())
    return polymer
```

### Step 5: Implement Main Function
```python
def main():
    """Main execution function."""
    polymer = read_input('input.md')
    result = react_polymer(polymer)
    print(result)

if __name__ == '__main__':
    main()
```

### Step 6: Code Organization
Organize the solution as follows:
1. Helper functions (reacts)
2. Core logic (react_polymer)
3. Input handling (read_input)
4. Main execution (main)

## Performance Considerations

### Time Complexity
- **Single pass**: O(n) where n is the length of the polymer
- Each character is pushed to stack at most once: O(n)
- Each character is popped from stack at most once: O(n)
- Total: O(n) = O(50,000) which is very efficient

### Space Complexity
- **Stack space**: O(n) in worst case (no reactions occur)
- For input like "aAbBcC" → stack will be empty (best case O(1))
- For input like "aaaBBB" → stack will have all characters (worst case O(n))
- This is acceptable for n = 50,000

### Optimization Notes
- Using a list as a stack in Python is efficient (amortized O(1) for append and pop)
- No need for string concatenation which would be O(n) per operation
- No need for multiple passes through the data
- The .lower() comparison is O(1) per character

## Edge Cases to Handle

1. **Empty polymer**: Return 0
2. **Single character**: Return 1
3. **No reactions possible**: Return original length
4. **All units react**: Return 0
5. **Cascading reactions**: Handled naturally by stack approach
6. **Case sensitivity**: Properly check both letter match and case difference
7. **Input with whitespace/newlines**: Filter to only alphabetic characters
8. **Markdown formatting**: Strip all non-alphabetic characters from input

## Input Assumptions

- The input file `input.md` may contain markdown formatting
- The polymer string may span multiple lines
- Only alphabetic characters (a-z, A-Z) are valid polymer units
- All whitespace, newlines, and other characters should be filtered out
- Error handling for file operations is intentionally omitted for simplicity (script assumes valid file path)

## Testing Strategy Integration

The implementation should be testable with:
- Simple examples from problem statement
- Edge cases (empty, single char, no reactions, all reactions)
- Large input (the actual 50,000 character input)
- Custom test cases to verify cascading reactions

## Expected Output Format

The program should output a single integer representing the final polymer length, printed to stdout.

## Complete Code Example

Here's the full integrated solution:

```python
def reacts(a, b):
    """Check if two characters react (same letter, opposite polarity)."""
    return a != b and a.lower() == b.lower()

def react_polymer(polymer, return_polymer=False):
    """
    Simulate polymer reactions until stable.

    Args:
        polymer: String representing the polymer
        return_polymer: If True, return (length, final_polymer_string)

    Returns:
        Integer length or tuple (length, final_polymer)
    """
    stack = []

    for unit in polymer:
        if stack and reacts(stack[-1], unit):
            stack.pop()
        else:
            stack.append(unit)

    if return_polymer:
        return len(stack), ''.join(stack)
    return len(stack)

def read_input(filename='input.md'):
    """Read and parse polymer from input file."""
    with open(filename, 'r') as f:
        content = f.read()
    # Filter to only alphabetic characters
    polymer = ''.join(c for c in content if c.isalpha())
    return polymer

def main():
    """Main execution function."""
    polymer = read_input('input.md')
    result = react_polymer(polymer)
    print(result)

if __name__ == '__main__':
    main()
```

## Algorithm Walkthrough Example

Let's trace through `"abBA"` to demonstrate the stack approach:

| Step | Current Unit | Stack Before | Action | Stack After |
|------|--------------|--------------|--------|-------------|
| 1 | a | [] | Push (empty stack) | [a] |
| 2 | b | [a] | Push (a and b don't react) | [a, b] |
| 3 | B | [a, b] | Pop (b and B react) | [a] |
| 4 | A | [a] | Pop (a and A react) | [] |

Final result: length = 0

This demonstrates how the stack naturally handles cascading reactions - when `bB` react and are removed, `a` becomes adjacent to `A` in the next iteration.
