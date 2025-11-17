# Implementation Plan: Circuit Signal Simulation (Part 2)

## Overview
Simulate a circuit of wires and bitwise logic gates to determine the signal on wire `a` after running the simulation twice: first with original instructions, then with wire `b` overridden by the first result.

## Algorithm Approach

### Strategy: Memoized Recursive Evaluation
Use a recursive evaluation approach with memoization (caching) to efficiently compute wire values only when needed and avoid redundant calculations.

**Time Complexity:** O(n) where n is the number of wires/instructions (each wire is evaluated at most once per simulation run due to memoization)

**Space Complexity:** O(n) for storing the instruction map and memoization cache

**Why This Approach:**
- The circuit forms a Directed Acyclic Graph (DAG) of dependencies
- Recursive evaluation naturally handles dependency resolution
- Memoization prevents redundant calculations
- More efficient than iterative approaches that may require multiple passes
- Cleaner code structure compared to topological sorting

## Step-by-Step Implementation

### Step 1: Parse Input Instructions
**Goal:** Convert text instructions into a structured format for evaluation

**Details:**
- Read all lines from the input file
- For each line, parse the instruction format:
  - Split by `->` to get operation and target wire
  - Parse the operation part based on keywords (AND, OR, NOT, LSHIFT, RSHIFT)
  - Store in a dictionary: `{wire_name: instruction_data}`
- Instruction data should include:
  - Operation type (ASSIGN, AND, OR, NOT, LSHIFT, RSHIFT)
  - Operands (can be wire names or numeric values)

**Data Structure:**
```python
instructions = {
    'a': {'op': 'SIGNAL', 'args': ['lx']},      # Wire assignment
    'b': {'op': 'SIGNAL', 'args': ['44430']},   # Direct value (stored as string, converted on evaluation)
    'x': {'op': 'OR', 'args': ['v', 'w']},      # Binary operation
    'i': {'op': 'NOT', 'args': ['y']},          # Unary operation
    # ... etc
}
```

**Note:** We use 'SIGNAL' for all direct assignments (both numeric and wire-to-wire). During evaluation, we'll check if the argument is numeric or a wire reference.

### Step 2: Implement Value Resolution Helper
**Goal:** Resolve a value that can be either a wire reference or a numeric literal

**Details:**
- Create a helper function `resolve_value(operand, memo)`
- If operand is numeric string, convert to integer
- If operand is wire name, recursively evaluate that wire
- Use memoization to avoid re-evaluating wires

### Step 3: Implement Wire Evaluation Function
**Goal:** Recursively evaluate any wire's signal value

**Details:**
- Create function `evaluate_wire(wire_name, instructions, memo)`
- Check if value already in memo cache, return if so
- Retrieve instruction for the wire
- Based on operation type:
  - **SIGNAL:** Direct value or resolve another wire (use resolve_value helper)
  - **AND:** Resolve both operands, compute bitwise AND
  - **OR:** Resolve both operands, compute bitwise OR
  - **NOT:** Resolve operand, compute bitwise complement using `~value & 0xFFFF`
  - **LSHIFT:** Resolve operand, left shift by amount, mask to 16 bits
  - **RSHIFT:** Resolve operand, right shift by amount
- Store result in memo cache
- Return result

**Important:** All values must be masked to 16 bits (value & 0xFFFF) to handle overflow

### Step 4: First Simulation Run
**Goal:** Execute circuit with original instructions to get wire `a`'s initial value

**Details:**
- Parse input instructions
- Create empty memo dictionary
- Call `evaluate_wire('a', instructions, memo)`
- Store the result as `original_a_value`

### Step 5: Override Wire `b`
**Goal:** Modify instructions to set wire `b` to the value from step 4

**Details:**
- Update the instructions dictionary for wire `b`:
  - Change to a SIGNAL operation with `original_a_value` as a string
- Alternative: Create a modified copy of instructions

**Example:**
```python
instructions['b'] = {'op': 'SIGNAL', 'args': [str(original_a_value)]}
```

### Step 6: Second Simulation Run **CRITICAL**
**Goal:** Re-run circuit with modified wire `b` to get new wire `a` value

**Details:**
- **MUST create a fresh, empty memo dictionary** - this is critical for correctness
- Do NOT reuse the memo from the first run
- Keep the modified instructions from step 5
- Call `evaluate_wire('a', instructions, memo)`
- This is the final answer

**Warning:** Failing to clear memo is the most common bug - the second run will return stale cached values

### Step 7: Output Result
**Goal:** Display the final signal value on wire `a`

**Details:**
- Print the result from step 6 as a single integer

## Key Implementation Considerations

