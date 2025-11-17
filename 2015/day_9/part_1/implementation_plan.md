# Implementation Plan: Traveling Salesman Problem - Shortest Route

## Overview
Implement a solution to find the shortest Hamiltonian path through 8 locations given pairwise distances.

## Algorithm Choice
**Brute Force with Permutations** - O(n! × n) complexity
- With n=8 locations: 8! = 40,320 permutations
- Each permutation requires O(n) time to calculate total distance
- Total operations: ~322,560 - completely feasible for modern computers

## Step-by-Step Implementation

### Step 1: Input Parsing
**Objective:** Parse the input file to extract locations and distances

**Implementation Details:**
- Read input file (use 'input.md' or accept as command-line argument)
- Read file line by line, stripping whitespace
- Parse each line using string splitting (simpler than regex for this format):
  - Split on `' to '` to separate location1 from rest
  - Split the rest on `' = '` to separate location2 from distance
  - Example: `parts = line.split(' to ')` then `loc2, dist = parts[1].split(' = ')`
- Extract three components per line:
  - `location1` (string)
  - `location2` (string)
  - `distance` (integer - convert using `int()`)
- Store parsed data for graph construction

**Data Structure Considerations:**
- Use a set to collect unique location names
- Store raw distance tuples for later processing

### Step 2: Build Distance Graph
**Objective:** Create a data structure for efficient distance lookups

**Implementation Details:**
- Use a dictionary of dictionaries: `distances[loc1][loc2] = dist`
- Since distances are bidirectional, store both:
  - `distances[loc1][loc2] = dist`
  - `distances[loc2][loc1] = dist`
- **Important:** Initialize nested dictionaries before assignment
- Alternative: Use a single dictionary with tuple keys: `distances[(loc1, loc2)] = dist`

**Recommended Approach:**
```python
from collections import defaultdict
distances = defaultdict(dict)  # Automatically creates nested dicts
# For each location pair and distance:
distances[loc1][loc2] = dist
distances[loc2][loc1] = dist  # Bidirectional
```

**Or without defaultdict:**
```python
distances = {}
# For each location pair and distance:
if loc1 not in distances:
    distances[loc1] = {}
if loc2 not in distances:
    distances[loc2] = {}
distances[loc1][loc2] = dist
distances[loc2][loc1] = dist
```

### Step 3: Extract Unique Locations
**Objective:** Get a list of all unique locations to permute

**Implementation Details:**
- Iterate through all parsed location pairs
- Add each location to a set (automatically handles duplicates)
- Convert set to list for permutation generation
- Expected result: List of 8 location names

### Step 4: Generate All Permutations
**Objective:** Generate all possible routes through all locations

**Implementation Details:**
- Use `itertools.permutations(locations)` from Python standard library
- This generates all n! orderings of the locations
- Each permutation represents a complete path visiting each location exactly once

**Optimization Note:**
- We could skip reverse permutations (e.g., A→B→C vs C→B→A) since they yield the same total distance
- This would reduce permutations from 40,320 to 20,160
- However, with only 40,320 permutations total, optimization adds complexity without meaningful performance gain
- Keep implementation simple and check all permutations

### Step 5: Calculate Distance for Each Route
**Objective:** For each permutation, calculate the total travel distance

**Implementation Details:**
- For each permutation (route):
  - Initialize `total_distance = 0`
  - Iterate through consecutive pairs: `(route[0], route[1])`, `(route[1], route[2])`, etc.
  - For each pair `(current, next)`:
    - Look up `distances[current][next]`
    - Add to `total_distance`
  - Store or compare this total

**Implementation Pattern:**
```python
for i in range(len(route) - 1):
    current = route[i]
    next_loc = route[i + 1]
    total_distance += distances[current][next_loc]
```

### Step 6: Track and Return Minimum Distance
**Objective:** Find the minimum distance among all routes

**Implementation Details:**
- Initialize `min_distance = float('inf')` or use first route's distance
- For each calculated route distance:
  - If `distance < min_distance`:
    - Update `min_distance = distance`
- After all permutations checked, return `min_distance`

**Alternative Approach:**
- Store all distances in a list and use `min(distances)`
- More memory but simpler code

### Step 7: Main Function Structure
**Objective:** Organize code into a clean, executable structure

**Implementation Details:**
```python
def parse_input(filename):
    # Read and parse input file
    # Return locations set and distances dict
    pass

def calculate_route_distance(route, distances):
    # Calculate total distance for a given route
    pass

def find_shortest_route(locations, distances):
    # Generate permutations and find minimum
    pass

def main():
    # 1. Parse input from 'input.md' (or use sys.argv[1] for command-line argument)
    locations, distances = parse_input('input.md')

    # 2. Find shortest route
    min_distance = find_shortest_route(locations, distances)

    # 3. Print result to stdout
    print(min_distance)

if __name__ == "__main__":
    main()
```

## Data Structures Summary

1. **Locations:** `set` or `list` of strings
   - Example: `{'Faerun', 'Norrath', 'Tristram', ...}`

2. **Distances:** `dict[str, dict[str, int]]` or `dict[tuple[str, str], int]`
   - Example: `distances['Faerun']['Norrath'] = 129`

3. **Route (permutation):** `tuple` of strings
   - Example: `('Faerun', 'Norrath', 'Tristram', ...)`

## Complexity Analysis

- **Time Complexity:** O(n! × n)
  - n! permutations
  - n-1 distance lookups per permutation
  - For n=8: ~322,560 operations

- **Space Complexity:** O(n²)
  - Distance matrix: 8×8 = 64 entries
  - Permutations generated lazily by itertools (O(n) at a time)

## Error Handling (Minimal)

Since this is a script for a specific input:
- Assume input file exists and is well-formed
- Assume all location pairs in permutations exist in distances dict
- No need for extensive validation

## Expected Output Format

Print a single integer representing the minimum distance:
```
117
```
(This is an example; actual answer depends on calculation)

## Libraries Required

- `itertools` - for permutations (standard library)
- `collections` - for defaultdict (standard library, optional but recommended)
- No external dependencies needed
- No regex library needed - use built-in string methods
