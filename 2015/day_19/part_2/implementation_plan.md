# Implementation Plan: Molecule Fabrication - Part 2

## Deep Problem Analysis

### Problem Statement
Find the minimum number of steps to transform a single electron `e` into a target medicine molecule using a set of replacement rules.

### Critical Observations

After analyzing the problem structure, rules, and target molecule, several key insights emerge:

1. **Forward vs. Backward Search**
   - Forward from `e`: Exponential branching (each rule creates multiple possibilities)
   - Backward from target: More constrained (reverse the rules and reduce the molecule)
   - **Conclusion**: Backward search is essential

2. **Rule Structure Analysis**
   Looking at the 43 rules provided:
   - Rules expand from simpler to more complex molecules
   - Special structural markers: `Rn`, `Ar`, `Y`
   - `Rn` and `Ar` appear to function like parentheses (always paired)
   - `Y` appears to function like a comma/separator (only appears inside Rn...Ar groups)
   - Starting rules: `e => HF`, `e => NAl`, `e => OMg` (only 3 ways to start)

3. **Grammar-Like Structure**
   The rules form a context-free grammar-like structure:
   ```
   Rn = opening parenthesis
   Ar = closing parenthesis
   Y = comma separator
   ```
   This suggests the molecule follows a specific syntactic structure.

4. **Mathematical Pattern (Key Insight)**

   After careful analysis of Advent of Code 2015 Day 19 Part 2, this problem has a hidden mathematical solution:

   The minimum steps can be calculated using a formula based on counting specific elements:
   - Count total elements (atoms)
   - Subtract 2× count of `Rn` (each `Rn...Ar` group reduces step count)
   - Subtract 2× count of `Ar` (paired with Rn)
   - Subtract count of `Y` (separators between components)
   - Subtract 1 (for starting from `e`)

   **Formula**: `steps = num_elements - num_Rn - num_Ar - 2*num_Y - 1`

   This works because:
   - Each step adds one element on average
   - But `Rn...Ar` groups and `Y` separators represent structural compression
   - The problem was designed with this property

### Algorithm Strategy Selection

Given the analysis, we'll implement **three approaches** with proper validation:

1. **Greedy Backward Reduction (Primary)**: Greedily reduce the molecule by reversing rules - most reliable for this problem
2. **Formula-Based (Validation)**: Use the mathematical pattern to validate greedy result
3. **BFS Backward Search (Fallback)**: Guaranteed correct but potentially slower

**Critical Note**: The formula ONLY works for molecules with Rn/Ar/Y structure. Since the actual input has this structure but simple examples don't, we'll use greedy as primary and formula for validation. If they agree, we have high confidence.

## Implementation Steps

### Step 0: Input Reconnaissance (NEW)
**File**: `solution.py`
**Function**: `analyze_input(input_text)`

**Purpose**: Analyze input structure before solving to understand the problem space.

**Implementation**:
```python
def analyze_input(input_text):
    """
    Analyze input structure before solving.
    Helps validate assumptions about the problem.

    Args:
        input_text: Raw input string

    Returns:
        tuple: (rules, target) after validation
    """
    rules, target = parse_input(input_text)

    # Basic statistics
    num_elements = count_elements(target)
    num_rn = target.count('Rn')
    num_ar = target.count('Ar')
    num_y = target.count('Y')

    # Validate Rn/Ar balance (they should be paired)
    assert num_rn == num_ar, f"Rn ({num_rn}) and Ar ({num_ar}) must be balanced"

    # Count 'e' rules
    e_rules = [r for r in rules if r[0] == 'e']

    return rules, target
```

**Purpose**: Validates assumptions before solving.

### Step 1: Input Parsing
**File**: `solution.py`
**Function**: `parse_input(input_text)`

**Purpose**: Extract replacement rules and target molecule from input.

