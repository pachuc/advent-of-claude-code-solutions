# Implementation Plan: Optimal Circular Seating Arrangement

## Problem Analysis
- **Problem Type**: Circular Traveling Salesman Problem (TSP) variant
- **Input Size**: 8 people (56 relationships total - 7×8 bidirectional pairs)
- **Search Space**: (8-1)!/2 = 2,520 unique circular arrangements
- **Complexity**: O(n!) - brute force permutation evaluation is feasible for n=8

## Algorithm Selection
Given the small input size (8 people), a **brute force permutation approach** is optimal:
- Runtime: O(n! × n) - generate all permutations and evaluate each
- Space: O(n) - store current arrangement and happiness mapping
- With n=8, this evaluates ~40,320 arrangements (before circular optimization)
- After fixing one person's position: 5,040 arrangements to evaluate
- This runs in milliseconds on modern hardware

Alternative approaches (dynamic programming with bitmask, branch & bound) would add complexity without meaningful performance gain for n=8.

## Implementation Steps

### Step 1: Input Parsing
**Objective**: Parse the input text and build a happiness relationship dictionary

**Implementation Details**:
1. Read the entire input file/string
2. For each line, use regex or string parsing to extract:
   - Person1 name
   - Action: "gain" or "lose"
   - Numeric value
   - Person2 name
3. Create a nested dictionary structure: `happiness[person1][person2] = value`
   - For "gain": store positive value
   - For "lose": store negative value
4. Extract unique set of all person names

**Data Structure**:
```python
happiness = {
    'Alice': {'Bob': -2, 'Carol': -62, 'David': 65, ...},
    'Bob': {'Alice': 93, 'Carol': 19, ...},
    ...
}
people = ['Alice', 'Bob', 'Carol', 'David', 'Eric', 'Frank', 'George', 'Mallory']
```

**Regex Pattern**:
```
r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.'
```

### Step 2: Happiness Calculation Function
**Objective**: Calculate total happiness for a given circular arrangement

**Implementation Details**:
1. Create function: `calculate_happiness(arrangement, happiness_map)`
2. Parameters:
   - `arrangement`: List of people in order around the table
   - `happiness_map`: The nested dictionary from Step 1
3. Algorithm:
   ```python
   total = 0
   n = len(arrangement)
   for i in range(n):
       person = arrangement[i]
       left_neighbor = arrangement[(i - 1) % n]  # Circular: wraps to end
       right_neighbor = arrangement[(i + 1) % n]  # Circular: wraps to start

       # Add happiness change from both neighbors
       total += happiness_map[person][left_neighbor]
       total += happiness_map[person][right_neighbor]

   return total
   ```
4. Note: This double-counts each relationship (once from each person's perspective), which is correct per problem specification

**Time Complexity**: O(n) per arrangement

### Step 3: Generate Permutations with Circular Optimization
**Objective**: Generate all unique circular arrangements efficiently

**Implementation Details**:
1. Use Python's `itertools.permutations()`
2. **Optimization**: Fix the first person's position to eliminate rotational duplicates
   - For circular arrangements, rotating [A,B,C,D] → [B,C,D,A] produces the same seating
   - Fix the first person (e.g., alphabetically first) at position 0
   - Generate permutations of remaining n-1 people
   - This reduces arrangements from n! to (n-1)!
3. Implementation:
   ```python
   from itertools import permutations

   people_sorted = sorted(people)  # For consistency
   fixed_person = people_sorted[0]
   remaining_people = people_sorted[1:]

   for perm in permutations(remaining_people):
       arrangement = [fixed_person] + list(perm)
       # Process this arrangement
   ```

**Reflection vs Rotation**:
- We only optimize for rotation (fixing position), not reflection
- Reflection ([A,B,C,D] vs [A,D,C,B]) produces different happiness values in directed graphs
- So we keep reflection duplicates

**Arrangements to Evaluate**: (8-1)! = 5,040

### Step 4: Find Maximum Happiness
**Objective**: Evaluate all arrangements and track the maximum

**Implementation Details**:
1. Initialize `max_happiness = float('-inf')` (or very large negative number)
2. Optionally track `best_arrangement = None` (for debugging, not required for output)
3. Iterate through all permutations from Step 3:
   ```python
   max_happiness = float('-inf')

   for perm in permutations(remaining_people):
       arrangement = [fixed_person] + list(perm)
       current_happiness = calculate_happiness(arrangement, happiness_map)

       if current_happiness > max_happiness:
           max_happiness = current_happiness
           # best_arrangement = arrangement[:]  # Optional

   return max_happiness
   ```

**Time Complexity**: O(n! × n) overall

### Step 5: Output Result
**Objective**: Print the maximum happiness value

**Implementation Details**:
1. Simply print the integer result: `print(max_happiness)`
2. No additional formatting needed

## Complete Program Structure

```python
import re
from itertools import permutations

def parse_input(input_text):
    """Parse input and return happiness map and list of people"""
    happiness = {}
    people = set()

    pattern = r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.'

    for line in input_text.strip().split('\n'):
        match = re.match(pattern, line)
        if match:
            person1, action, value, person2 = match.groups()
            people.add(person1)
            people.add(person2)

            if person1 not in happiness:
                happiness[person1] = {}

            happiness_value = int(value) if action == 'gain' else -int(value)
            happiness[person1][person2] = happiness_value

    return happiness, list(people)

def calculate_happiness(arrangement, happiness_map):
    """Calculate total happiness for a circular arrangement"""
    total = 0
    n = len(arrangement)

    for i in range(n):
        person = arrangement[i]
        left_neighbor = arrangement[(i - 1) % n]
        right_neighbor = arrangement[(i + 1) % n]

        total += happiness_map[person][left_neighbor]
        total += happiness_map[person][right_neighbor]

    return total

def find_optimal_seating(happiness_map, people):
    """Find the seating arrangement with maximum happiness"""
    people_sorted = sorted(people)
    fixed_person = people_sorted[0]
    remaining_people = people_sorted[1:]

    max_happiness = float('-inf')

    for perm in permutations(remaining_people):
        arrangement = [fixed_person] + list(perm)
        current_happiness = calculate_happiness(arrangement, happiness_map)

        if current_happiness > max_happiness:
            max_happiness = current_happiness

    return max_happiness

def main():
    # Read input - verify the correct filename
    # Could be 'input.md', 'input.txt', or other
    with open('input.txt', 'r') as f:
        input_text = f.read()

    # Parse input
    happiness_map, people = parse_input(input_text)

    # Find optimal seating
    max_happiness = find_optimal_seating(happiness_map, people)

    # Output result
    print(max_happiness)

if __name__ == '__main__':
    main()
```

## Runtime Analysis

**With 8 people**:
- Permutations to evaluate: 7! = 5,040
- Happiness calculations per permutation: 8 people × 2 neighbors = 16 operations
- Total operations: ~80,640 arithmetic operations
- **Expected runtime**: < 50ms on modern hardware

**Scalability Limit**:
- n=10: 362,880 permutations (~4 seconds)
- n=11: 3,628,800 permutations (~40 seconds)
- n=12: 39,916,800 permutations (~7 minutes)
- Beyond n=12, would need dynamic programming or heuristic approaches

## Error Handling Considerations

Since this is a scripting problem, minimal error handling needed:
- Assume input is well-formed per specification
- Assume all bidirectional relationship pairs are provided (person A→B and person B→A)
- Note: Relationships are directional, not symmetric (happiness[A][B] may differ from happiness[B][A])
- No validation for missing relationships needed for given input
