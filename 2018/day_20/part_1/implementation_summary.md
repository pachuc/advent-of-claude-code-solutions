# Implementation Summary: A Regular Map

## Overview
Successfully implemented a solution to parse a regular expression describing routes through a facility, build a graph of rooms and doors, and find the maximum shortest path distance from the starting position.

## Solution Approach

### Algorithm
The solution uses three main components:

1. **Regex Parser with Graph Building** (`parse_regex_and_build_graph`)
   - Uses a stack-based approach to handle nested branches
   - Tracks current positions as we parse the regex character by character
   - Maintains a set of doors connecting adjacent rooms
   - Stack stores tuples of (starting_positions, branch_endpoints) for each branch level

2. **Adjacency Graph Builder** (`build_adjacency_graph`)
   - Converts the set of doors into a bidirectional adjacency graph
   - Uses defaultdict(set) for efficient neighbor lookup

3. **BFS Maximum Distance Finder** (`find_max_distance`)
   - Performs breadth-first search from the starting position (0, 0)
   - Tracks the shortest distance to each room
   - Returns the maximum distance found

### Key Data Structures

- **Doors**: Set of frozensets, where each frozenset contains two adjacent room coordinates
  - Example: `{frozenset([(0,0), (0,-1)]), frozenset([(0,-1), (1,-1)]), ...}`
- **Positions**: Set of (x, y) tuples representing current location(s) during parsing
- **Stack**: List of tuples `(starting_positions, branch_endpoints)` for handling nested branches
- **Adjacency Graph**: defaultdict(set) mapping each room to its neighbors

### Branch Handling Logic

The implementation handles branches using the following logic:

- **`(`**: Push current positions to stack along with empty branch endpoints list
- **`|`**: Save current positions as endpoints of this branch alternative, restore starting positions from stack
- **`)`**: Merge all branch alternative endpoints into a single set of positions

This approach correctly handles:
- Empty branch alternatives (e.g., `(NEWS|)`)
- Nested branches (e.g., `(N(E|W)|S)`)
- Multiple alternatives (e.g., `(N|S|E|W)`)

## Files Created

1. **solution.py** - Main solution file containing:
   - `parse_regex_and_build_graph(regex)` - Parses regex and builds door set
   - `build_adjacency_graph(doors)` - Converts doors to adjacency graph
   - `find_max_distance(graph, start)` - BFS to find maximum shortest path
   - `solve(input_text)` - Main solver function
   - Main execution block that reads input and prints result

2. **test_solution.py** - Test file containing:
   - `test_provided_examples()` - Tests all 5 examples from problem statement
   - `test_simple_cases()` - Tests basic edge cases
   - Main execution block that runs all tests and reports results

3. **implementation_summary.md** - This file

## Testing Process

### Simple Test Cases
Tested basic functionality with simple inputs:
- ✓ Single direction: `^N$` → 1
- ✓ Multiple same direction: `^NNN$` → 3
- ✓ Empty regex: `^$` → 0
- ✓ Simple two-way branch: `^N(E|W)N$` → 3

All simple tests **PASSED**.

### Provided Examples
Tested with all 5 examples from the problem statement:
- ✓ Example 1: `^WNE$` → 3
- ✓ Example 2: `^ENWWW(NEEE|SSE(EE|N))$` → 10
- ✓ Example 3: `^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$` → 18
- ✓ Example 4: `^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$` → 23
- ✓ Example 5: `^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$` → 31

All provided examples **PASSED**.

### Actual Puzzle Input
- Input: Large regex from input.md (~10K characters)
- Output: **3672**
- Performance: Completed in under 1 second
- Memory: No issues observed

## Result

**Answer: 3672**

The solution successfully:
- Parses the complex regex with nested branches
- Builds a complete graph of all rooms and doors
- Finds the shortest path to each room using BFS
- Returns the maximum distance (3672 doors)

## Code Quality

The implementation is:
- **Clean**: Well-structured with clear function separation
- **Efficient**: Uses appropriate data structures (sets, deques, defaultdict)
- **Correct**: Passes all test cases including edge cases
- **Readable**: Well-commented and follows Python conventions
- **Simple**: Focuses on solving the problem without unnecessary complexity

## Time Complexity

- Parsing: O(R × P) where R is regex length and P is number of positions (bounded by rooms)
- Graph building: O(D) where D is number of doors
- BFS: O(V + E) where V is number of rooms and E is number of doors
- Overall: O(R × P + V + E)

For the actual input, this completes in well under 1 second, meeting performance requirements.
