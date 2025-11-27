# Implementation Plan: Chronal Classification - Part 1

## Overview
We need to count how many sample observations behave like three or more different opcodes. Each sample has a "Before" state, an instruction with parameters, and an "After" state. We'll test each of the 16 opcodes to see which ones could produce the observed transformation.

## Algorithm Efficiency Analysis

**Input Size**: ~4000 lines, which means ~1000 samples (4 lines per sample)
**Operations per sample**: Test 16 opcodes, each requiring constant-time operations
**Overall Complexity**: O(n) where n is the number of samples (16 opcodes is a constant)
**Expected Runtime**: Very fast - simple arithmetic and comparisons on small register arrays

This problem doesn't require complex optimization since:
- Number of opcodes is fixed (16)
- Register count is fixed (4)
- Each opcode simulation is O(1)
- Total: O(samples × 16 × 1) = O(samples) which is linear and efficient

## Step-by-Step Implementation Plan

### 1. Input Parsing
**File**: `solution.py`

**Components**:
- Create a function `parse_input(filename)` that:
  - Reads the entire input file
  - Splits content into samples (each sample is 3 lines + blank line)
  - **Important**: Samples section ends when encountering two consecutive blank lines
  - After the double blank line, the test program begins (which we ignore for Part 1)
  - For each sample:
    - Extract "Before" register state using regex: `Before:\s*\[(\d+), (\d+), (\d+), (\d+)\]`
    - Extract instruction values: `opcode A B C`
    - Extract "After" register state using regex: `After:\s*\[(\d+), (\d+), (\d+), (\d+)\]`
  - Return list of tuples: `(before_registers, instruction, after_registers)`

**Data Structures**:
- `before_registers`: tuple of 4 integers
- `instruction`: tuple of 4 integers (opcode, A, B, C)
- `after_registers`: tuple of 4 integers

**Parsing Strategy**:
```python
def parse_input(filename):
    with open(filename) as f:
        lines = f.readlines()

    samples = []
    i = 0

    # Parse until we hit two consecutive blank lines
    while i < len(lines):
        line = lines[i].strip()

        # Check for double blank line (end of samples section)
        if i + 1 < len(lines) and not line and not lines[i + 1].strip():
            break

        # Parse a sample (3 lines + 1 blank)
        if line.startswith('Before:'):
            before = parse_registers(line)
            instruction = parse_instruction(lines[i + 1])
            after = parse_registers(lines[i + 2])
            samples.append((before, instruction, after))
            i += 4  # Skip to next sample (3 lines + blank)
        else:
            i += 1

    return samples
```

### 2. Opcode Simulation Functions
**File**: `solution.py`

**Approach**: Create individual functions for each of the 16 opcodes. Each function:
- Takes parameters: `registers` (list of 4 ints), `A`, `B`, `C`
- Returns a new list representing the register state after execution
- Uses list copying to avoid mutating the input

**Implementation Details**:

```python
def execute_opcode(opcode_name, registers, A, B, C):
    """Execute a specific opcode and return new register state"""
    result = registers.copy()

    # Addition operations
    if opcode_name == 'addr':
        result[C] = registers[A] + registers[B]
    elif opcode_name == 'addi':
        result[C] = registers[A] + B

    # Multiplication operations
    elif opcode_name == 'mulr':
        result[C] = registers[A] * registers[B]
    elif opcode_name == 'muli':
        result[C] = registers[A] * B

    # Bitwise AND operations
    elif opcode_name == 'banr':
        result[C] = registers[A] & registers[B]
    elif opcode_name == 'bani':
        result[C] = registers[A] & B

    # Bitwise OR operations
    elif opcode_name == 'borr':
        result[C] = registers[A] | registers[B]
    elif opcode_name == 'bori':
        result[C] = registers[A] | B

    # Assignment operations
    elif opcode_name == 'setr':
        result[C] = registers[A]
    elif opcode_name == 'seti':
        result[C] = A

    # Greater-than testing
    elif opcode_name == 'gtir':
        result[C] = 1 if A > registers[B] else 0
    elif opcode_name == 'gtri':
        result[C] = 1 if registers[A] > B else 0
    elif opcode_name == 'gtrr':
        result[C] = 1 if registers[A] > registers[B] else 0

    # Equality testing
    elif opcode_name == 'eqir':
        result[C] = 1 if A == registers[B] else 0
    elif opcode_name == 'eqri':
        result[C] = 1 if registers[A] == B else 0
    elif opcode_name == 'eqrr':
        result[C] = 1 if registers[A] == registers[B] else 0

    return result
```

