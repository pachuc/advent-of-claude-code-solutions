# Implementation Plan: Instruction Pointer Simulation

## Problem Analysis

This is a CPU simulation problem where we need to:
1. Execute assembly-like instructions on a 6-register CPU
2. Handle instruction pointer (IP) binding to one of the registers
3. Support flow control through jumps (modifying the IP via the bound register)
4. Determine when the program halts and return the final value in register 0

### Algorithm Complexity Considerations

**Time Complexity**: The runtime depends on the program logic. Looking at the input:
- The program has 36 instructions (lines 2-37 in input.md)
- IP is bound to register 3
- There are jump instructions that can create loops
- Without analyzing the specific logic, we must assume potentially O(n) to O(n²) or even higher iterations depending on loop structures

**Space Complexity**: O(1) - we only need 6 registers and the instruction list

**Efficiency Concerns**:
- The input program may run for many iterations (potentially millions)
- We need efficient opcode execution (no string comparisons in the main loop)
- Simple array/list operations for registers
- For this problem, a straightforward simulation should suffice unless the program runs indefinitely

## Step-by-Step Implementation Plan

### Step 1: Define Data Structures

**1.1 Register State**
- Use a list of 6 integers: `registers = [0, 0, 0, 0, 0, 0]`
- All registers start at 0

**1.2 Instruction Representation**
- Parse each instruction line into a tuple: `(opcode, A, B, C)`
- Store all instructions in a list for indexed access

**1.3 Instruction Pointer Binding**
- Store the bound register number from the `#ip N` declaration
- Use this throughout execution to sync IP with the register

### Step 2: Implement Opcode Functions

**2.1 Create Opcode Dictionary**
- Map opcode names (strings) to their implementation functions
- Each function takes: `(registers, A, B, C)` and modifies registers in-place

**2.2 Implement Each Opcode Category**

*Addition Opcodes:*
- `addr(regs, A, B, C)`: `regs[C] = regs[A] + regs[B]`
- `addi(regs, A, B, C)`: `regs[C] = regs[A] + B`

*Multiplication Opcodes:*
- `mulr(regs, A, B, C)`: `regs[C] = regs[A] * regs[B]`
- `muli(regs, A, B, C)`: `regs[C] = regs[A] * B`

*Bitwise AND Opcodes:*
- `banr(regs, A, B, C)`: `regs[C] = regs[A] & regs[B]`
- `bani(regs, A, B, C)`: `regs[C] = regs[A] & B`

*Bitwise OR Opcodes:*
- `borr(regs, A, B, C)`: `regs[C] = regs[A] | regs[B]`
- `bori(regs, A, B, C)`: `regs[C] = regs[A] | B`

*Assignment Opcodes:*
- `setr(regs, A, B, C)`: `regs[C] = regs[A]` (parameter B is unused/ignored)
- `seti(regs, A, B, C)`: `regs[C] = A` (parameter B is unused/ignored)

*Comparison Opcodes (greater-than):*
- `gtir(regs, A, B, C)`: `regs[C] = 1 if A > regs[B] else 0`
- `gtri(regs, A, B, C)`: `regs[C] = 1 if regs[A] > B else 0`
- `gtrr(regs, A, B, C)`: `regs[C] = 1 if regs[A] > regs[B] else 0`

*Equality Opcodes:*
- `eqir(regs, A, B, C)`: `regs[C] = 1 if A == regs[B] else 0`
- `eqri(regs, A, B, C)`: `regs[C] = 1 if regs[A] == B else 0`
- `eqrr(regs, A, B, C)`: `regs[C] = 1 if regs[A] == regs[B] else 0`

**Note**: For a script solution, we can assume register indices are valid (0-5). Optional validation can be added but is not strictly necessary.

### Step 3: Parse Input

**3.1 Parse IP Binding Declaration**
- Read the first line
- Extract the register number from `#ip N` format using string operations or regex
- Store as `ip_register`
- **Validation**: Ensure `0 <= ip_register <= 5` (raise error if invalid)

**3.2 Parse Instructions**
- Read remaining lines
- For each line:
  - Strip whitespace using `.strip()`
  - Skip empty lines
  - Split by whitespace using `.split()`
  - Create tuple: `(opcode_string, int(A), int(B), int(C))`
  - Store in `instructions` list
- **Validation**: Verify opcode names are valid (optional but recommended)

### Step 4: Implement Execution Loop

**4.1 Initialize State**
```python
registers = [0, 0, 0, 0, 0, 0]
ip = 0
ip_register = <parsed from input>
instructions = <parsed from input>
```

**4.2 Main Execution Loop**
```python
iteration_count = 0
max_iterations = 10_000_000  # Safety limit to detect infinite loops

while True:
    # Step 1: Check halt condition BEFORE execution
    if ip < 0 or ip >= len(instructions):
        break

    # Step 2: Safety check for infinite loops
    iteration_count += 1
    if iteration_count > max_iterations:
        raise RuntimeError(f"Exceeded {max_iterations} iterations - possible infinite loop")

    # Step 3: Write IP to bound register
    registers[ip_register] = ip

    # Step 4: Fetch instruction
    opcode, A, B, C = instructions[ip]

    # Step 5: Execute instruction
    opcode_functions[opcode](registers, A, B, C)

    # Step 6: Read IP from bound register
    ip = registers[ip_register]

    # Step 7: Increment IP
    ip += 1
```

**4.3 Halt Condition**
- Loop exits when `ip < 0` or `ip >= len(instructions)`
- Check happens at the START of each iteration, before writing IP to register
- This ensures we don't execute instructions outside the program bounds

### Step 5: Return Result

**5.1 Extract Final Value**
- After the loop terminates, return `registers[0]`

**5.2 Output Format**
- Print only the integer value to stdout: `print(registers[0])`
- This outputs the number followed by a newline (Python default)
- No additional text or formatting needed

## Code Structure

```python
def parse_input(input_text):
    """Parse input and return ip_register and instructions list"""
    pass

def create_opcode_functions():
    """Return dictionary mapping opcode names to functions"""
    pass

def execute_program(ip_register, instructions):
    """Execute the program and return final value in register 0"""
    pass

def main():
    """Main entry point"""
    # Read input
    # Parse input
    # Execute program
    # Print result
    pass
```

## Optimization Considerations

1. **Opcode Dispatch**: Use dictionary lookup instead of if/elif chains
2. **Register Access**: Use list indexing (already O(1))
3. **Infinite Loop Detection**:
   - Implement a simple iteration counter with max limit (10 million iterations)
   - This prevents hanging on potentially infinite loops
   - More sophisticated state tracking (IP + register values) is not needed for this problem
   - If limit is hit, raise an error with a clear message

## Edge Cases to Handle

1. **Empty program**: Instructions list is empty → IP starts at 0, immediately out of bounds, return registers[0] = 0
2. **IP register modification**: The bound register can be modified by instructions, affecting control flow (this is intentional for jumps)
3. **Negative IP values**: Program halts if IP becomes negative (checked at loop start)
4. **Large IP values**: Program halts if IP exceeds instruction count (checked at loop start)
5. **Malformed input**: Missing `#ip` line or invalid format should raise clear error
6. **Invalid register references**: For a script solution, assume input is valid; optional validation can check 0 <= register <= 5

## Expected Implementation Time

- Opcode functions: ~50 lines
- Parsing: ~20 lines
- Execution loop: ~15 lines
- Main/utilities: ~20 lines
- **Total**: ~100-120 lines of Python code