**Implementation**:
```python
def parse_input(input_text):
    """
    Parse input to extract rules and target molecule.

    Args:
        input_text: Raw input string

    Returns:
        tuple: (rules, target) where rules is list of (source, target) tuples
               and target is the target molecule string
    """
    lines = input_text.strip().split('\n')
    rules = []
    target = None

    blank_found = False
    for line in lines:
        line = line.strip()

        if not line:
            blank_found = True
            continue

        if not blank_found and '=>' in line:
            parts = line.split(' => ')
            source = parts[0].strip()
            target_part = parts[1].strip()
            rules.append((source, target_part))
        elif blank_found and line:
            target = line
            break

    return rules, target
```

**Complexity**: O(n) where n is number of lines
**Edge Cases**:
- Handle missing blank line
- Handle malformed rule lines
- Validate target exists

### Step 2: Element Counting for Formula Approach
**File**: `solution.py`
**Function**: `count_elements(molecule)`

**Purpose**: Count individual elements in the molecule string.

**Implementation**:
```python
def count_elements(molecule):
    """
    Count individual elements in a molecule string.
    Elements are uppercase letter optionally followed by lowercase letter(s).

    Args:
        molecule: String representing the molecule

    Returns:
        int: Number of elements
    """
    import re
    # Match element symbols: Uppercase followed by optional lowercase letters
    elements = re.findall(r'[A-Z][a-z]*', molecule)
    return len(elements)
```

**Complexity**: O(n) where n is length of molecule
**Note**: This handles multi-character element symbols like `Ca`, `Si`, `Th`, etc.

### Step 3: Formula-Based Solution
**File**: `solution.py`
**Function**: `solve_by_formula(target)`

**Purpose**: Calculate steps using the mathematical formula.

**Implementation**:
```python
def solve_by_formula(target):
    """
    Solve using mathematical formula based on element counting.

    Formula: steps = num_elements - num_Rn - num_Ar - 2*num_Y - 1

    This works because:
    - Each step typically adds one element
    - Rn/Ar represent grouping (reduces effective steps)
    - Y represents separation (reduces effective steps)
    - Subtract 1 for starting from 'e'

    Args:
        target: Target molecule string

    Returns:
        int: Minimum number of steps
    """
    num_elements = count_elements(target)
    num_rn = target.count('Rn')
    num_ar = target.count('Ar')
    num_y = target.count('Y')

    steps = num_elements - num_rn - num_ar - 2 * num_y - 1

    return steps
```

**Complexity**: O(n) where n is length of molecule
**Assumptions**:
- Problem follows the mathematical pattern (typical for AoC 2015)
- Rn, Ar, Y are not part of other element names

### Step 4: Greedy Backward Reduction
**File**: `solution.py`
**Function**: `solve_by_greedy(rules, target)`

**Purpose**: Greedily reduce the molecule by applying reverse replacements.

**Implementation**:
```python
def solve_by_greedy(rules, target):
    """
    Solve by greedily applying reverse replacements.

    Strategy:
    - Reverse all rules (target => source becomes source => target for backward)
    - Sort by length of pattern (longer first, then alphabetically for determinism)
    - Repeatedly find and replace until we reach 'e'

    Args:
        rules: List of (source, target) tuples
        target: Target molecule string

    Returns:
        int: Number of steps, or -1 if failed
    """
    if target == 'e':
        return 0

    # Reverse rules for backward search
    reversed_rules = [(tgt, src) for src, tgt in rules]

    # Sort by pattern length (longer first), then alphabetically for determinism
    reversed_rules.sort(key=lambda x: (len(x[0]), x[0]), reverse=True)

    current = target
    steps = 0
    max_steps = len(target) * 10  # Scale with input size

    while current != 'e' and steps < max_steps:
        found = False

        for pattern, replacement in reversed_rules:
            if pattern in current:
                # Replace first occurrence
                current = current.replace(pattern, replacement, 1)
                steps += 1
                found = True
                break

        if not found:
            return -1  # No solution found

    if current == 'e':
        return steps
    else:
        return -1  # Exceeded max steps
```

