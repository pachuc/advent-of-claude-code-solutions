# Implementation Plan - Part 2: Tower Balancing

## Overview
Find the program with the wrong weight and determine what its weight should be to balance the tower. This builds directly on Part 1's solution.

## Step 1: Parse Input and Find Root
**Objective:** Parse input to build tree structure and dynamically find root

**Details:**
- Extend the parsing logic from `part_1_solution.py` to also extract weights
- Part 1 only extracted program names and children - we need to ADD weight extraction
- Build a dictionary mapping each program to its own weight
- Build a dictionary mapping each program to its children list
- Find the root node dynamically using Part 1's approach (program that is never a child)

**Data Structures:**
```python
weights = {}          # program_name -> own_weight (int)
children = {}         # program_name -> list of child names
all_programs = set()  # all program names
all_children = set()  # all programs that are children
root = None           # will be found dynamically
```

**Parsing Pattern:**
```
Format: name (weight) -> child1, child2, ...
Example: fwft (72) -> ktlj, cntj, xhth
Parse: name="fwft", weight=72, children=["ktlj", "cntj", "xhth"]
```

**Implementation:**
```python
def parse_input(input_data):
    lines = [line.strip() for line in input_data.strip().split('\n') if line.strip()]

    weights = {}
    children = {}
    all_programs = set()
    all_children = set()

    for line in lines:
        # Split by '->' to separate parent from children
        parts = line.split('->')
        parent_part = parts[0]

        # Extract name and weight
        name = parent_part.split('(')[0].strip()
        weight = int(parent_part.split('(')[1].split(')')[0])

        weights[name] = weight
        all_programs.add(name)

        # Extract children if they exist
        if len(parts) > 1 and parts[1].strip():
            child_list = [child.strip() for child in parts[1].split(',')]
            children[name] = child_list
            all_children.update(child_list)

    # Find root: program that is never a child
    root = (all_programs - all_children).pop()

    return weights, children, root
```

## Step 2: Calculate Total Weights Recursively
**Objective:** Compute total weight for each program (own weight + all descendants)

**Algorithm:**
- Use recursive function with memoization to avoid recalculation
- Base case: leaf node (no children) → total weight = own weight
- Recursive case: total weight = own weight + sum(total weights of all children)

**Implementation:**
```python
def calculate_total_weight(node, weights, children, memo):
    if node in memo:
        return memo[node]

    total = weights[node]
    if node in children:
        for child in children[node]:
            total += calculate_total_weight(child, weights, children, memo)

    memo[node] = total
    return total
```

**Complexity:** O(n) where n = number of programs

## Step 3: Find the Imbalanced Node
**Objective:** Locate the deepest node where children have mismatched total weights

**Strategy:**
- Traverse tree starting from root
- At each node with children, check if all children have the same total weight
- If children weights differ, one is wrong - continue searching in that subtree
- The deepest node with imbalanced children contains the problematic child

**Algorithm:**
```python
def find_imbalanced_node(node, weights, children, total_weights):
    if node not in children or not children[node]:
        return None  # Leaf node, no imbalance here

    # Get total weights of all children
    child_weights = {child: total_weights[child] for child in children[node]}

    # Check if all equal
    if len(set(child_weights.values())) == 1:
        return None  # All balanced at this level

    # Find which child is different
    weight_counts = {}
    for child, weight in child_weights.items():
        if weight not in weight_counts:
            weight_counts[weight] = []
        weight_counts[weight].append(child)

    # The wrong child has a unique weight (appears once)
    wrong_child = None
    correct_weight = None
    for weight, nodes in weight_counts.items():
        if len(nodes) == 1:
            wrong_child = nodes[0]
        else:
            correct_weight = weight

    # Recursively check if the imbalance is deeper
    deeper_imbalance = find_imbalanced_node(wrong_child, weights, children, total_weights)
    if deeper_imbalance:
        return deeper_imbalance

    # This is the deepest imbalance
    return (wrong_child, total_weights[wrong_child], correct_weight)
```

**Key Insight:**
- Multiple children will have the "correct" total weight
- Exactly one child will have the "wrong" total weight
- We search depth-first to find the deepest imbalance

## Step 4: Calculate the Corrected Weight
**Objective:** Determine what the wrong program's own weight should be

**Calculation:**
```python
wrong_program, wrong_total_weight, correct_total_weight = imbalance_info

# The difference in total weights
difference = correct_total_weight - wrong_total_weight

# Adjust the program's own weight
corrected_weight = weights[wrong_program] + difference
```

**Logic:**
- If wrong_total_weight is too high, difference is negative → reduce own weight
- If wrong_total_weight is too low, difference is positive → increase own weight
- The correction affects only the program's own weight, not its children

## Step 5: Main Function Structure
**Objective:** Orchestrate the solution

**Flow:**
```python
def solve_part2(input_data):
    # Step 1: Parse input and find root
    weights, children, root = parse_input(input_data)

    # Step 2: Calculate total weights starting from root
    # (memoization will handle caching during recursion)
    total_weights = {}
    calculate_total_weight(root, weights, children, total_weights)

    # Step 3: Find the imbalanced node
    imbalance = find_imbalanced_node(root, weights, children, total_weights)

    # Step 4: Calculate corrected weight
    wrong_program, wrong_total, correct_total = imbalance
    difference = correct_total - wrong_total
    corrected_weight = weights[wrong_program] + difference

    return corrected_weight

def main():
    # Read input file
    with open('/app/agent_workspace/2017/day_7/part_2/input.md', 'r') as f:
        input_data = f.read()

    # Solve and print result
    result = solve_part2(input_data)
    print(result)
    return result

if __name__ == "__main__":
    main()
```

## Step 6: Testing with Example
**Objective:** Validate with the example from the problem

**Example Input:**
```
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
```

**Expected Behavior:**
- Root should be identified as "tknk"
- `ugml` total weight: 251 (too heavy by 8)
- `padx` and `fwft` total weight: 243 (correct)
- Wrong program: `ugml` with weight 68
- Corrected weight: 60

**Testing:**
- Run solution on example input
- Verify output is 60
- This confirms the algorithm works before running on actual input

## Edge Cases and Assumptions
1. **Multiple children with same weight:** Use counting to identify the outlier - the correct weight will appear 2+ times, wrong weight appears exactly once
2. **Imbalance at root level:** Check root's children first
3. **Imbalance deep in tree:** Recursively search for deepest imbalance
4. **Leaf node as wrong program:** Its total weight equals its own weight (no issue)
5. **Two children case:** If a parent has exactly 2 children with different weights, we recurse into each to find which has the imbalance deeper down. The problem guarantees exactly one wrong program, so this will resolve correctly.

## Optimization Notes
- **Memoization:** Critical for total weight calculation to avoid redundant computations
- **Single tree traversal:** Calculate all total weights in one pass
- **Efficient lookup:** Use dictionaries for O(1) access to weights and children

## Expected Complexity
- **Time:** O(n) where n = number of programs (~1300)
- **Space:** O(n) for storing weights, children, and memoization cache
- **Runtime:** Sub-second for the given input size
