# Implementation Plan: Computer Instruction Simulator

## Problem Analysis

We need to build a simple virtual machine simulator that:
- Has two registers (a, b) initialized to 0
- Executes 6 types of instructions sequentially
- Handles relative jumps and conditional branching
- Stops when instruction pointer goes out of bounds
- Returns the final value of register b

### Input Analysis
The provided input has 48 instructions with:
- Register operations (hlf, tpl, inc)
- Unconditional jumps (jmp)
- Conditional jumps (jie, jio)
- Two distinct code paths (lines 1-21 and lines 23-40)
- A loop structure at the end (lines 42-48)

### Algorithm Complexity
- Time Complexity: O(n) where n is the number of instruction executions
  - Worst case: The program may loop, but the input appears designed to terminate
  - Each instruction is O(1) to execute
  - The loop at the end will execute log(a) times as it halves register a
- Space Complexity: O(m) where m is the number of instructions (to store the program)
  - We only need to store the instruction list and two register values
  - No additional data structures needed

### Key Implementation Considerations
1. **Parsing**: Instructions have varying formats (register-only vs jump with offsets)
2. **Jump Offsets**: Must handle both positive and negative offsets correctly
3. **Conditional Logic**: jie (even) and jio (equals 1) have different conditions
4. **Termination**: Program ends when IP < 0 or IP >= program length
5. **Register Access**: Need efficient way to read/write registers by name

## Step-by-Step Implementation Plan

### Step 1: File I/O and Input Reading
**What to do:**
- Read the input file containing instructions
- Store each line as a string in a list
- Strip whitespace and handle empty lines if any

**Implementation details:**
```python
def read_input(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]
```

### Step 2: Instruction Parsing
**What to do:**
- Create a function to parse each instruction into a structured format
- Extract instruction type, register (if applicable), and offset (if applicable)
- Pre-parse all instructions once at the start for efficiency (avoids re-parsing in loops)

**Implementation details:**
- Split each instruction by spaces
- Handle comma separations for conditional jumps
- Return a tuple: (operation, register_or_None, offset_or_None)

**Parsing logic:**
- For `hlf/tpl/inc r`: Extract operation and register name
- For `jmp offset`: Extract offset value (convert to int, handles +/- signs)
- For `jie/jio r, offset`: Extract operation, register name, and offset

**Input assumptions:** We assume all input is well-formed per problem constraints, so no error handling is needed for malformed instructions.

```python
def parse_instruction(line):
    parts = line.replace(',', '').split()
    op = parts[0]

    if op in ['hlf', 'tpl', 'inc']:
        return (op, parts[1], None)
    elif op == 'jmp':
        return (op, None, int(parts[1]))
    elif op in ['jie', 'jio']:
        return (op, parts[1], int(parts[2]))
```

### Step 3: Register Management
**What to do:**
- Initialize a dictionary or simple variables to hold register values
- Create helper functions to get/set register values by name

**Implementation details:**
```python
registers = {'a': 0, 'b': 0}
# Access: registers[reg_name]
# Update: registers[reg_name] = new_value
```

### Step 4: Instruction Execution Logic
**What to do:**
- Create a function to execute a single instruction
- Implement logic for each of the 6 instruction types
- Return the new instruction pointer value

**Implementation details:**

**For arithmetic operations (hlf, tpl, inc):**
- `hlf`: registers[r] //= 2, then ip += 1
- `tpl`: registers[r] *= 3, then ip += 1
- `inc`: registers[r] += 1, then ip += 1

**For jumps:**
- `jmp`: ip += offset
- `jie`: if registers[r] % 2 == 0: ip += offset, else: ip += 1
- `jio`: if registers[r] == 1: ip += offset, else: ip += 1

```python
def execute_instruction(instruction, ip, registers):
    op, reg, offset = instruction

    if op == 'hlf':
        registers[reg] //= 2
        return ip + 1
    elif op == 'tpl':
        registers[reg] *= 3
        return ip + 1
    elif op == 'inc':
        registers[reg] += 1
        return ip + 1
    elif op == 'jmp':
        return ip + offset
    elif op == 'jie':
        if registers[reg] % 2 == 0:
            return ip + offset
        return ip + 1
    elif op == 'jio':
        if registers[reg] == 1:
            return ip + offset
        return ip + 1
```

