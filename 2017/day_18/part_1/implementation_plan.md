# Implementation Plan: Duet Assembly Interpreter

## Problem Analysis

We need to build an interpreter for a simple assembly language that:
- Maintains register state (all starting at 0)
- Executes 7 different instruction types
- Tracks the last sound frequency played
- Stops when `rcv` is executed with a non-zero register value
- Returns the last sound frequency at that point

### Input Characteristics
- 42 lines of assembly code
- Uses registers: i, a, p, b, f
- Contains loops (via `jgz` instructions)
- Has multiple `snd` and `rcv` instructions

### Algorithm Complexity
- **Time Complexity**: O(n) where n is the number of instructions executed (could loop)
- **Space Complexity**: O(r) where r is the number of unique registers (constant, ~5-10)
- The input contains loops, but they are bounded by counter variables, so execution should terminate

## Step-by-Step Implementation Plan

### Step 1: Input Parsing
**Goal**: Read and parse the input file into a list of instructions

**Details**:
1. Read the input file line by line
2. Strip whitespace and ignore empty lines
3. Split each line into tokens (operation + operands)
4. Store as a list of instruction tuples/lists
   - Example: `["set", "a", "1"]` or `["jgz", "i", "-2"]`

**Data Structure**: List of lists/tuples
```python
instructions = [
    ["set", "i", "31"],
    ["set", "a", "1"],
    ...
]
```

### Step 2: Initialize State
**Goal**: Set up the execution environment

**Details**:
1. Create a dictionary for registers (defaultdict(int) for auto-initialization to 0)
2. Create a variable to track the last sound frequency (initialize to None or 0)
3. Create an instruction pointer (pc = program counter) starting at 0

**Data Structures**:
```python
from collections import defaultdict
registers = defaultdict(int)  # Auto-initializes to 0
last_sound = None
pc = 0  # Program counter
```

### Step 3: Helper Function - Value Resolution
**Goal**: Create a function to resolve operand values (register or literal)

**Details**:
1. Try to parse operand as an integer (literal value)
2. If successful: return the integer value
3. If not: treat as register name and return `registers[operand]`
4. Handle negative numbers correctly

**Function Signature**:
```python
def get_value(operand: str, registers: dict) -> int:
    """Resolve an operand to its integer value.

    Args:
        operand: Either a register name (e.g., 'a') or a literal value (e.g., '42', '-5')
        registers: Dictionary of register values

    Returns:
        The integer value of the operand
    """
    try:
        return int(operand)
    except ValueError:
        return registers[operand]
```

**Rationale**: Using try/except with int() is more robust than checking if the string is a digit, as it handles all edge cases including negative numbers and multi-character strings.

### Step 4: Implement Instruction Handlers
**Goal**: Implement each of the 7 instructions

**Details**:

#### 4.1 `snd X` - Play Sound
- Resolve value of X (could be register or literal)
- Store in `last_sound` variable
- Increment pc by 1

#### 4.2 `set X Y` - Set Register
- Resolve value of Y
- Set `registers[X] = value_of_Y`
- Increment pc by 1

#### 4.3 `add X Y` - Add to Register
- Resolve value of Y
- Add to register: `registers[X] += value_of_Y`
- Increment pc by 1

#### 4.4 `mul X Y` - Multiply Register
- Resolve value of Y
- Multiply: `registers[X] *= value_of_Y`
- Increment pc by 1

#### 4.5 `mod X Y` - Modulo Operation
- Resolve value of Y
- Set: `registers[X] %= value_of_Y`
- Increment pc by 1

#### 4.6 `rcv X` - Recover Frequency (TERMINATION CONDITION)
- Resolve value of X
- If value is non-zero:
  - Return `last_sound` (this is our answer!)
- If value is zero:
  - Do nothing, increment pc by 1

#### 4.7 `jgz X Y` - Jump if Greater than Zero
- Resolve value of X
- Resolve value of Y (the offset)
- If X > 0:
  - Set `pc += value_of_Y`
- Else:
  - Increment pc by 1

### Step 5: Main Execution Loop
**Goal**: Execute instructions until termination

**Details**:
1. Loop while `0 <= pc < len(instructions)`
2. Fetch instruction at `instructions[pc]`
3. Parse operation and operands
4. Execute appropriate instruction handler
5. Check for termination (rcv with non-zero returns immediately)
6. Handle jumps correctly (pc already modified by instruction)
7. Break if pc goes out of bounds

**Structure**:
```python
while 0 <= pc < len(instructions):
    instruction = instructions[pc]
    op = instruction[0]

    if op == "snd":
        # Handle snd
    elif op == "set":
        # Handle set
    # ... etc
    elif op == "rcv":
        value = get_value(instruction[1])
        if value != 0:
            return last_sound  # DONE!
        pc += 1
    # ... etc
```

### Step 6: Output Result
**Goal**: Return/print the recovered frequency

