# Problem Report: A Regular Map - Part 2

## Context from Part 1

In Part 1, we navigated a facility made up of rooms arranged in a grid, where rooms only connect to adjacent rooms when a door is present between them. We were given a regular expression (regex) that describes routes through every door in the facility.

The regex uses:
- `^` and `$` to mark the beginning and end of routes
- `N`, `S`, `E`, `W` for directional movements (north, south, east, west)
- Parentheses `()` for branching paths
- Pipes `|` to separate branch options
- Empty options (e.g., `(NEWS|)`) to allow skipping branches

By parsing the regex and tracing all possible routes, we built a graph of all rooms and doors in the facility. We then used BFS (Breadth-First Search) to find the shortest path from the starting position (0, 0) to every room, measuring distance by the number of doors passed through.

**Part 1 Answer:** The furthest room from the starting position required passing through **3672 doors**.

## Part 2 Objective

Now that we know the facility is very large, we need to count **how many rooms have a shortest path from the starting location that passes through at least 1000 doors**.

## Input Format

The input is the same regular expression from Part 1 (found in input.md):
- A single-line regex string starting with `^` and ending with `$`
- Contains directional characters `N`, `S`, `E`, `W`
- Contains branching logic with `()` and `|`
- May contain empty branch options

## Output Requirements

Return a single integer: **the count of rooms that require passing through at least 1000 doors to reach from the starting position** (using the shortest path to each room).

## Algorithm Requirements

1. **Reuse Part 1's graph construction**: Parse the regex and build the graph of rooms and doors (this part remains unchanged)

2. **Modify the BFS search**: Instead of just finding the maximum distance, we need to:
   - Perform BFS from the starting position (0, 0)
   - For each room discovered, record the minimum number of doors needed to reach it
   - Count how many rooms have a distance >= 1000

3. **Return the count** of rooms meeting the threshold criteria

## Key Differences from Part 1

- Part 1: Find the **maximum** distance (furthest room)
- Part 2: Count **how many** rooms are at distance >= 1000

The graph construction logic remains identical; only the final calculation changes.