### Step 5: Main Execution Loop
**What to do:**
- Pre-parse all instructions once for efficiency
- Create the main simulator loop
- Initialize instruction pointer to 0
- Execute instructions until termination condition is met
- Detect out-of-bounds instruction pointer
- Optionally add infinite loop detection for safety

**Implementation details:**
```python
def simulate(instruction_strings):
    # Pre-parse all instructions once
    instructions = [parse_instruction(line) for line in instruction_strings]
    registers = {'a': 0, 'b': 0}
    ip = 0

    # Optional: safety check for infinite loops
    MAX_ITERATIONS = 1_000_000
    iteration_count = 0

    while 0 <= ip < len(instructions):
        # Optional: infinite loop detection
        if iteration_count > MAX_ITERATIONS:
            raise RuntimeError("Possible infinite loop detected")
        iteration_count += 1

        # Optional: debug output
        # if DEBUG:
        #     print(f"IP={ip}, Instr={instruction_strings[ip]}, a={registers['a']}, b={registers['b']}")

        ip = execute_instruction(instructions[ip], ip, registers)

    return registers
```

**Note on return value:** The function returns the full `registers` dictionary to support testing both registers. The main function will extract `registers['b']` for the final answer.

### Step 6: Main Program Entry Point
**What to do:**
- Read input file
- Run simulation
- Extract and print the result (value of register b)

**Implementation details:**
```python
def main():
    instructions = read_input('input.md')
    registers = simulate(instructions)
    print(registers['b'])

if __name__ == '__main__':
    main()
```

## Complete Program Structure

```
solution.py
├── read_input(filename) -> list[str]
│   └── Reads instruction lines from file
├── parse_instruction(line) -> tuple(op, reg, offset)
│   └── Parses a single instruction line into structured format
├── execute_instruction(instruction, ip, registers) -> int
│   └── Executes one instruction, returns new IP
├── simulate(instruction_strings) -> dict
│   ├── Pre-parses all instructions
│   ├── Initializes registers
│   ├── Runs execution loop with optional safety checks
│   └── Returns register dictionary
└── main()
    ├── Calls read_input()
    ├── Calls simulate()
    └── Prints registers['b']
```

## Efficiency Considerations

1. **Pre-parsing optimization**: We pre-parse all instructions once at the start to avoid re-parsing in loops
   - For 48 instructions, this is negligible overhead but cleaner design
   - Prevents repeated string operations during execution
2. **Direct register access**: Using a dictionary for registers is efficient (O(1) lookup)
3. **Simple instruction execution**: Each instruction is O(1) to execute
4. **Loop termination**: The program naturally terminates when IP goes out of bounds
5. **Optional safety checks**: MAX_ITERATIONS guard prevents infinite loops without affecting normal execution

## Edge Cases to Handle in Implementation

1. **Register initialization**: Both registers must start at 0
2. **Integer division**: Use `//` for halving to ensure integer result
3. **Jump offset parsing**: Strip the `+` sign, handle `-` sign correctly
4. **Comma in conditional jumps**: Must remove comma when parsing
5. **Out-of-bounds detection**: Check both lower (< 0) and upper (>= len) bounds

## Expected Behavior

Based on the input (48 instructions, indices 0-47):
1. Line 0: `jio a, +22` - since a=0 (not 1), skip to line 1
2. Lines 1-21: Multiple operations on register a, building up its value
3. Line 22: `jmp +19` - jump to line 41
4. Line 41: `jio a, +8` - if a==1, skip to end; otherwise continue
5. Lines 42-48: Loop that increments b and manipulates a until termination

The program will eventually halt when IP reaches 48 or beyond (out of bounds past the last instruction at index 47).

## Optional Features

**Debug Output:** Add a DEBUG flag to enable execution tracing:
```python
DEBUG = False  # Set to True for debugging

if DEBUG:
    print(f"IP={ip}, Instr={instruction_strings[ip]}, a={registers['a']}, b={registers['b']}")
```

**Infinite Loop Detection:** The MAX_ITERATIONS check (suggested 1,000,000) will catch accidental infinite loops during development.