**Details**:
1. When `rcv` executes with non-zero value, return `last_sound`
2. Print the result to stdout
3. Handle edge case where program terminates without rcv:
   - If the main loop exits without returning a value, check if `last_sound` is None
   - Print a warning message if no sound was ever played
   - Return None or raise an error to indicate invalid program behavior

## Error Handling Considerations

Since this is a script for a specific input (not production code):
- Assume input is well-formed
- Don't need extensive validation
- Can assume rcv will be called with non-zero eventually
- Optional: Add a max iterations counter (e.g., 1,000,000) during development to detect infinite loops

## Code Structure

```python
from collections import defaultdict

def get_value(operand, registers):
    """Resolve operand to integer value.

    Args:
        operand: Either a register name or a literal integer string
        registers: Dictionary of register values

    Returns:
        Integer value of the operand
    """
    try:
        return int(operand)
    except ValueError:
        return registers[operand]

def solve(input_file='input.md'):
    """Execute the Duet assembly program and return the recovered frequency.

    Args:
        input_file: Path to the input file (default: 'input.md')

    Returns:
        The frequency of the last sound played when rcv executes with non-zero value
    """
    # Step 1: Parse input
    instructions = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                instructions.append(line.split())

    # Step 2: Initialize state
    registers = defaultdict(int)
    last_sound = None
    pc = 0

    # Step 5: Execute (with optional safety limit)
    # max_iterations = 1_000_000  # Optional: uncomment for debugging
    # iterations = 0

    while 0 <= pc < len(instructions):
        # Optional infinite loop protection (uncomment for debugging)
        # iterations += 1
        # if iterations > max_iterations:
        #     raise RuntimeError(f"Exceeded max iterations: {max_iterations}")

        instruction = instructions[pc]
        op = instruction[0]

        if op == "snd":
            last_sound = get_value(instruction[1], registers)
            pc += 1
        elif op == "set":
            registers[instruction[1]] = get_value(instruction[2], registers)
            pc += 1
        elif op == "add":
            registers[instruction[1]] += get_value(instruction[2], registers)
            pc += 1
        elif op == "mul":
            registers[instruction[1]] *= get_value(instruction[2], registers)
            pc += 1
        elif op == "mod":
            registers[instruction[1]] %= get_value(instruction[2], registers)
            pc += 1
        elif op == "rcv":
            if get_value(instruction[1], registers) != 0:
                return last_sound
            pc += 1
        elif op == "jgz":
            if get_value(instruction[1], registers) > 0:
                pc += get_value(instruction[2], registers)
            else:
                pc += 1

    # Program terminated without rcv returning a value
    if last_sound is None:
        print("WARNING: Program terminated without playing any sound")
    return None

def solve_with_string(input_str):
    """Execute Duet program from a string (for testing).

    Args:
        input_str: The program as a multi-line string

    Returns:
        The recovered frequency value
    """
    # Parse instructions from string
    instructions = []
    for line in input_str.strip().split('\n'):
        line = line.strip()
        if line:
            instructions.append(line.split())

    # Initialize state
    registers = defaultdict(int)
    last_sound = None
    pc = 0

    # Execute
    while 0 <= pc < len(instructions):
        instruction = instructions[pc]
        op = instruction[0]

        if op == "snd":
            last_sound = get_value(instruction[1], registers)
            pc += 1
        elif op == "set":
            registers[instruction[1]] = get_value(instruction[2], registers)
            pc += 1
        elif op == "add":
            registers[instruction[1]] += get_value(instruction[2], registers)
            pc += 1
        elif op == "mul":
            registers[instruction[1]] *= get_value(instruction[2], registers)
            pc += 1
        elif op == "mod":
            registers[instruction[1]] %= get_value(instruction[2], registers)
            pc += 1
        elif op == "rcv":
            if get_value(instruction[1], registers) != 0:
                return last_sound
            pc += 1
        elif op == "jgz":
            if get_value(instruction[1], registers) > 0:
                pc += get_value(instruction[2], registers)
            else:
                pc += 1

    return None

if __name__ == "__main__":
    result = solve()
    if result is not None:
        print(result)
    else:
        print("ERROR: No result obtained")
```

## Performance Analysis

### Time Complexity
- Parsing: O(n) where n = number of instructions (42)
- Execution: O(k) where k = number of instructions executed
  - Looking at the input: loops are bounded by counters
  - Worst case: several thousand iterations
  - Expected runtime: < 1 second

### Space Complexity
- O(n) for storing instructions (42 instructions)
- O(r) for registers (5 unique registers: i, a, p, b, f)
- Total: O(n) which is negligible for this input size

## Edge Cases to Handle in Implementation
1. Negative offsets in jumps (jumping backwards)
2. Jump offset can be a register value, not just literal
3. First operand of `jgz` can also be a literal (e.g., `jgz 1 3`)
4. `snd` operand can be register or literal
5. Program counter going out of bounds (termination)
