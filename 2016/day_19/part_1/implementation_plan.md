# Implementation Plan: Elf Gift Exchange Circle

## Problem Analysis

This is a variant of the Josephus problem where:
- N elves are arranged in a circle, numbered 1 to N
- Each elf steals presents from the elf immediately to their left in the circle
  - "To their left" means the next elf in numerical order (1→2→3→...→N→1)
- When an elf has no presents, they are removed from the circle
- Turns proceed sequentially through remaining elves
- We need to find which elf remains with all presents

**Critical verification**: The problem states N=5 results in Elf 3 winning. We MUST verify our algorithm produces this result before trusting it for the actual input.

**Input size**: N = 3,017,957 (very large - requires efficient algorithm)

## Algorithm Considerations

### Approach 1: Simulation with List/Array (O(N²) - TOO SLOW)
- Using a list to track active elves
- Simulating each turn by removing eliminated elves
- **Problem**: For N ≈ 3 million, this would require ~9 trillion operations (unacceptable)

### Approach 2: Simulation with Circular Linked List (O(N) - VIABLE)
- Each node points to the next active elf
- When an elf steals, we remove the next node by updating pointers
- **Complexity**: O(N) - one pass through all elves
- **Memory**: O(N) for storing the linked list

### Approach 3: Mathematical Formula (O(log N) - OPTIMAL)
- The Josephus problem has known mathematical solutions
- For this specific variant (stealing from next neighbor), there's a pattern
- This is equivalent to Josephus(N, 2) where every 2nd person is eliminated
- **Formula**: J(N) = 2 * L + 1, where N = 2^m + L and 0 ≤ L < 2^m
- **Complexity**: O(log N) - just finding the highest power of 2

## Selected Approach

**We will implement Approach 3 (Mathematical Formula)** as the primary solution because:
1. N = 3,017,957 is very large, requiring optimal efficiency
2. The mathematical solution is O(log N) vs O(N) for simulation
3. The Josephus problem formula is well-established and correct

**We will also implement Approach 2 (Linked List)** as a verification method for smaller test cases.

## Implementation Steps

### Step 1: Read and Parse Input
- Read the input file `input.md`
- Extract the integer N from the file content
- Handle various formats:
  - Strip whitespace and newlines
  - Extract first integer found (in case file has extra text)
  - Use regex or simple parsing to be robust

**Implementation**:
```python
import re

def read_input(filename='input.md'):
    """Read and parse the input file."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    # Find first integer in the content
    match = re.search(r'\d+', content)
    if match:
        return int(match.group())
    raise ValueError("No integer found in input file")
```

### Step 2: Implement Mathematical Solution (Primary)

**Function**: `josephus_formula(n: int) -> int`

The Josephus problem with k=2 (every 2nd person eliminated) has the formula:
- Find the highest power of 2 that is ≤ N: call this 2^m
- Calculate L = N - 2^m (the remainder)
- Result = 2 * L + 1

**Steps**:
1. Find the highest power of 2 less than or equal to N
   - Use bit manipulation or logarithms
   - Method: Find m where 2^m ≤ N < 2^(m+1)
2. Calculate L = N - 2^m
3. Return 2 * L + 1

**Implementation details**:
```python
def josephus_formula(n):
    """
    Solve using Josephus problem formula for k=2.

    For the Josephus problem where every second person is eliminated:
    - Find the highest power of 2 that is <= n, call it 2^m
    - Calculate L = n - 2^m (the remainder)
    - The winner's position is: 2 * L + 1

    This formula works because the pattern resets at each power of 2.
    """
    if n == 1:
        return 1

    # Find highest power of 2 <= n
    power_of_2 = 1
    while power_of_2 * 2 <= n:
        power_of_2 *= 2

    # Calculate L (remainder after subtracting highest power of 2)
    L = n - power_of_2

    # Apply Josephus formula
    return 2 * L + 1
```

### Step 3: Implement Simulation Solution (Verification)

**Function**: `simulate_with_linked_list(n: int) -> int`

Create a circular linked list structure:
- Each node contains: elf_number, next_pointer
- Start at elf 1
- Loop: current elf eliminates next elf, move to the elf after eliminated one
- Continue until only one remains

**Steps**:
1. Create a simple Node class or use a dictionary to represent the circular structure
2. Initialize all elves 1 to N in a circle
3. Set current = 1 (start with elf 1)
4. While more than one elf remains:
   - Find the next elf after current
   - Remove that elf from the circle (update pointers)
   - Move current to the elf after the removed one
5. Return the remaining elf's number

**Implementation details**:
```python
def simulate_with_linked_list(n):
    """
    Simulate the elf gift exchange using a circular linked list.

    Each elf steals from the next elf in the circle (to their left).
    We use a dictionary to maintain the circular structure efficiently.
    """
    if n == 1:
        return 1

    # Create circular linked list using dict: elf -> next_elf
    next_elf = {i: i + 1 for i in range(1, n + 1)}
    next_elf[n] = 1  # Circle back to create the circle

    current = 1
    remaining = n

    while remaining > 1:
        # Current elf eliminates the next elf (to their left)
        eliminated = next_elf[current]
        # Update pointer to skip the eliminated elf
        next_elf[current] = next_elf[eliminated]
        # Move to the next active elf (now pointed to by current)
        current = next_elf[current]
        remaining -= 1

    return current
```

### Step 4: Main Function
1. Read input from `input.md`
2. Call `josephus_formula(n)` to get the result
3. Print/return the result

### Step 5: Code Structure

```python
import re

def read_input(filename='input.md'):
    """Read and parse the input file."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    match = re.search(r'\d+', content)
    if match:
        return int(match.group())
    raise ValueError("No integer found in input file")

def josephus_formula(n):
    """Solve using mathematical formula - O(log N)."""
    # Implementation as described above
    pass

def simulate_with_linked_list(n):
    """Solve using circular linked list simulation - O(N)."""
    # Implementation as described above
    pass

def main():
    n = read_input()
    result = josephus_formula(n)
    print(result)

if __name__ == '__main__':
    main()
```

## Performance Analysis

### Mathematical Solution
- **Time Complexity**: O(log N) - finding highest power of 2
- **Space Complexity**: O(1) - only storing a few variables
- **For N = 3,017,957**: ~22 operations (log₂ of 3 million)

### Simulation Solution
- **Time Complexity**: O(N) - one iteration per elf elimination
- **Space Complexity**: O(N) - storing the linked list structure
- **For N = 3,017,957**: ~3 million operations

## Edge Cases to Handle

1. **N = 1**: Only one elf, they win by default → Return 1
   - Both implementations should handle this explicitly
2. **N = 2**: Elf 1 takes from Elf 2 → Return 1
3. **N is a power of 2**: L = 0, result = 1
4. **Large N**: The mathematical formula handles this efficiently
5. **Input parsing**: Handle extra whitespace, newlines, or text in input file

## Verification Strategy

Before trusting the result for N = 3,017,957:
1. First verify N = 5 produces 3 (from the problem example)
2. Cross-validate formula vs simulation for N = 1 to 100
3. Test powers of 2 and other patterns
4. Only after all validations pass, trust the formula for the large input

## File Organization

- **solution.py**: Main solution file with all implementations
- **input.md**: Contains the input value
- **implementation_plan.md**: This file
- **test_plan.md**: Testing strategy