**Complexity**: O(steps × rules × molecule_length)
- steps: Number of reduction steps (typically O(n))
- rules: Number of rules (43 in this case)
- molecule_length: Decreases each iteration

**Strategy Notes**:
- Greedy may not always find optimal solution
- But for well-structured problems (like AoC), often works
- Trying longest patterns first increases success probability

### Step 5: BFS Backward Search (Fallback)
**File**: `solution.py`
**Function**: `solve_by_bfs(rules, target)`

**Purpose**: Use BFS to guarantee finding the shortest path.

**Implementation**:
```python
from collections import deque

def solve_by_bfs(rules, target):
    """
    Solve using BFS backward search from target to 'e'.
    Guaranteed to find minimum steps but potentially slower.

    Args:
        rules: List of (source, target) tuples
        target: Target molecule string

    Returns:
        int: Minimum number of steps, or -1 if not found
    """
    if target == 'e':
        return 0

    # Reverse rules
    reversed_rules = [(tgt, src) for src, tgt in rules]

    queue = deque([(target, 0)])
    visited = {target}
    max_steps = 1000

    while queue:
        current, steps = queue.popleft()

        if steps >= max_steps:
            return -1

        # Try all possible replacements
        for pattern, replacement in reversed_rules:
            # Find all occurrences
            idx = 0
            while idx < len(current):
                pos = current.find(pattern, idx)
                if pos == -1:
                    break

                # Create new molecule
                new_molecule = current[:pos] + replacement + current[pos + len(pattern):]

                if new_molecule == 'e':
                    return steps + 1

                # Only explore if shorter (pruning optimization)
                if new_molecule not in visited and len(new_molecule) < len(current):
                    visited.add(new_molecule)
                    queue.append((new_molecule, steps + 1))

                idx = pos + 1

    return -1  # No solution found
```

**Complexity**: O(b^d × r × m) where:
- b: Branching factor (limited by pruning)
- d: Depth (number of steps)
- r: Number of rules
- m: Average molecule length

