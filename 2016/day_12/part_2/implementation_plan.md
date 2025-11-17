# Implementation Plan: Assembunny Code Interpreter - Part 2

## Overview
Part 2 uses the exact same assembunny interpreter from Part 1, with only one change: register `c` must be initialized to `1` instead of `0`. The Part 1 solution can be directly adapted with a single-line modification.

## Core Approach
- Reuse the virtual machine interpreter from `part_1_solution.py`
- The interpreter uses an instruction pointer (IP) to track execution position
- Four instructions are supported: `cpy`, `inc`, `dec`, `jnz`
- Execution continues until IP moves outside the instruction range
- Setting `c=1` will cause different execution paths through conditional jumps
- The program should complete efficiently (under 1 second) as it only performs integer arithmetic and loops

## Step-by-Step Implementation

### Step 1: Copy Part 1 Solution Structure
- Copy the entire `part_1_solution.py` as the starting point
- The core functions remain identical:
  - `get_value(operand, registers)`: Returns integer value or register value
  - `parse_instructions(lines)`: Parses input into instruction tuples
  - `execute(instructions)`: Main interpreter loop

### Step 2: Modify Register Initialization
**Location**: `execute()` function, line 26

**Change Required**:
```python
# OLD (Part 1):
registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}

# NEW (Part 2):
registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
```

This is the ONLY code change needed.

### Step 3: Verify Input Parsing
- Confirm `parse_instructions()` correctly handles the input format
- The function should:
  - Strip whitespace from each line
  - Skip empty lines
  - Split on whitespace to extract instruction and operands
  - Handle both 2-part instructions (`inc`, `dec`) and 3-part instructions (`cpy`, `jnz`)

### Step 4: Ensure Correct Instruction Execution
All instruction implementations from Part 1 remain valid:

**`cpy x y`**:
- Resolve `x` to a value (literal or register)
- Store in register `y`
- Increment IP by 1

**`inc x`**:
- Increment register `x` by 1
- Increment IP by 1

**`dec x`**:
- Decrement register `x` by 1
- Increment IP by 1

**`jnz x y`**:
- Resolve `x` to a value
- If non-zero, add `y` (resolved to value) to IP
- If zero, increment IP by 1

### Step 5: Return Result
- After execution completes (IP outside instruction range)
- Return the value in register `a`

## Implementation Checklist
- [ ] Copy `part_1_solution.py` structure
- [ ] Change register `c` initialization from `0` to `1` in the `execute()` function
- [ ] Ensure `get_value()` handles both literals and registers (already implemented)
- [ ] Ensure `parse_instructions()` correctly parses the input (already implemented)
- [ ] Verify `execute()` implements all 4 instructions correctly (already implemented)
- [ ] Verify loop termination condition works (already implemented)
- [ ] Confirm input is read from `input.md` file
- [ ] Print the final value of register `a`
- [ ] Verify output differs from Part 1's answer (318077)

## Edge Cases (Already Handled in Part 1)
1. **Negative jumps**: The `jnz` instruction can jump backwards
2. **Register vs literal operands**: Both `jnz` and `cpy` accept either
3. **Empty lines**: Skipped during parsing
4. **Program termination**: Detected when IP moves outside instruction bounds

## Expected Behavior
- Setting `c=1` triggers different execution paths through conditional jumps
- Runtime should be under 1 second
- Final value in register `a` will differ from Part 1's answer (318077)
- Program terminates normally (no infinite loops)
