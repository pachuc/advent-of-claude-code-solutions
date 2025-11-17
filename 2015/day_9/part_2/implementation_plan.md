# Implementation Plan: Longest Route TSP Variant

## Problem Analysis
- **Problem Type**: Traveling Salesman Problem (TSP) - Maximization variant
- **Goal**: Find the longest Hamiltonian path through all locations
- **Input Size**: 8 locations, 28 bidirectional edges
- **Complexity**: O(n!) for brute force, but feasible for n=8
- **Approach**: Complete enumeration of all permutations

## Algorithm Selection

### Chosen Approach: Brute Force Permutation
- **Rationale**: With only 8 locations, we have 8! = 40,320 permutations
- **Time Complexity**: O(n! × n) where n=8
- **Space Complexity**: O(n²) for adjacency storage
- **Feasibility**: Runs in milliseconds for this input size

### Alternative Approaches Considered (but not needed):
- Dynamic Programming (Held-Karp): O(n² × 2^n) - unnecessary complexity for n=8
- Branch and Bound: Requires additional pruning logic - overkill
- Heuristics (Greedy, etc.): Don't guarantee optimal solution

## Implementation Steps

### Step 1: Input Parsing
**Objective**: Extract locations and distances from input file

**Implementation Details**:
1. Read input file line by line
2. Parse each line with format: `Location1 to Location2 = Distance`
3. Use regex or string split to extract:
   - `Location1` (string)
   - `Location2` (string)
   - `Distance` (integer)

**Data Structures**:
```python
# Set to collect unique locations
locations = set()

# Dictionary to store distances (bidirectional)
# Key: tuple of (loc1, loc2) or (loc2, loc1)
# Value: distance (int)
distances = {}
```

**Parsing Implementation**:
```python
with open('input.md', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        # Parse format: "Location1 to Location2 = Distance"
        # Split by ' to ' to get left (loc1) and right (rest)
        parts = line.split(' to ')
        loc1 = parts[0].strip()

        # Split right part by ' = ' to get loc2 and distance
        right_parts = parts[1].split(' = ')
        loc2 = right_parts[0].strip()
        distance = int(right_parts[1].strip())

        # Add locations to set
        locations.add(loc1)
        locations.add(loc2)

        # Store bidirectional distances
        distances[(loc1, loc2)] = distance
        distances[(loc2, loc1)] = distance
```

**Edge Cases to Handle**:
- Strip whitespace from location names
- Handle bidirectional nature: store both (A,B) and (B,A) as keys
- Ensure distances are parsed as integers
- Skip empty lines in input

### Step 2: Build Distance Graph
**Objective**: Create efficient data structure for distance lookup

**Implementation Details**:
1. Convert the `locations` set to a list for indexing
2. Build a distance dictionary that maps pairs of locations to distances
3. Ensure bidirectional access: `distances[(A, B)] == distances[(B, A)]`

**Data Structure**:
```python
# Dictionary with tuple keys (ONLY approach to use)
distances = {
    (loc1, loc2): dist,
    (loc2, loc1): dist  # bidirectional
}
```

**Why tuple keys**: This approach provides O(1) lookup time and handles bidirectional edges naturally by storing both (A,B) and (B,A) during parsing.

### Step 3: Generate All Permutations
**Objective**: Generate all possible routes through all locations

**Implementation Details**:
1. Use `itertools.permutations()` to generate all orderings
2. Each permutation represents a complete route visiting all locations once

**Code Approach**:
```python
from itertools import permutations

all_routes = permutations(locations)
# This generates 8! = 40,320 permutations
```

**Note on Permutation Count**:
- We generate all 8! = 40,320 permutations of the 8 locations
- This includes "reverse duplicates": route [A,B,C] and [C,B,A] both get checked
- Since edges are bidirectional, reverse routes have the same distance
- However, checking all permutations is still efficient (runs in <100ms) and simpler than filtering
- The algorithm correctly finds the maximum among all these permutations

### Step 4: Calculate Distance for Each Route
**Objective**: Compute total distance for each permutation

**Implementation Details**:
1. For each permutation (route):
   - Initialize `total_distance = 0`
   - Iterate through consecutive pairs in the route
   - Look up distance between each pair in the distances dictionary
   - Add to total_distance

**Code Structure**:
```python
def calculate_route_distance(route, distances):
    total = 0
    for i in range(len(route) - 1):
        loc1, loc2 = route[i], route[i+1]
        total += distances[(loc1, loc2)]
    return total
```

**Edge Cases**:
- Ensure all edges exist in the distances dictionary
- Handle the case where route has only 1 location (distance = 0)

