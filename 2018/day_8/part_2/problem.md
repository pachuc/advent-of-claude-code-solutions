# Problem Report: Tree Node Value Calculator (Part 2)

## Context from Part 1
In Part 1, we parsed a tree structure encoded as a sequence of space-separated integers. The tree structure consists of nodes where each node has:
1. **Header** (2 numbers): number of child nodes, number of metadata entries
2. **Child nodes** (zero or more, as specified in header)
3. **Metadata entries** (one or more, as specified in header)

Part 1 required us to sum ALL metadata entries across the entire tree. The answer was 49180.

## Part 2 Objective
Calculate the **value of the root node** using a new set of rules that define how node values are computed.

## Input Format
- Same as Part 1: A single line containing space-separated integers
- These numbers encode the same tree structure
- The input file remains the same (input.md)

## Node Value Calculation Rules

The value of a node depends on whether it has child nodes:

### Case 1: Node with NO child nodes (leaf node)
- **Value = sum of its metadata entries**
- Example: Node B has metadata `[10, 11, 12]`, so value = 10 + 11 + 12 = 33

### Case 2: Node with child nodes
- **Metadata entries become 1-based indexes** that reference child nodes
- The value is the **sum of the values of the referenced child nodes**
- Rules for indexing:
  - Metadata entry `1` refers to the 1st child node
  - Metadata entry `2` refers to the 2nd child node
  - And so on...
  - Metadata entry `0` does not refer to any child (skip it)
  - If a metadata entry references a child index that doesn't exist, skip it
  - A child can be referenced multiple times and counts each time

## Example Walkthrough

Using the example tree:
```
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
```

Tree structure:
- **Node A**: 2 children (B, C), metadata: [1, 1, 2]
- **Node B**: 0 children, metadata: [10, 11, 12]
- **Node C**: 1 child (D), metadata: [2]
- **Node D**: 0 children, metadata: [99]

Calculating values (bottom-up):
1. **Node D** (no children): value = 99
2. **Node B** (no children): value = 10 + 11 + 12 = 33
3. **Node C** (has 1 child):
   - Metadata: [2]
   - Child 2 doesn't exist (C only has 1 child)
   - Value = 0 (no valid references)
4. **Node A** (has 2 children):
   - Metadata: [1, 1, 2]
   - Child 1 = Node B (value 33)
   - Child 1 again = Node B (value 33)
   - Child 2 = Node C (value 0)
   - Value = 33 + 33 + 0 = 66

**Root node (A) value = 66**

## Expected Output
A single integer representing the value of the root node.

## Algorithm Approach
1. Parse the input numbers into a list (same as Part 1)
2. Recursively process the tree structure:
   - Read header (child count, metadata count)
   - Recursively process each child node and **store their values**
   - Read metadata entries
   - Calculate node value based on the rules:
     - If no children: sum metadata entries
     - If has children: sum values of children referenced by metadata (using 1-based indexing)
   - Return the node's value
3. Return the value of the root node

## Key Differences from Part 1
- Part 1: Sum all metadata entries across all nodes
- Part 2: Calculate the value of just the root node using the special indexing rules
- Part 2 requires tracking node values during recursion, not just summing metadata
