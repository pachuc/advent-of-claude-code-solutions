# Implementation Plan: Intcode Computer Simulator

## Problem Summary

Implement an Intcode computer simulator that:
1. Parses a comma-separated list of integers as memory
2. Applies a pre-processing step (set position 1 to 12, position 2 to 2)
3. Executes instructions based on opcodes (1=ADD, 2=MULTIPLY, 99=HALT)
4. Returns the value at position 0 after halting

## Algorithm Analysis

### Complexity Considerations
- **Input Size**: The input contains ~129 integers, which is relatively small
- **Time Complexity**: O(n) where n is the number of instructions executed
  - Each instruction is processed in O(1) time (constant lookup and arithmetic)
  - The program will halt after a finite number of instructions
- **Space Complexity**: O(m) where m is the length of the program
  - We only need to store the memory array in place
  - No additional data structures needed

Given the small input size, a straightforward iterative approach is optimal. No sophisticated algorithms are needed.

## Implementation Steps

### Step 1: Parse Input
- Read the input string from `input.md`
- Split by comma and convert each element to an integer
- Store in a Python list (mutable, supports in-place modification)

```python
def parse_input(input_str):
    return [int(x) for x in input_str.strip().split(',')]
```

### Step 2: Apply Pre-processing
- Before execution, modify the memory:
  - `memory[1] = 12`
  - `memory[2] = 2`

```python
def preprocess(memory):
    memory[1] = 12
    memory[2] = 2
```

### Step 3: Implement Instruction Execution

#### Main Execution Loop
- Initialize instruction pointer (ip) to 0
- Loop while opcode at current position is not 99:
  1. Read opcode at `memory[ip]`
  2. Based on opcode:
     - **Opcode 1 (ADD)**: `memory[memory[ip+3]] = memory[memory[ip+1]] + memory[memory[ip+2]]`
     - **Opcode 2 (MULTIPLY)**: `memory[memory[ip+3]] = memory[memory[ip+1]] * memory[memory[ip+2]]`
     - **Opcode 99**: Halt execution
  3. Advance ip by 4

```python
def execute(memory):
    ip = 0  # instruction pointer

    while True:
        opcode = memory[ip]

        if opcode == 99:
            break
        elif opcode == 1:
            # ADD
            param1 = memory[ip + 1]
            param2 = memory[ip + 2]
            param3 = memory[ip + 3]
            memory[param3] = memory[param1] + memory[param2]
        elif opcode == 2:
            # MULTIPLY
            param1 = memory[ip + 1]
            param2 = memory[ip + 2]
            param3 = memory[ip + 3]
            memory[param3] = memory[param1] * memory[param2]

        ip += 4

    return memory[0]
```

### Step 4: Main Function
- Read input from file
- Parse into memory array
- Apply pre-processing
- Execute and return result

```python
def main():
    with open('input.md', 'r') as f:
        input_str = f.read()

    memory = parse_input(input_str)
    preprocess(memory)
    result = execute(memory)

    print(result)
```

## Complete Code Structure

```python
def parse_input(input_str):
    """Parse comma-separated integers into a list."""
    return [int(x) for x in input_str.strip().split(',')]

def preprocess(memory):
    """Apply the 1202 alarm state (position 1=12, position 2=2)."""
    memory[1] = 12
    memory[2] = 2

def execute(memory):
    """Execute the Intcode program and return value at position 0."""
    ip = 0

    while True:
        opcode = memory[ip]

        if opcode == 99:
            break
        elif opcode == 1:
            param1, param2, param3 = memory[ip+1], memory[ip+2], memory[ip+3]
            memory[param3] = memory[param1] + memory[param2]
        elif opcode == 2:
            param1, param2, param3 = memory[ip+1], memory[ip+2], memory[ip+3]
            memory[param3] = memory[param1] * memory[param2]

        ip += 4

    return memory[0]

def main():
    with open('input.md', 'r') as f:
        input_str = f.read()

    memory = parse_input(input_str)
    preprocess(memory)
    result = execute(memory)

    print(result)

if __name__ == '__main__':
    main()
```

## Key Design Decisions

1. **Mutable List for Memory**: Python lists allow efficient O(1) random access and in-place modification, perfect for this use case.

2. **Single Pass Execution**: No need to pre-scan the program; we execute instructions sequentially until HALT.

3. **No Error Handling for Invalid Opcodes**: The problem guarantees valid input, so we don't need to handle unknown opcodes.

4. **Direct Position Access**: Parameters are used as direct indices into memory (position mode), as specified in the problem.

## Potential Edge Cases to Consider

1. **Self-modifying code**: The program can modify its own instructions (memory positions that contain opcodes)
2. **Writing to position 0**: The result we return might be written multiple times during execution
3. **Large integer values**: Python handles arbitrary precision integers natively, so no overflow concerns
4. **Empty or minimal programs**: Programs like `99` would halt immediately with initial value at position 0

## File Organization

- `solution.py` - Main solution script
- `input.md` - Input data (already provided)
- `problem.md` - Problem description (already provided)
