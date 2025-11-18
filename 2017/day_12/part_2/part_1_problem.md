# Problem Report: Digital Plumber

## Context
Programs in a village communicate through a system of bidirectional pipes. Some programs cannot reach each other due to missing or disconnected pipes. We need to investigate connectivity within this network.

## Objective
Determine how many programs are in the group that contains program ID `0`. A "group" consists of all programs that can communicate with program `0` either directly or indirectly through other programs.

## Input Format
The input consists of lines describing the pipe connections for each program. Each line has the format:
```
<program_id> <-> <connected_id_1>, <connected_id_2>, ...
```

- `program_id`: The ID of the program (an integer)
- `<->`: Indicates bidirectional connection
- Following the arrow: A comma-separated list of one or more program IDs that this program can communicate with directly

### Input Properties
- Connections are bidirectional: if program `8` can communicate with `11`, then `11` can communicate with `8`
- Each program has one or more direct connections
- Programs may connect to themselves (e.g., `4 <-> 4, 1473`)

## Expected Output
A single integer representing the total count of programs that are in the group containing program ID `0`.

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
Programs in the group containing program `0`:
- Program `0` (by definition)
- Program `2` (directly connected to `0`)
- Program `3` (via program `2`)
- Program `4` (via program `2`)
- Program `6` (via programs `4` then `2`)
- Program `5` (via programs `6`, then `4`, then `2`)

Total: **6 programs** (all programs except program `1`, which only connects to itself)

### Example Output
```
6
```

## Algorithm Approach
This is a graph connectivity problem. The solution requires:
1. Parse the input to build a graph representation (adjacency list)
2. Perform a graph traversal (BFS or DFS) starting from program `0`
3. Track all visited programs during the traversal
4. Return the count of visited programs

The traversal will explore all programs reachable from program `0` through any path of connections.
