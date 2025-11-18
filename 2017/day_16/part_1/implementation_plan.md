# Implementation Plan: Permutation Promenade

## Plan Updates (v2)

Based on the critique, the following changes were made:

1. **Fixed mutability consistency**: All operations (spin, exchange, partner) now modify the programs list in-place, eliminating confusion about return values
2. **Clarified edge case handling**: Documented assumption that spin values won't exceed array length (valid for AoC input)
3. **Verified input format**: Confirmed input is a single line of comma-separated moves in `input.md`
4. **Updated complete code**: Reflects in-place modifications for all three operations

## Problem Analysis

We need to simulate a dance of 16 programs (a-p) executing a sequence of moves:
- **Spin (sX)**: Rotate the last X programs to the front
- **Exchange (xA/B)**: Swap programs at positions A and B
- **Partner (pA/B)**: Swap programs named A and B

The input contains ~48K characters of comma-separated moves, which means there are likely 10,000+ individual moves to execute.

## Algorithm Considerations

### Runtime Complexity
- **Spin operation**: O(n) where n = 16 (size of program array)
- **Exchange operation**: O(1) - direct index swap
- **Partner operation**: O(n) - need to find positions of two programs
- **Total**: O(m * n) where m = number of moves, n = 16

With n fixed at 16 and m potentially being 10,000+, the overall complexity is effectively O(m).

### Data Structure Choice
Use a **list of characters** to represent program positions:
- Easy indexing for exchange operations
- Simple slicing for spin operations
- Straightforward iteration for partner operations
- List is mutable, allowing in-place modifications

## Step-by-Step Implementation Plan

### Step 1: Input Parsing
1. Read the input file (`input.md`)
2. Strip whitespace and split by comma to get individual moves
3. Store moves in a list for iteration
4. **Note**: Input is a single line of comma-separated moves

**Implementation details:**
```python
with open('input.md', 'r') as f:
    input_data = f.read().strip()
moves = input_data.split(',')
```

### Step 2: Initialize Program State
1. Create a list of 16 characters from 'a' to 'p'
2. This represents the initial positions

**Implementation details:**
```python
programs = list('abcdefghijklmnop')
```

### Step 3: Implement Spin Operation
1. Parse the move to extract X (number of programs to spin)
2. Use Python list slicing to rotate:
   - Take last X elements: `programs[-X:]`
   - Take first (n-X) elements: `programs[:-X]`
   - Concatenate: `programs[-X:] + programs[:-X]`
3. Handle edge case: if X == 0, no rotation needed
4. **Assumption**: X will not exceed len(programs) in the input (valid for AoC)

**Implementation details:**
```python
def spin(programs, x):
    if x == 0:
        return programs
    return programs[-x:] + programs[:-x]
```

**Note**: This modifies in-place using slice assignment for consistency:
```python
def spin(programs, x):
    if x == 0:
        return
    programs[:] = programs[-x:] + programs[:-x]
```

### Step 4: Implement Exchange Operation
1. Parse the move to extract positions A and B
2. Swap elements at positions A and B directly
3. Use tuple unpacking for clean swap

**Implementation details:**
```python
def exchange(programs, a, b):
    programs[a], programs[b] = programs[b], programs[a]
```

### Step 5: Implement Partner Operation
1. Parse the move to extract program names A and B
2. Find indices of programs A and B using `list.index()`
3. Swap the programs at those indices

**Implementation details:**
```python
def partner(programs, name_a, name_b):
    idx_a = programs.index(name_a)
    idx_b = programs.index(name_b)
    programs[idx_a], programs[idx_b] = programs[idx_b], programs[idx_a]
```

### Step 6: Parse and Execute Moves
1. Iterate through each move in the moves list
2. Identify move type by first character (s/x/p)
3. Parse parameters based on move type:
   - **s**: Extract number after 's'
   - **x**: Extract two numbers separated by '/'
   - **p**: Extract two characters separated by '/'
4. Call appropriate function
5. Modify programs list in-place (for exchange and partner) or reassign (for spin)

**Implementation details:**
```python
for move in moves:
    if not move:  # Skip empty strings
        continue

    if move[0] == 's':
        x = int(move[1:])
        programs = spin(programs, x)

    elif move[0] == 'x':
        parts = move[1:].split('/')
        a, b = int(parts[0]), int(parts[1])
        exchange(programs, a, b)

    elif move[0] == 'p':
        parts = move[1:].split('/')
        name_a, name_b = parts[0], parts[1]
        partner(programs, name_a, name_b)
```

### Step 7: Generate Output
1. After all moves are executed, convert the programs list to a string
2. Print or return the final arrangement

**Implementation details:**
```python
result = ''.join(programs)
print(result)
```

## Optimization Considerations

### Potential Optimizations (if needed):
1. **Pre-compile move parsing**: Parse all moves once before execution
2. **Dictionary lookup for partner**: Maintain a position map (char -> index) to avoid O(n) search
   - Update map after each operation that changes positions
   - Trade-off: O(1) lookup but O(1) update overhead

3. **Spin optimization**: Use deque with rotate() method for O(1) rotation
   - `from collections import deque`
   - `deque.rotate(x)` rotates right by x positions

### Decision:
Start with the straightforward implementation. With n=16, even O(n) operations per move are negligible. Only optimize if performance becomes an issue.

### Consistency Note:
For cleaner code, all three operations should modify the programs list in-place:
- `spin`: Use `programs[:] = programs[-x:] + programs[:-x]`
- `exchange`: Already in-place with tuple unpacking
- `partner`: Already in-place with tuple unpacking

This eliminates the need to reassign the result of spin operations.

## Complete Program Structure

```python
def spin(programs, x):
    """Rotate last x programs to the front (modifies in-place)"""
    if x == 0:
        return
    programs[:] = programs[-x:] + programs[:-x]

def exchange(programs, a, b):
    """Swap programs at positions a and b (modifies in-place)"""
    programs[a], programs[b] = programs[b], programs[a]

def partner(programs, name_a, name_b):
    """Swap programs named name_a and name_b (modifies in-place)"""
    idx_a = programs.index(name_a)
    idx_b = programs.index(name_b)
    programs[idx_a], programs[idx_b] = programs[idx_b], programs[idx_a]

def main():
    # Read input
    with open('input.md', 'r') as f:
        input_data = f.read().strip()

    # Parse moves
    moves = input_data.split(',')

    # Initialize programs
    programs = list('abcdefghijklmnop')

    # Execute each move
    for move in moves:
        if not move:  # Skip empty strings
            continue

        if move[0] == 's':
            x = int(move[1:])
            spin(programs, x)

        elif move[0] == 'x':
            parts = move[1:].split('/')
            a, b = int(parts[0]), int(parts[1])
            exchange(programs, a, b)

        elif move[0] == 'p':
            parts = move[1:].split('/')
            name_a, name_b = parts[0], parts[1]
            partner(programs, name_a, name_b)

    # Output result
    result = ''.join(programs)
    print(result)

if __name__ == '__main__':
    main()
```

## Implementation Checklist

- [ ] Read and parse input file
- [ ] Initialize program list
- [ ] Implement spin operation
- [ ] Implement exchange operation
- [ ] Implement partner operation
- [ ] Parse and execute all moves
- [ ] Generate and output final result