### 1. Bitwise Operations
- **AND:** `value1 & value2`
- **OR:** `value1 | value2`
- **NOT:** `~value & 0xFFFF` (use bitwise NOT with 16-bit mask)
  - Note: Python's `~` operator produces negative numbers (e.g., `~123 = -124`)
  - The `& 0xFFFF` mask is **required** to get the correct 16-bit unsigned result
  - Alternative `65535 - value` works but is less idiomatic
- **LSHIFT:** `(value << amount) & 0xFFFF`
- **RSHIFT:** `value >> amount`

### 2. 16-bit Unsigned Integer Constraint
- All results must be in range [0, 65535]
- Apply mask `& 0xFFFF` after operations that could overflow
- NOT operation: complement within 16 bits = 65535 - value

### 3. Memoization **CRITICAL**
- Use dictionary to cache wire values
- **MUST clear cache between simulation runs** - create a fresh empty dictionary
- Failure to clear memo will cause incorrect results in the second simulation
- Only memo stores the computed wire values, instructions remain unchanged (except wire `b`)
- Common bug: Reusing the same memo object between runs

### 4. Operand Handling
- Operands can be:
  - Numeric literals (e.g., "123", "1")
  - Wire names (e.g., "x", "ab", "lx")
- Check if operand is digit to distinguish between types
- Use `str.isdigit()` or try/except with int conversion

### 5. Parsing Details
- Direct numeric assignment: `123 -> x` - parsed as SIGNAL operation with args ['123']
- Wire-to-wire assignment: `lx -> a` - parsed as SIGNAL operation with args ['lx']
- Mixed operands: `1 AND x -> y` - AND operation with args ['1', 'x']
- During evaluation, use `resolve_value()` to determine if operand is numeric or wire reference

## Code Structure

```python
def parse_instructions(lines):
    """Parse input lines into instruction dictionary"""
    pass

def resolve_value(operand, instructions, memo):
    """Resolve operand to integer value (handle both literals and wire refs)"""
    pass

def evaluate_wire(wire_name, instructions, memo):
    """Recursively evaluate wire value with memoization"""
    pass

def simulate_circuit(instructions):
    """Run circuit simulation and return wire 'a' value"""
    pass

def main():
    # Read input
    # Parse instructions
    # First run
    original_a = simulate_circuit(instructions)

    # Override wire b
    instructions['b'] = {'op': 'SIGNAL', 'args': [str(original_a)]}

    # Second run (simulate_circuit creates fresh memo internally)
    final_a = simulate_circuit(instructions)

    # Output
    print(final_a)
```

## Optimization Notes

### Why This is Efficient
- **Single evaluation per wire:** Memoization ensures each wire is computed once per run
- **Lazy evaluation:** Only computes wires needed for target wire `a`
- **No multiple passes:** Recursive approach follows dependencies directly
- **Minimal overhead:** Simple dictionary lookups and integer operations

### Input Size Considerations
- Input has 340 instructions
- Circuit depth is likely logarithmic or small linear
- Worst case: O(340) wire evaluations per run
- Two simulation runs = O(680) operations total
- This is extremely efficient even for larger inputs

### Alternative Approaches Considered
1. **Iterative with multiple passes:** Less efficient, may require O(n²) in worst case
2. **Topological sort:** More complex, same O(n) but higher constant overhead
3. **Event-driven simulation:** Overkill for this DAG structure

## Common Pitfalls to Avoid

### 1. Forgetting to Clear Memo Between Runs ⚠️
**Most common bug!** Always create a fresh memo dictionary for the second simulation.

### 2. Forgetting 16-bit Masking
Apply `& 0xFFFF` after LSHIFT operations and NOT operations to ensure values stay in [0, 65535].

### 3. Python's NOT Operator Produces Negative Numbers
`~123` in Python gives `-124`, not the 16-bit complement. Always use `~value & 0xFFFF`.

### 4. Confusing Wire Names with Numeric Literals
The operand "1" is a number, "a" is a wire. Use `str.isdigit()` or try/except to distinguish.

### 5. Incorrect NOT Calculation
NOT is **not** `65535 - value` in general bitwise logic, though it works for 16-bit values. Use `~value & 0xFFFF` for correctness.

## Input-Specific Notes (for reference)
- Wire `b` initially has value `44430` in the provided input (line 4)
- Wire `a` receives its value from wire `lx` (line 96: `lx -> a`)
- Wire `c` is assigned constant `0` (line 122: `0 -> c`)

## Error Handling
Since this is a script for a specific problem, minimal error handling needed:
- Assume input is well-formed
- Assume no circular dependencies (problem guarantees DAG)
- Assume all wire references are valid
