# Problem Report: Tree License Number Calculator

## Context
We need to fix a navigation system by processing its license file. The license file contains numbers that define a tree data structure, which must be parsed to calculate a license number.

## Objective
Calculate the sum of all metadata entries in a tree structure encoded as a sequence of numbers.

## Input Format
- A single line containing space-separated integers
- These numbers encode a tree structure in a specific format (see Tree Structure Format below)

## Tree Structure Format

### Node Definition
Each node in the tree consists of:
1. **Header** (exactly 2 numbers):
   - First number: quantity of child nodes
   - Second number: quantity of metadata entries
2. **Child nodes** (zero or more, as specified in header)
3. **Metadata entries** (one or more, as specified in header)

### Parsing Rules
- Nodes are encoded in a depth-first, pre-order traversal format
- After a node's header, all of its child nodes appear (recursively) before its metadata entries
- Child nodes are themselves complete node structures (header + children + metadata)

### Example
```
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
```

Breaking this down:
- **Node A**: `2 3` (2 children, 3 metadata) `... 1 1 2` (metadata at end)
  - **Node B**: `0 3 10 11 12` (0 children, 3 metadata: 10, 11, 12)
  - **Node C**: `1 1 ... 2` (1 child, 1 metadata: 2)
    - **Node D**: `0 1 99` (0 children, 1 metadata: 99)

All metadata entries: 10, 11, 12, 99, 2, 1, 1, 2

## Expected Output
A single integer representing the sum of all metadata entries across all nodes in the tree.

For the example above: `10 + 11 + 12 + 99 + 2 + 1 + 1 + 2 = 138`

## Algorithm Approach
1. Parse the input numbers into a list
2. Recursively process the tree structure:
   - Read header (child count, metadata count)
   - Recursively process each child node
   - Read metadata entries
   - Collect all metadata values
3. Sum all collected metadata entries
4. Return the total sum