### Step 5: Find Maximum Distance
**Objective**: Track and return the longest route distance

**Implementation Details**:
1. Initialize `max_distance = 0`
2. For each route:
   - Calculate its distance
   - Update `max_distance` if current route is longer
3. Return `max_distance`

**Optimization Options**:
```python
# Option 1: Iterative tracking
max_distance = 0
for route in all_routes:
    distance = calculate_route_distance(route, distances)
    max_distance = max(max_distance, distance)

# Option 2: Using Python's max() with generator
max_distance = max(
    calculate_route_distance(route, distances)
    for route in all_routes
)
```

**Recommendation**: Use Option 2 for cleaner, more Pythonic code

### Step 6: Output Result
**Objective**: Print the final answer

**Implementation Details**:
1. Print the maximum distance as a single integer
2. Format: `print(max_distance)`

**Optional Enhancement** (for debugging):
```python
# If you want to track the best route as well:
max_distance = 0
best_route = None

for route in permutations(locations):
    distance = calculate_route_distance(route, distances)
    if distance > max_distance:
        max_distance = distance
        best_route = route

print(f"Maximum distance: {max_distance}")
print(f"Best route: {' -> '.join(best_route)}")
```

## Complete Code Structure

```python
import re
from itertools import permutations

def parse_input(filename):
    """Parse input file and return locations set and distances dict"""
    locations = set()
    distances = {}

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse format: "Location1 to Location2 = Distance"
            parts = line.split(' to ')
            loc1 = parts[0].strip()

            right_parts = parts[1].split(' = ')
            loc2 = right_parts[0].strip()
            distance = int(right_parts[1].strip())

            locations.add(loc1)
            locations.add(loc2)

            # Store bidirectional
            distances[(loc1, loc2)] = distance
            distances[(loc2, loc1)] = distance

    return locations, distances

def calculate_route_distance(route, distances):
    """Calculate total distance for a given route"""
    total = 0
    for i in range(len(route) - 1):
        total += distances[(route[i], route[i+1])]
    return total

def find_longest_route(locations, distances):
    """Find the longest route through all locations"""
    max_distance = max(
        calculate_route_distance(route, distances)
        for route in permutations(locations)
    )
    return max_distance

def main():
    locations, distances = parse_input('input.md')
    result = find_longest_route(locations, distances)
    print(result)

if __name__ == '__main__':
    main()
```

## Performance Considerations

### Expected Runtime
- **Permutation Generation**: 8! = 40,320 permutations
- **Distance Calculation**: 7 lookups per route (8-1 edges)
- **Total Operations**: ~282,240 dictionary lookups
- **Expected Time**: < 100ms on modern hardware

### Memory Usage
- **Locations**: 8 strings, negligible
- **Distances**: 28 entries × 2 (bidirectional) = 56 entries, negligible
- **Permutations**: Generated lazily by itertools, minimal memory
- **Total Memory**: < 1 MB

### Scalability Limit
- This brute force approach works well up to ~10-11 locations
- Beyond that, need to consider:
  - Dynamic programming (Held-Karp algorithm)
  - Approximation algorithms
  - Heuristic methods

## Error Handling

### Minimal Error Handling Needed
Since this is a script for a known input format:

1. **File not found**: Assume 'input.md' exists in the current directory
2. **Parse errors**: Assume input is well-formed (format: "Location1 to Location2 = Distance")
3. **Missing edges**: Assume complete graph (all pairs exist)
4. **Invalid distances**: Assume all distances are positive integers

**Important Note**: The input file must be named 'input.md' or the filename should be passed as a command-line argument.

### Optional Validation (if desired)
```python
# Check if graph is complete
expected_edges = len(locations) * (len(locations) - 1) // 2
actual_edges = len(distances) // 2
if actual_edges != expected_edges:
    print(f"Warning: Graph may be incomplete. Expected {expected_edges} edges, found {actual_edges}")

# Check for missing edge during calculation (catches incomplete graphs)
try:
    total += distances[(route[i], route[i+1])]
except KeyError:
    print(f"Error: No distance found between {route[i]} and {route[i+1]}")
    raise
```

## Implementation Priority

1. **Must Have**:
   - Input parsing
   - Distance calculation
   - Permutation generation
   - Max finding

2. **Nice to Have** (for debugging):
   - Print the actual longest route
   - Validation of complete graph
   - Count of total routes checked

3. **Not Needed**:
   - Extensive error handling
   - Logging
   - Progress indicators
   - Optimization beyond basic approach
