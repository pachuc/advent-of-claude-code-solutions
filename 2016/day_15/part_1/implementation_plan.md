# Implementation Plan: Disc Timing Puzzle

## Problem Analysis

This is a modular arithmetic problem where we need to find the first time T such that when a capsule is released, it passes through all rotating discs when they are at position 0.

For each disc i (1-indexed):
- The disc has `positions[i]` total positions
- At time 0, the disc is at `initial[i]`
- The capsule reaches disc i at time `T + i`
- The disc position at time `T + i` is: `(initial[i] + T + i) % positions[i]`
- We need this to equal 0

This creates a system of linear congruences:
```
(initial[1] + T + 1) % positions[1] == 0
(initial[2] + T + 2) % positions[2] == 0
...
(initial[n] + T + n) % positions[n] == 0
```

Rearranged: `T ≡ -(initial[i] + i) (mod positions[i])` for all discs i

## Approach Considerations

### Approach 1: Brute Force (Simple)
- **Algorithm**: Iterate T from 0 upward, checking all disc conditions
- **Time Complexity**: O(T_answer * n) where n is number of discs
- **Space Complexity**: O(n) for storing disc data
- **Pros**: Simple to implement, guaranteed to work
- **Cons**: Could be slow if answer is large

### Approach 2: Chinese Remainder Theorem (CRT)
- **Algorithm**: Solve system of congruences mathematically
- **Time Complexity**: O(n²) or O(n log n) depending on implementation
- **Space Complexity**: O(n)
- **Pros**: Fast for any answer size, mathematically elegant
- **Cons**: More complex implementation, requires coprime moduli for direct CRT (may need extended approach)

### Approach 3: Iterative Constraint Satisfaction (Progressive Search with LCM Stepping)
- **Algorithm**: Build constraints disc-by-disc, incrementing by LCM of processed disc positions
- **Time Complexity**: O(n * answer / growing_step) where step grows with LCM
- **Space Complexity**: O(n)
- **Pros**: Balance between simplicity and efficiency, much faster than brute force
- **Cons**: LCM can grow large, but for given input (positions 3, 5, 7, 13, 17, 19), LCM = 1,184,490 which is manageable

### Recommended Approach

For this problem, we'll use **Approach 3 (Iterative Constraint Satisfaction)** because:
1. Input size is small (6 discs in given input)
2. Positions are small numbers (3-19 in given input)
3. LCM of all positions = 3 × 5 × 7 × 13 × 17 × 19 = 1,184,490 (fits easily in Python int)
4. Balances simplicity with reasonable efficiency
5. Easier to debug and verify than full CRT implementation

## Implementation Steps

### Step 1: Input Parsing
**Goal**: Parse disc information from input file

**Details**:
- Read input file line by line
- Extract disc number, total positions, and initial position
- Use regex to parse: `Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).`
- Store in a list of tuples or dict: `(disc_num, total_positions, initial_position)`
- Validate that disc numbers are sequential starting from 1

**Data Structure**:
```python
discs = [
    (disc_num, total_positions, initial_position),
    ...
]
```

**Validation**:
- Verify disc numbers are sequential starting from 1
- Raise error or skip malformed lines

### Step 2: Define Check Function (For Verification/Testing)
**Goal**: Create a function to check if time T works for all discs

**Details**:
- Function signature: `def is_valid_time(T, discs) -> bool`
- This function is primarily for testing and verification, not used by the main algorithm
- For each disc i (1-indexed):
  - Calculate position when capsule arrives: `(initial[i] + T + i) % positions[i]`
  - If any disc is not at position 0, return False
- If all discs are at position 0, return True

**Pseudo-code**:
```python
def is_valid_time(T, discs):
    """Verify that time T satisfies all disc constraints (for testing)"""
    for disc_num, positions, initial in discs:
        capsule_arrival_time = T + disc_num
        disc_position = (initial + capsule_arrival_time) % positions
        if disc_position != 0:
            return False
    return True
```

### Step 3: Implement Optimized Search
**Goal**: Find the minimum T efficiently using incremental search with optimization