**Opcode List**: Store all 16 opcode names in a list for iteration:
```python
ALL_OPCODES = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani',
               'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri',
               'gtrr', 'eqir', 'eqri', 'eqrr']
```

### 3. Sample Analysis Function
**File**: `solution.py`

**Function**: `count_matching_opcodes(before, instruction, after)`
- Parameters:
  - `before`: list of 4 integers (register state before)
  - `instruction`: tuple (opcode_num, A, B, C) - note: opcode_num is ignored
  - `after`: list of 4 integers (register state after)
- Process:
  - Extract A, B, C from instruction (ignore opcode number)
  - Initialize counter to 0
  - For each of the 16 opcode names:
    - Execute the opcode with parameters A, B, C on the before state
    - Compare result with after state
    - If they match exactly, increment counter
  - Return counter

**Matching Logic**:
```python
result = execute_opcode(opcode_name, before, A, B, C)
if result == after:
    matches += 1
```

### 4. Main Solution Function
**File**: `solution.py`

**Function**: `solve(filename)`
- Parse input to get all samples
- Initialize counter for samples with 3+ matches
- For each sample:
  - Count how many opcodes match
  - If count >= 3, increment the result counter
- Return the final count

**Structure**:
```python
def solve(filename):
    samples = parse_input(filename)
    count = 0

    for before, instruction, after in samples:
        matching_opcodes = count_matching_opcodes(before, instruction, after)
        if matching_opcodes >= 3:
            count += 1

    return count
```

### 5. Main Entry Point
**File**: `solution.py`

**Implementation**:
```python
if __name__ == "__main__":
    result = solve("input.md")
    print(result)
```

## Key Implementation Considerations

### Edge Cases to Handle:
1. **Register bounds**: For register operations, A and B are used as indices (0-3) when the opcode ends in 'r'. C is always a register index (0-3). For immediate opcodes (ending in 'i'), A or B are used as literal values and can be any integer.
   - The problem guarantees valid inputs, so no validation needed
2. **Division by zero**: Not applicable (no division operations)
3. **Immediate vs Register**: Carefully distinguish 'i' (immediate) vs 'r' (register) opcodes
4. **Ignored parameters**: setr ignores B, seti ignores B
5. **Input parsing boundary**: Samples end at double blank line, test program follows (ignored for Part 1)

### Correctness Checks:
1. Ensure register copying prevents mutation
2. Verify all 16 opcodes are implemented
3. Test with the provided example first
4. Double-check comparison operations (>, ==) return 0 or 1, not boolean

### Optimization Notes:
- No optimization needed - algorithm is already O(n)
- Count all matches for accuracy and potential debugging purposes

### Helper Function for Debugging (Optional):
For debugging purposes, it may be helpful to add:
```python
def find_matching_opcodes(before, instruction, after):
    """Returns list of opcode names that match the sample"""
    _, A, B, C = instruction
    matching = []
    for opcode_name in ALL_OPCODES:
        result = execute_opcode(opcode_name, before, A, B, C)
        if result == after:
            matching.append(opcode_name)
    return matching
```

## File Structure
```
/app/agent_workspace/2018/day_16/part_1/
├── solution.py          # Main solution file
├── input.md             # Input data
├── problem.md           # Problem description
├── implementation_plan.md
└── test_plan.md
```

## Testing Hook
Before considering implementation complete:
1. Test with the example from problem.md
2. Verify output format is a single integer
3. Run against actual input.md
