# Implementation Plan: Coprocessor Instruction Counter

## Overview
Build a simple assembly interpreter that executes a coprocessor program and counts how many times the `mul` instruction is invoked.

## Algorithm Analysis

### Complexity Considerations
- **Time Complexity**: The program contains loops (via `jnz` instructions). Analyzing the input reveals nested loops that could potentially execute many iterations.
- **Space Complexity**: O(1) - only 8 registers and instruction list storage needed
- **Input Size**: 32 instructions in the input - manageable size
- **Potential Runtime**: The nested loop structure (lines 10-24) suggests this could be computationally expensive, but since we're only counting `mul` invocations in debug mode (register `a` starts at 0), execution should complete in reasonable time.

### Key Observations from Input
1. Register `a` starts at 0 (debug mode)
2. Line 3: `jnz a 2` - since `a=0`, this will NOT jump (continues to line 4)
3. Line 4: `jnz 1 5` - since 1 is not zero, this WILL jump by 5 (skips to line 9)
4. Lines 5-8 are skipped in debug mode
5. The main execution involves nested loops starting at line 9

## Step-by-Step Implementation Plan

### Step 1: Parse Input Instructions
**File**: `solution.py`

1. Read the input file (`input.md`) using standard file I/O
2. For each line:
   - Strip whitespace using `.strip()`
   - Skip empty lines (check `if not line`)
   - Split line into parts using `.split()`
   - Store as tuple with exactly 3 elements: `(op, arg1, arg2)`
3. All instructions in this problem have exactly 2 operands, so all tuples will have 3 elements

**Data Structure**:
```python
instructions = [
    ("set", "b", "67"),     # Operands stored as strings
    ("set", "c", "b"),      # Will be resolved by get_value()
    ("jnz", "a", "2"),
    # ... etc
]
```

**Parsing Implementation**:
```python
def parse_instructions(lines):
    instructions = []
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        parts = line.split()
        # All instructions have format: op arg1 arg2
        instructions.append((parts[0], parts[1], parts[2]))
    return instructions
```

**Note**: Operands are kept as strings during parsing. The `get_value()` helper function will resolve them to integers during execution. This separation of concerns keeps parsing simple.

### Step 2: Initialize Program State
1. Create a dictionary for 8 registers (`a` through `h`), all initialized to 0
2. Initialize instruction pointer (`ip`) to 0
3. Initialize `mul_count` counter to 0

**Data Structure**:
```python
registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}
ip = 0
mul_count = 0
```

### Step 3: Implement Helper Function - Get Value
Create a helper function to resolve operand values:
- If operand is a register name (single letter a-h), return the register's current value
- If operand is a number (could be negative), convert to integer and return it

**Function Signature**:
```python
def get_value(operand: str, registers: dict) -> int:
    if operand.lstrip('-').isdigit():
        return int(operand)
    else:
        return registers[operand]
```

### Step 4: Implement Instruction Execution
Create functions or a switch-case structure for each instruction type:

#### 4.1: `set X Y`
- Get value of Y (using helper function)
- Set register X to that value
- Increment instruction pointer by 1

#### 4.2: `sub X Y`
- Get value of Y
- Subtract Y from register X
- Store result in register X
- Increment instruction pointer by 1

#### 4.3: `mul X Y`
- Get value of Y
- Multiply register X by Y
- Store result in register X
- **Increment mul_count by 1** (this is what we're tracking!)
- Increment instruction pointer by 1

#### 4.4: `jnz X Y`
- Get value of X
- If X != 0:
  - Get value of Y (the offset)
  - Add offset to instruction pointer
- Else:
  - Increment instruction pointer by 1 (normal progression)

### Step 5: Main Execution Loop
Implement the main interpreter loop with careful instruction pointer management:

```python
while 0 <= ip < len(instructions):
    op, arg1, arg2 = instructions[ip]

    # jnz is special - it handles ip itself
    if op == "jnz":
        x_val = get_value(arg1, registers)
        if x_val != 0:
            offset = get_value(arg2, registers)
            ip += offset  # Jump by offset
        else:
            ip += 1  # No jump, proceed normally
    else:
        # All other instructions: execute then increment ip
        if op == "set":
            registers[arg1] = get_value(arg2, registers)
        elif op == "sub":
            registers[arg1] -= get_value(arg2, registers)
        elif op == "mul":
            registers[arg1] *= get_value(arg2, registers)
            mul_count += 1  # Track mul invocations

        ip += 1  # Common increment for non-jump instructions
```

**Key Points**:
- `jnz` handles `ip` internally (either jumps OR increments)
- All other instructions execute, then `ip` increments by 1
- This separation prevents double-incrementing the instruction pointer

**Termination Condition**: Loop exits when `ip` goes outside the valid range `[0, len(instructions))`.

### Step 6: Return Result
After the loop terminates, return or print the `mul_count` value.

### Step 7: Main Entry Point
Create a main function or script entry point:

```python
def main():
    # Read input file
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse instructions
    instructions = parse_instructions(lines)

    # Execute program
    result = execute_program(instructions)

    # Print result (just the number)
    print(result)
```

**Output Format**: Print only the numeric result (e.g., `6724`) for easy verification.

**Error Handling**: Not needed - we assume input is well-formed and from a trusted source (this is a scripting solution, not production code).

## Implementation Structure

```python
def parse_instructions(lines):
    """Parse input lines into instruction tuples"""
    pass

def get_value(operand, registers):
    """Resolve operand to actual value"""
    pass

def execute_program(instructions):
    """Main interpreter loop"""
    # Initialize state
    # Loop until ip out of bounds
    # Execute each instruction
    # Return mul_count
    pass

def main():
    """Entry point"""
    # Read input
    # Parse
    # Execute
    # Print result
    pass

if __name__ == "__main__":
    main()
```

## Optimization Considerations

### Not Needed for This Problem
- No memoization required (stateful execution)
- No need for JIT compilation or optimization
- The debug mode (register `a` = 0) keeps runtime manageable

### Sufficient Approach
- Simple interpreter with direct instruction execution
- O(1) register lookups using dictionary
- Straightforward loop execution

## Edge Cases to Handle in Implementation

1. **Empty lines in input**: Skip them during parsing
2. **Negative number operands**: Handle correctly with `int()` conversion
3. **Jump to same instruction**: `jnz 1 0` would create infinite loop (not in our input)
4. **Jump beyond bounds**: Natural termination - loop condition handles this
5. **Register names**: Ensure we handle single letters a-h

## Expected Runtime

Given the input structure and debug mode (a=0):
- The program will skip the multiplication at line 5
- Main nested loops will execute but terminate naturally
- Expected runtime: < 1 second for debug mode
- Expected mul_count: Unknown initially, but should be:
  - Greater than 0 (there are `mul` instructions in the loops)
  - Less than 1,000,000 (sanity check for reasonable execution)
  - Will be validated by running the implementation
  - If this is from Advent of Code, the answer can be submitted for verification

**Validation Approach**: Since the exact answer is unknown, we will:
1. Run the implementation and record the result
2. Manually trace the first few iterations to verify correctness
3. Ensure the program terminates (doesn't hang)
4. Submit to Advent of Code or compare with expected output if available
