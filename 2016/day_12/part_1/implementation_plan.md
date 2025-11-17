# Implementation Plan: Assembunny Code Interpreter

## Overview
Build a Python interpreter for the assembunny assembly-like language that executes instructions on a virtual machine with 4 registers and outputs the final value of register `a`.

## Algorithm Analysis

### Input Analysis
The given input program performs:
1. Initialization (a=1, b=1, d=26)
2. A conditional skip based on register c (initially 0)
3. A loop adding 7 to d (making d=33)
4. A nested loop structure that appears to perform multiplication operations
5. A final nested loop that adds a constant value to register a

### Complexity Considerations
- The program has nested loops, so execution could involve many iterations
- With d=33 and nested multiplication loops, we might execute thousands of instructions
- However, the instruction set is simple and each operation is O(1)
- Overall runtime will be O(total instructions executed), which should be acceptable
- No optimization needed - straightforward interpretation is sufficient

## Implementation Steps

### Step 1: Data Structure Design
**Create the virtual machine state:**
- Dictionary to store 4 registers: `{'a': 0, 'b': 0, 'c': 0, 'd': 0}`
- Instruction pointer (integer) starting at 0
- List to store parsed instructions

**Design choices:**
- Use a dictionary for registers for easy lookup by name
- Store instructions as a list of tuples for efficient random access (needed for jumps)
  - Each tuple format: `(instruction_name, arg1, arg2)` where args can be None
- Keep instruction pointer as a simple integer index

### Step 2: Input Parsing
**Parse the input file:**
1. Read all lines from the input file
2. Strip whitespace and filter out empty lines
3. Split each line into components (instruction name + operands)
4. Store as a list of tuples: `[(instruction, arg1, arg2), ...]`
   - For instructions with fewer than 2 args, use None for missing args

**Parsing strategy:**
```python
instructions = []
for line in file:
    parts = line.strip().split()
    if len(parts) == 2:
        instructions.append((parts[0], parts[1], None))
    elif len(parts) == 3:
        instructions.append((parts[0], parts[1], parts[2]))
```

### Step 3: Helper Functions
**Create utility functions:**

1. **`get_value(operand, registers)`**
   - Purpose: Get the value of an operand (either a register or literal)
   - Logic: Try to parse as integer, if fails, look up in registers
   - Return: Integer value
   ```python
   def get_value(operand, registers):
       try:
           return int(operand)
       except ValueError:
           return registers[operand]
   ```

Note: We don't need an `is_register()` helper function since we trust the input is valid (as specified in problem constraints). The `get_value()` function handles both literals and registers automatically.

### Step 4: Instruction Implementation
**Implement each instruction as a function or match case:**

1. **`cpy x y`**
   - Get value of x (could be literal or register)
   - Set register y to this value
   - Increment instruction pointer by 1

2. **`inc x`**
   - Increment register x by 1
   - Increment instruction pointer by 1

3. **`dec x`**
   - Decrement register x by 1
   - Increment instruction pointer by 1

4. **`jnz x y`**
   - Get value of x (could be literal or register)
   - If value is not zero:
     - Get value of y (could be literal or register)
     - Add y to instruction pointer (note: y can be negative for backward jumps)
   - Else:
     - Increment instruction pointer by 1
   - Important: The main loop condition `0 <= ip < len(instructions)` ensures program terminates if jump goes out of bounds (negative or beyond end)

### Step 5: Main Execution Loop
**Create the interpreter loop:**

```python
def execute(instructions):
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    ip = 0  # instruction pointer

    while 0 <= ip < len(instructions):
        inst, arg1, arg2 = instructions[ip]

        if inst == 'cpy':
            registers[arg2] = get_value(arg1, registers)
            ip += 1
        elif inst == 'inc':
            registers[arg1] += 1
            ip += 1
        elif inst == 'dec':
            registers[arg1] -= 1
            ip += 1
        elif inst == 'jnz':
            if get_value(arg1, registers) != 0:
                ip += get_value(arg2, registers)
            else:
                ip += 1

    return registers['a']
```

**Key considerations:**
- Loop continues while instruction pointer is within valid range
- When ip goes beyond the instruction list, program halts
- Each instruction must properly update the instruction pointer

### Step 6: Main Program Structure
**Put it all together:**

1. Read input from file (input.md)
2. Parse instructions into data structure
3. Execute instructions
4. Print the value of register `a`

```python
def main():
    # Read and parse input
    with open('input.md', 'r') as f:
        instructions = parse_instructions(f.readlines())

    # Execute
    result = execute(instructions)

    # Output
    print(result)

if __name__ == '__main__':
    main()
```

## Efficiency Considerations

### Time Complexity
- Parsing: O(n) where n is the number of instructions
- Execution: O(k) where k is the total number of instructions executed
  - For this input, k could be in the thousands due to nested loops
  - Each instruction is O(1), so this is acceptable

### Space Complexity
- O(n) to store the instruction list
- O(1) for the 4 registers
- Overall: O(n)

### Why No Optimization Needed
- The instruction set is simple with no complex operations
- Even with nested loops, modern computers can execute millions of simple operations per second
- The input size (23 instructions) is small
- Total executed instructions will likely be under 100,000, which executes in milliseconds
- This is a one-time script, not a performance-critical system

## Code Structure

```
solution.py
├── get_value(operand, registers) -> int
├── parse_instructions(lines) -> list
├── execute(instructions) -> int
└── main()
```

## Implementation Notes
- No need for extensive error handling (we trust the input is valid)
- No need for debugging output unless testing
- Keep code simple and readable
- Use Python's built-in features (dictionaries, string operations)
- No external libraries needed
