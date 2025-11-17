# Problem Report: Grid Computing - Viable Pairs Count

## Objective
Count the number of viable pairs of storage nodes in a grid computing cluster to understand how data can be rearranged across the grid.

## Context
We have access to a massive storage cluster arranged in a grid where each storage node is only connected to its four adjacent nodes (or fewer for edge/corner nodes). While we can only directly access data on node `/dev/grid/node-x0-y0`, we need to understand the arrangement of data across all nodes to plan how to shift data around by moving it between adjacent nodes.

## Input Format
The input is the output of a `df -h` command showing disk usage for all nodes in the grid. The format is:

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

## Task Definition
A **viable pair** is defined as any two nodes (A, B) that satisfy ALL of the following conditions:

1. Node A is **not empty** (its `Used` value is not zero)
2. Nodes A and B are **not the same node**
3. The data on node A (its `Used` value) **would fit** on node B (A's `Used` ≤ B's `Avail`)

**Important notes:**
- Viable pairs are counted regardless of whether nodes A and B are directly connected
- Order matters: (A, B) is different from (B, A) - both should be counted if they each satisfy the conditions
- We're looking at whether data COULD theoretically be moved, not whether it's actually possible given the grid's adjacency constraints

## Expected Output
A single integer representing the total count of viable pairs of nodes.

## Algorithm Requirements
1. Parse the input to extract the `Used` and `Avail` values for each node
2. For each pair of distinct nodes (A, B):
   - Check if A's `Used` > 0
   - Check if A's `Used` ≤ B's `Avail`
   - If both conditions are true, count this as a viable pair
3. Return the total count of viable pairs
