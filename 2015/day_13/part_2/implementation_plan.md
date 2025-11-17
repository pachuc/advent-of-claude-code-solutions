# Implementation Plan: Optimal Seating Arrangement with Self Included

## Problem Analysis

This is a circular permutation optimization problem where we need to:
1. Parse happiness relationships between guests
2. Add ourselves to the guest list (with 0 happiness relationships)
3. Find the seating arrangement that maximizes total happiness
4. Account for circular seating (each person has exactly 2 neighbors)

**Input Size**: 8 guests + self = 9 people total
**Computational Complexity**: For n people, there are (n-1)! unique circular arrangements (fixing one position to account for rotational symmetry)
- For 9 people: 8! = 40,320 arrangements (very manageable with brute force)
- Note: We do NOT divide by 2 to eliminate reflections because happiness relationships are **directed/asymmetric** (A's happiness with B ≠ B's happiness with A), making clockwise and counter-clockwise arrangements genuinely different

## Algorithm Choice

Given the input size (9 people), a **brute force permutation approach** is optimal:
- Generate all permutations of seating arrangements
- Calculate happiness for each arrangement
- Return the maximum

**Why not dynamic programming or other optimizations?**
- The state space is too complex for efficient DP (no obvious overlapping subproblems)
- The problem size is small enough that brute force is fast (< 1 second)
- Brute force guarantees correctness and is simpler to implement

## Implementation Steps

### Step 1: Parse Input Data
**Goal**: Extract happiness relationships from input text

**Implementation**:
```python
def parse_input(input_text):
    """
    Parse happiness relationships from input text
    Returns:
    - happiness_map: dict[person][neighbor] = happiness_value
    - people: set of all person names
    """
```

**Details**:
- Use regex pattern: `r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.'`
- Extract: person, gain/lose, magnitude, neighbor
- Convert "lose" to negative values
- Store in nested dictionary: `happiness[person1][person2] = value`
- Collect all unique person names in a set
- Expected: 8 people × 7 relationships each = 56 total directed relationships

**Edge cases**:
- Handle both "gain" and "lose" correctly
- Ensure all person names are captured

### Step 2: Add Self to Guest List
**Goal**: Include ourselves with neutral (0) happiness relationships

**Implementation**:
```python
def add_self(happiness_map, people, self_name="Me"):
    """
    Add ourselves to the seating arrangement with 0 happiness
    Modifies happiness_map and people in place
    """
```

**Details**:
- Choose a distinct name for ourselves (e.g., "Me")
- Add bidirectional 0 happiness relationships:
  - For each existing person: `happiness["Me"][person] = 0` and `happiness[person]["Me"] = 0`
- Add "Me" to the people set

### Step 3: Calculate Happiness for a Given Arrangement
**Goal**: Compute total happiness for a specific seating order

**Implementation**:
```python
def calculate_happiness(arrangement, happiness_map):
    """
    Calculate total happiness for a circular seating arrangement
    Args:
        arrangement: list of people in seating order
        happiness_map: nested dict of happiness values
    Returns: total happiness (int)
    """
```

**Details**:
- Iterate through the arrangement
- For each person at index i:
  - Left neighbor: `arrangement[(i-1) % n]`
  - Right neighbor: `arrangement[(i+1) % n]`
  - Add: `happiness[person][left_neighbor] + happiness[person][right_neighbor]`
- Return sum of all happiness values

**Key insight**: Each adjacency contributes twice (once from each person's perspective)

### Step 4: Generate All Seating Arrangements
**Goal**: Generate all unique circular permutations

**Implementation**:
```python
from itertools import permutations

def find_optimal_seating(people, happiness_map):
    """
    Find the seating arrangement with maximum happiness
    Returns: maximum happiness value
    """
```

**Details**:
- Convert people set to list
- Fix the first person to eliminate rotational duplicates
  - Take one person (e.g., first in list) and fix them at position 0
  - Generate permutations of the remaining (n-1) people: `permutations(people_list[1:])`
  - Prepend the fixed person to each permutation: `[fixed] + list(perm)`
  - This reduces permutations from n! to (n-1)! = 40,320 arrangements
- For each arrangement:
  - Calculate happiness using `calculate_happiness()`
  - Track both maximum happiness value and the optimal arrangement
- Return maximum happiness and optimal arrangement (for verification)

**Optimization**: By fixing the first person, we avoid counting rotations as different arrangements
**Note**: We generate (n-1)! = 40,320 permutations, not (n-1)!/2, because happiness relationships are asymmetric

### Step 5: Main Execution Flow
**Goal**: Orchestrate the solution

**Implementation**:
```python
def solve(input_file):
    """
    Main solver function
    """
    # 1. Read input file
    with open(input_file, 'r') as f:
        input_text = f.read()

    # 2. Parse input
    happiness_map, people = parse_input(input_text)

    # 3. Add self
    add_self(happiness_map, people)

    # 4. Find optimal seating
    max_happiness, optimal_arrangement = find_optimal_seating(people, happiness_map)

    # 5. Output results
    print(f"Maximum happiness: {max_happiness}")
    print(f"Optimal arrangement: {' -> '.join(optimal_arrangement)}")

    return max_happiness
```

**Output format**:
- Print the maximum happiness value (primary answer)
- Print the optimal arrangement for manual verification
- Return the happiness value for testing

## Data Structures

**Happiness Map**:
```python
happiness_map = {
    "Alice": {"Bob": -2, "Carol": -62, ...},
    "Bob": {"Alice": 93, "Carol": 19, ...},
    ...
}
```
- Nested dictionary for O(1) lookup
- Space complexity: O(n²) where n is number of people

**People Set**:
```python
people = {"Alice", "Bob", "Carol", ...}
```
- Set for O(1) membership testing and uniqueness

## Time Complexity Analysis

- **Parsing**: O(m) where m is number of input lines (m = n²-n for complete graph)
- **Adding self**: O(n) to add relationships
- **Permutation generation**: O((n-1)!) arrangements to generate
- **Happiness calculation per arrangement**: O(n)
- **Overall**: O(n * (n-1)!) ≈ O(n!)

For n=9: 9 * 8! = 9 * 40,320 = 362,880 operations (very fast, completes in well under 1 second)

## Space Complexity Analysis

- **Happiness map**: O(n²)
- **Permutation storage**: O(n) per permutation (not stored, generated on-the-fly)
- **Overall**: O(n²)

## Code Structure

```
solution.py
├── parse_input(input_text) -> (happiness_map, people)
├── add_self(happiness_map, people, self_name)
├── calculate_happiness(arrangement, happiness_map) -> int
├── find_optimal_seating(people, happiness_map) -> (int, list)
└── solve(input_file) -> int
```

## Error Handling

Since this is a script for a specific input:
- Minimal error handling required
- Assume input is well-formed and complete (all relationships present)
- If a relationship is missing during lookup, the code will raise a KeyError (acceptable for this use case)
- No need for extensive validation of data integrity

## Summary

This implementation uses a straightforward brute-force approach:
1. Parse all happiness relationships
2. Add ourselves with neutral relationships
3. Generate all circular permutations (fixing one person)
4. Calculate happiness for each arrangement
5. Return the maximum

The approach is optimal for this problem size and guarantees correctness.
