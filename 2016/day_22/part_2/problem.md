# Problem Report: Grid Computing - Minimum Steps to Access Goal Data

## Part 1 Context
In Part 1, we analyzed a grid storage cluster to count "viable pairs" - pairs of nodes where node A's used data could theoretically fit in node B's available space, regardless of whether they were directly connected. This helped us understand which nodes could potentially exchange data. The answer to Part 1 was 981 viable pairs.

The grid consists of storage nodes arranged in a 2D grid, where each node is identified by coordinates `/dev/grid/node-x{X}-y{Y}`. Each node has a Size (total capacity), Used (current usage), and Avail (available space).

## Part 2 Objective
Find the **minimum number of steps** required to move the goal data from the top-right corner node (the node with y=0 and the highest x value) to the directly accessible node at position (0, 0).

## Context
We have a grid storage cluster where:
- Each storage node is only connected to its four adjacent neighbors (up, down, left, right)
- We can only directly access data on node `/dev/grid/node-x0-y0` (the top-left corner)
- The **goal data** starts in the node with `y=0` and the **highest x value** (the top-right corner)
- We need to move this goal data to `node-x0-y0` so we can access it
- Data can only be moved between adjacent nodes (not copied - the source becomes empty)
- A move is only possible if the destination node has enough available space to receive all the data

## Input Format
Same as Part 1: The input is the output of a `df -h` command showing disk usage for all nodes in the grid.

```
root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0     89T   65T    24T   73%
/dev/grid/node-x0-y1     92T   64T    28T   69%
...
```

Each line (after the header) contains:
- **Filesystem**: Node identifier in format `/dev/grid/node-x{X}-y{Y}` where X and Y are coordinates
- **Size**: Total storage capacity (in Terabytes with 'T' suffix)
- **Used**: Amount of storage currently used (in Terabytes with 'T' suffix)
- **Avail**: Available storage space (in Terabytes with 'T' suffix)
- **Use%**: Percentage of storage used

## Grid Properties
Based on the example, the grid typically contains:
- **Normal nodes (`.`)**: Nodes with some data that can be moved around, but not enough space to receive other nodes' data
- **Empty node (`_`)**: A node with 0T used - this is critical for enabling data movement
- **Wall nodes (`#`)**: Very large, very full nodes that cannot be moved and block paths
- **Goal node (`G`)**: The node at position (max_x, 0) containing the data we want to access
- **Access node `()`**: The node at position (0, 0) where we can directly access data

## Task Definition
Calculate the minimum number of **move operations** needed to get the goal data from position `(max_x, 0)` to position `(0, 0)`.

**Move operation**: Transfer all data from one node to an adjacent node (the source becomes empty after the move). A move is only valid if:
1. The source and destination are adjacent (horizontally or vertically, not diagonally)
2. The destination has enough available space to receive all the source's data

## Strategy Insights from Example
The puzzle provides a detailed example with a 3x3 grid that requires **7 steps** to move the goal data from position `(2, 0)` to `(0, 0)`. The example demonstrates:

1. **Empty node is key**: You need an empty node (Used = 0T) to act as a "gap" for shuffling data around
2. **Sliding puzzle mechanics**: This is similar to a sliding tile puzzle where you move the empty space around
3. **Multi-step process**:
   - First, position the empty node to be adjacent to the goal data
   - Then swap the goal with the empty space to move it one position left
   - To move the goal left again, you must cycle the empty node around it (move it down, right, right, up) to get it to the left of the goal again
   - Repeat this pattern to slide the goal all the way to (0, 0)
4. **Wall nodes**: Very large, very full nodes (`#` in the example) act as immovable obstacles that block certain paths
5. **No deletion**: You cannot delete data - you must move it somewhere else, which constrains your options

The example's 7 steps consisted of:
- 1 move to create an empty space in the top row
- 1 move to swap goal into that space
- 5 more moves to cycle the empty around and move the goal one more position left

## Algorithm Requirements

1. **Parse the input** to extract:
   - Grid dimensions (find max X and max Y from node coordinates)
   - Each node's position (x, y), Size, Used, and Avail values
   - Goal node position: the node with y=0 and the highest x value
   - Target node position: (0, 0)

2. **Classify nodes**:
   - Find the empty node(s) where Used = 0T
   - Identify wall/immovable nodes: nodes whose Used value is too large to fit on any other node (typically nodes with very high Size and Used values)
   - Determine which nodes can realistically exchange data

3. **Find minimum steps** using one of these approaches:

   **Approach A - BFS/A\* State Space Search**:
   - State = (goal_position, empty_position)
   - Initial state = ((max_x, 0), (empty_x, empty_y))
   - Goal state = ((0, 0), any_position)
   - For each state, generate valid moves by:
     - Finding adjacent nodes to the empty position
     - Checking if the adjacent node's data can fit in the empty space
     - Creating new state with updated positions
   - Use BFS or A* to find shortest path

   **Approach B - Pattern-based Calculation**:
   - Calculate steps to move empty node to be adjacent to goal (pathfinding around walls)
   - Add 1 step to swap goal with empty
   - For each remaining position the goal must move left:
     - Add 5 steps (the pattern to cycle empty around: down, right, right, up, swap)
   - This works if the grid layout is simple enough

4. **Return** the total minimum step count

## Expected Output
A single integer representing the minimum number of move operations required to move the goal data to `node-x0-y0`.

## Important Implementation Notes

### Node Classification
When analyzing the grid, classify nodes as follows:
- **Empty node**: Used = 0T (there's typically only one)
- **Wall node**: Nodes where Used is significantly larger than most other nodes' capacity, making them effectively immovable
  - If a node's Used value is greater than the Size of normal nodes, it's a wall
  - Walls typically have both large Size AND large Used values
- **Normal nodes**: All other nodes that can participate in data movement

### Algorithm Complexity
- **BFS/A* approach**: More general, guaranteed to find optimal solution, but may explore many states
  - State representation: (goal_x, goal_y, empty_x, empty_y)
  - Need to track visited states to avoid cycles
  - Generate moves by trying to move data FROM adjacent nodes INTO the empty node
- **Analytical approach**: Faster if grid has predictable structure
  - Calculate: (steps to position empty next to goal) + (steps to move goal to target)
  - Moving goal one space left typically requires 5 steps after initial positioning
  - Must account for navigating around wall nodes

### Key Insights
- This is a state-space search problem similar to the classic "15-puzzle" sliding tile game
- The state consists of BOTH the goal data position AND the empty node position
- Wall nodes create obstacles that must be navigated around when moving the empty space
- Once the empty is positioned, moving the goal leftward follows a repeating pattern:
  - Swap goal with empty (1 step, goal moves left)
  - Cycle empty around to the left of goal again (typically 4-5 steps)
- The puzzle is solvable because there's an empty node that can accommodate normal nodes' data
- Be careful with coordinate systems: puzzle uses (x, y) notation where y=0 is the top row
