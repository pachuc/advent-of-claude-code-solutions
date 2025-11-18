# Problem Report: Digital Plumber - Part 2

## Context from Part 1
Programs in a village communicate through a system of bidirectional pipes. In Part 1, we determined that **239 programs** are in the connected group containing program ID `0`. This means these 239 programs can all communicate with program `0` either directly or indirectly through other programs.

## Part 2 Objective
Now we need to determine the **total number of distinct groups** in the entire network. Not all programs can reach program `0`'s group - some programs are isolated in separate groups with no way to communicate with program `0`'s group.

A **group** is a collection of programs that can all communicate with each other (directly or indirectly) via pipes, but cannot communicate with programs outside their group.

## Input Format
The input format is the same as Part 1:
```
<program_id> <-> <connected_id_1>, <connected_id_2>, ...
```

- `program_id`: The ID of the program (an integer)
- `<->`: Indicates bidirectional connection
- Following the arrow: A comma-separated list of one or more program IDs that this program can communicate with directly

### Input Properties
- Connections are bidirectional
- Each program has one or more direct connections
- Programs may connect to themselves

## Expected Output
A single integer representing the **total number of distinct groups** in the network.

### Output Format
The answer should be a single number.

## Example

### Example Input
```
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
```

### Example Explanation
There are **2 groups**:
1. **Group 1**: Programs `0, 2, 3, 4, 5, 6` (all connected to each other through various paths)
2. **Group 2**: Program `1` (only connected to itself, isolated from the other group)

### Example Output
```
2
```

## Algorithm Approach
This is a graph connected components problem. The solution requires:
1. Parse the input to build a graph representation (adjacency list) - same as Part 1
2. Iterate through all programs in the network
3. For each unvisited program, perform a graph traversal (BFS or DFS) to find all programs in its group
4. Mark all programs in the discovered group as visited
5. Increment the group counter
6. Continue until all programs have been assigned to a group
7. Return the total number of groups found

The key difference from Part 1 is that we need to find ALL connected components, not just the one containing program `0`.