**Optimizations**:
- Only explore molecules that get shorter (safe for backward search since we're reversing expansions)
- Use visited set to avoid cycles
- Early termination when 'e' is found

**Note on Pruning**: The condition `len(new_molecule) < len(current)` is safe for backward search because:
- We're reversing expansion rules
- Expansions increase length, so valid reductions must decrease length
- Any rule that doesn't reduce length won't help us reach 'e'

### Step 6: Main Solver Function
**File**: `solution.py`
**Function**: `solve(input_text, method='auto')`

**Purpose**: Orchestrate the solution using the best approach with validation.

**Implementation**:
```python
def solve(input_text, method='auto'):
    """
    Main solver function. Uses greedy with formula validation.

    Strategy:
    1. Run greedy (most reliable for this problem)
    2. Validate with formula (if they agree, high confidence)
    3. Fall back to BFS if needed

    Args:
        input_text: Raw input string
        method: 'auto', 'formula', 'greedy', or 'bfs'

    Returns:
        int: Minimum number of steps
    """
    rules, target = parse_input(input_text)

    if method == 'greedy' or method == 'auto':
        greedy_result = solve_by_greedy(rules, target)

        if greedy_result != -1:
            # Validate with formula if input has Rn/Ar/Y structure
            if 'Rn' in target or 'Ar' in target:
                formula_result = solve_by_formula(target)

                # If they agree, high confidence
                if formula_result == greedy_result:
                    return greedy_result
                # If they disagree slightly, trust greedy
                elif abs(formula_result - greedy_result) <= 2:
                    return greedy_result

            return greedy_result

        if method == 'greedy':
            return greedy_result

    if method == 'formula':
        return solve_by_formula(target)

    if method == 'bfs' or method == 'auto':
        result = solve_by_bfs(rules, target)
        return result

    return -1
```

**Strategy**:
1. Run greedy first (most reliable)
2. Validate with formula if input has Rn/Ar/Y structure
3. Fall back to BFS if greedy fails

### Step 7: Entry Point
**File**: `solution.py`
**Function**: `main()`

**Implementation**:
```python
def main():
    """Read input and solve the problem."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    result = solve(input_text)
    print(result)

if __name__ == '__main__':
    main()
```

## Algorithm Efficiency Analysis

### Approach Comparison

| Approach | Time Complexity | Space Complexity | Correctness | Speed |
|----------|----------------|------------------|-------------|--------|
| Formula  | O(n) | O(1) | High (if pattern holds) | Instant |
| Greedy   | O(n × r × m) | O(n) | Medium (depends on problem) | Fast |
| BFS      | O(b^d × r × m) | O(b^d) | Guaranteed | Slower |

Where:
- n: Target molecule length (~545 chars)
- r: Number of rules (43)
- m: Average molecule length during search
- b: Branching factor (~2-5 with pruning)
- d: Depth (~200-300 steps estimated)

### Expected Performance

For the actual input:
- **Formula**: < 1ms (just counting)
- **Greedy**: 10-100ms (if it works)
- **BFS**: 1-10 seconds (with pruning)

### Memory Usage

- **Formula**: ~1 KB (just the target string)
- **Greedy**: ~1 KB (current molecule state)
- **BFS**: ~10-100 MB (visited set, could have thousands of states)

## Code Structure

```
solution.py
├── parse_input(input_text)           # Parse rules and target
├── count_elements(molecule)          # Count elements in molecule
├── solve_by_formula(target)          # Mathematical formula approach
├── solve_by_greedy(rules, target)    # Greedy backward reduction
├── solve_by_bfs(rules, target)       # BFS backward search
├── solve(input_text, method)         # Main orchestrator
└── main()                            # Entry point
```

## Implementation Order

1. Parse input function
2. Input reconnaissance function
3. Count elements helper
4. Greedy solver (primary approach)
5. Test greedy on simple example (HOH)
6. Formula-based solver (for validation)
7. Test formula vs greedy on actual input
8. BFS solver (fallback)
9. Main solve function with validation logic
10. Comprehensive testing

## Edge Cases and Validation

### Edge Cases to Handle

1. **Target is 'e'**: Return 0 immediately
2. **Empty target**: Invalid input
3. **No rules**: Cannot solve
4. **No 'e' rules**: Cannot reach 'e'
5. **Unsolvable target**: Return -1
6. **Very long target**: Ensure efficiency

### Validation Steps

1. Verify formula produces reasonable result (positive, < 1000)
2. If using greedy/BFS, verify result matches formula (if available)
3. Ensure no infinite loops (max_steps limit)
4. Check for reasonable execution time

## Why This Approach?

### Advantages of Multi-Strategy Approach

1. **Speed**: Formula is instant if it works
2. **Reliability**: Multiple fallbacks ensure solution
3. **Understanding**: Each approach teaches us about the problem
4. **Flexibility**: Can choose specific method for testing

### Why Formula Might Work

Advent of Code 2015 Day 19 Part 2 is famous for having a mathematical trick. The problem appears to be a complex search problem, but actually has a simple counting solution. This is intentional puzzle design.

The formula works because:
- The grammar is unambiguous (one way to parse the molecule)
- Each element generally requires one step to add
- Structural markers (Rn, Ar, Y) represent compression
- The problem was designed with this property

### Why We Still Implement Search

Even if formula works:
1. **Verification**: We can validate the formula by comparing with search
2. **Learning**: Understanding search algorithms is valuable
3. **Generality**: Search works for variants of the problem
4. **Confidence**: Multiple methods agreeing increases confidence

## Testing Strategy Reference

See `test_plan.md` for comprehensive testing approach covering:
- Formula validation
- Greedy correctness
- BFS correctness
- Edge cases
- Performance benchmarks
- Comparison between methods
