# Implementation Plan: Clock Signal Generator

## Overview
We need to implement an assembunny interpreter and find the lowest positive integer that, when placed in register `a`, causes the program to output an alternating clock signal pattern `0, 1, 0, 1, 0, 1...` indefinitely.

## Algorithm Approach

### Core Strategy
1. Build a simple assembunny interpreter with inline instruction execution
2. Check for the alternating pattern in real-time as outputs are generated (early termination)
3. Iterate through positive integers starting from 1, testing each until we find the correct pattern
4. Verify a sufficient number of outputs (50) to confirm the pattern repeats

### Time Complexity Considerations
- The program has a loop structure that will execute many iterations per candidate
- With early termination, invalid candidates fail immediately on first wrong output
- Expected answer is likely in range 1-1000 based on program structure (d = a + 2555)
- Total runtime: < 5 seconds expected

### Space Complexity
- O(1) for the interpreter (4 registers + program counter + output counter)
- O(n) for storing the program instructions (n = 30 lines)
- No need to store all outputs, just validate as they're generated

## Step-by-Step Implementation

### Step 1: Parse Input Instructions
```python
def parse_input(filename):
    """
    Read and parse the assembunny program.
    Returns list of instruction components: [['cpy', 'a', 'd'], ['inc', 'x'], ...]
    """
    instructions = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                instructions.append(line.split())
    return instructions
```

### Step 2: Implement Value Resolution Helper
```python
def get_value(operand, registers):
    """
    Returns numeric value of an operand.
    If operand is a register name ('a'-'d'), return register value.
    Otherwise, convert to integer and return.
    """
    if operand in registers:
        return registers[operand]
    return int(operand)
```

### Step 3: Build the Assembunny Interpreter with Early Termination

```python
def run_program(initial_a, instructions, max_outputs=50):
    """
    Execute assembunny program with real-time pattern validation.
    Returns True if produces alternating 0,1,0,1... pattern for max_outputs.
    Returns False immediately on first pattern violation.

    PC Update Rules:
    - Normal instructions: pc += 1
    - JNZ when condition true: pc += offset (can be negative for backwards jumps)
    - JNZ when condition false: pc += 1
    """
    # Initialize registers
    registers = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    pc = 0
    output_count = 0

    # Execute until we have enough outputs or program ends
    while 0 <= pc < len(instructions) and output_count < max_outputs:
        inst = instructions[pc]
        cmd = inst[0]

        # Execute instruction with inline logic
        if cmd == 'cpy':
            x, y = inst[1], inst[2]
            if y in registers:  # Only copy to valid registers
                registers[y] = get_value(x, registers)
            pc += 1

        elif cmd == 'inc':
            registers[inst[1]] += 1
            pc += 1

        elif cmd == 'dec':
            registers[inst[1]] -= 1
            pc += 1

        elif cmd == 'jnz':
            x = get_value(inst[1], registers)
            if x != 0:
                offset = get_value(inst[2], registers)
                pc += offset
            else:
                pc += 1

        elif cmd == 'out':
            value = get_value(inst[1], registers)
            expected = output_count % 2  # Expected: 0, 1, 0, 1, ...

            # Early termination: fail immediately if pattern breaks
            if value != expected:
                return False

            output_count += 1
            pc += 1

    # Success: generated max_outputs with perfect alternating pattern
    return output_count >= max_outputs
```

### Step 4: Main Search Algorithm

```python
def find_clock_signal_input(instructions):
    """
    Find the lowest positive integer that produces the clock signal pattern.
    Uses early termination - invalid candidates fail fast.
    """
    verification_length = 50  # Check 50 outputs to confirm pattern

    for candidate in range(1, 10000):  # Conservative upper bound
        if run_program(candidate, instructions, verification_length):
            return candidate

    raise Exception("No solution found in range 1-10000")
```

### Step 5: Main Execution Flow

```python
def main():
    # Parse input
    instructions = parse_input('input.md')

    # Find and print the answer
    answer = find_clock_signal_input(instructions)
    print(answer)

if __name__ == "__main__":
    main()
```

## Debug Mode (Optional)

For troubleshooting, add a debug flag:

```python
def run_program(initial_a, instructions, max_outputs=50, debug=False):
    # ... existing code ...

    if debug:
        print(f"Testing a={initial_a}")
        # Inside loop, after 'out' instruction:
        print(f"  Output {output_count}: {value} (expected {expected})")
```

## Key Implementation Details

### PC (Program Counter) Management
- **Normal instructions** (cpy, inc, dec, out): `pc += 1`
- **JNZ when x != 0**: `pc += offset` (offset can be negative for backwards loops)
- **JNZ when x == 0**: `pc += 1` (no jump)
- The offset in JNZ is relative to the current position

### Input Parsing Notes
- The input file may have trailing newlines - `strip()` handles this
- Each line splits into instruction components: `['cpy', 'a', 'd']`
- No special comment handling needed for this input

## Edge Cases to Handle
1. **Infinite loops**: Max outputs limit (50) prevents hanging
2. **Register vs integer operands**: `get_value()` handles both
3. **PC bounds**: Check `0 <= pc < len(instructions)` in main loop
4. **Invalid register in cpy**: Check `if y in registers` before assignment
5. **No solution found**: Upper bound of 10000 prevents infinite search

## Complete Code Structure
```
solution.py          # ~80 lines total:
                     # - parse_input(): ~8 lines
                     # - get_value(): ~4 lines
                     # - run_program(): ~40 lines
                     # - find_clock_signal_input(): ~6 lines
                     # - main(): ~4 lines
input.md            # Input program (provided)
```

## Expected Runtime and Efficiency
- **Early termination**: Invalid candidates fail on first wrong output (usually immediate)
- **Verification length**: 50 outputs is sufficient to confirm pattern
- **Search space**: Answer likely in range 1-1000
- **Expected runtime**: < 5 seconds
- **Worst case**: Even with answer at 10000, should complete in < 30 seconds