**Details**:
- Start with T = 0
- Check if current T satisfies all disc conditions
- If yes, return T (this is our answer)
- If no, increment T and continue

**Optimization Strategy**:
- Start simple: increment by 1
- For better performance, we can build up constraints:
  - First find T that satisfies disc 1
  - Then find T that satisfies discs 1 and 2 (increment by positions[1])
  - Continue building up, incrementing by LCM of satisfied disc positions

**Optimized Pseudo-code**:
```python
def find_earliest_time(discs):
    time = 0
    step = 1

    for i, (disc_num, positions, initial) in enumerate(discs):
        # Find next time that works for this disc
        while (initial + time + disc_num) % positions != 0:
            time += step

        # Update step to maintain all previous constraints
        # Use LCM, but simple multiplication works if positions are coprime
        step = lcm(step, positions)

    return time
```

### Step 4: Main Execution Flow
**Goal**: Orchestrate the solution

**Details**:
- Read input from file (or stdin)
- Parse discs
- Find earliest time
- Print result

**Structure**:
```python
def main():
    # Parse input
    discs = parse_input('input.md')

    # Find solution
    result = find_earliest_time(discs)

    # Output result
    print(result)

if __name__ == '__main__':
    main()
```

### Step 5: Add Helper Functions
**Goal**: Support functions for the main algorithm

**Required Helpers**:

1. **GCD Function** (if not using math.gcd):
   ```python
   def gcd(a, b):
       while b:
           a, b = b, a % b
       return a
   ```

2. **LCM Function** (if not using math.lcm):
   ```python
   def lcm(a, b):
       return abs(a * b) // gcd(a, b)
   ```

3. **Parse Input Function**:
   ```python
   import re

   def parse_input(filename):
       pattern = r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)\.'
       discs = []
       with open(filename) as f:
           for line in f:
               line = line.strip()
               if not line:  # Skip empty lines
                   continue
               match = re.match(pattern, line)
               if match:
                   disc_num = int(match.group(1))
                   positions = int(match.group(2))
                   initial = int(match.group(3))
                   discs.append((disc_num, positions, initial))

       # Validate disc numbers are sequential starting from 1
       for i, (disc_num, _, _) in enumerate(discs):
           if disc_num != i + 1:
               raise ValueError(f"Disc numbers must be sequential starting from 1")

       return discs
   ```

## Complete Implementation Structure

```python
import re
from math import gcd, lcm

def parse_input(filename):
    """Parse disc information from input file"""
    # Implementation from Step 5

def find_earliest_time(discs):
    """Find earliest time to press button using optimized search"""
    # Implementation from Step 3

def is_valid_time(T, discs):
    """Check if time T works for all discs (for verification)"""
    # Implementation from Step 2

def main():
    """Main execution"""
    # Implementation from Step 4

if __name__ == '__main__':
    main()
```

## Algorithm Efficiency Analysis

**Time Complexity**:
- Optimized approach: O(n * T_max / step) where step grows with LCM
- Worst case still bounded by answer value, but typically much faster
- For small inputs (n=6), this will be very fast

**Space Complexity**:
- O(n) for storing disc information
- O(1) additional space for computation

**Expected Runtime**:
- For given input (6 discs, positions 3-19), answer is likely < 1,000,000
- Should complete in milliseconds

## Edge Cases to Handle

1. **Empty input**: Return 0 or handle gracefully
2. **Single disc**: Simple modular arithmetic
3. **T = 0**: Check if 0 is valid answer
4. **Large position numbers**: LCM might grow large, but still manageable
5. **Initial position 0**: Already at slot position initially

## Implementation Notes

- **Python Version**: Target Python 3.9+ to use built-in `math.gcd` and `math.lcm`
- For older Python, implement LCM using `lcm(a,b) = a*b // gcd(a,b)`
- **Input File**: Default to reading from 'input.md' in current directory
- Keep variable names clear and meaningful
- Add minimal comments for clarity
- **Error Handling**: Basic validation for disc number sequence; crashes on file not found are acceptable for this script
- **Verification**: The `is_valid_time()` function can be included for optional result verification
