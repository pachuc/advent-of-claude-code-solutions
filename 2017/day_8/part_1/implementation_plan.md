# Implementation Plan: Register Instruction Processor

## Updates Based on Critique

This plan has been updated to address the following improvements:
- Added `parse_instruction_line()` helper function for better testability
- Added error handling for file operations (FileNotFoundError)
- Added optional verbose mode for debugging and manual verification
- Documented assumptions about input format
- Clarified edge case handling (registers default to 0)
- Updated code structure to reflect all functions

## Problem Analysis

We need to process CPU register instructions that conditionally modify register values based on comparison operations. The goal is to find the largest value in any register after all instructions complete.

### Input Characteristics
- 1000 instructions in the input
- Each instruction has: target register, operation (inc/dec), amount, condition register, comparator, and condition value
- All registers start at 0
- Registers are created on-the-fly when referenced

### Algorithm Complexity Considerations
- **Time Complexity**: O(n) where n is the number of instructions - each instruction is processed once
- **Space Complexity**: O(r) where r is the number of unique registers (likely much smaller than n)
- Input size: 1000 instructions is small, so performance is not a concern
- Simple linear processing is optimal - no need for complex optimizations

## Implementation Steps

### Step 1: Parse Input
**Task**: Read and parse the input file containing instructions

**Implementation**:
```python
def parse_instruction_line(line):
    """Parse a single instruction line and return instruction dict

    This helper function is separated for testability.
    """
    parts = line.strip().split()
    # Input is assumed to be well-formed (7 space-separated parts)
    return {
        'target_reg': parts[0],
        'operation': parts[1],
        'amount': int(parts[2]),
        'cond_reg': parts[4],
        'comparator': parts[5],
        'cond_val': int(parts[6])
    }

def parse_input(filename):
    """Parse input file and return list of instruction tuples"""
    instructions = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            instructions.append(parse_instruction_line(line))
    return instructions
```

**Rationale**:
- Separated `parse_instruction_line()` for easier unit testing
- Simple string splitting works because format is consistent
- Store as dictionary for clarity (could use tuple for micro-optimization, but readability is more important)
- Skip empty lines for robustness
- Input is assumed to be well-formed (appropriate for AoC problems)

### Step 2: Define Comparison Operations
**Task**: Create a mapping of comparator strings to actual comparison functions

**Implementation**:
```python
def get_comparator(operator):
    """Return comparison function for given operator string"""
    comparators = {
        '>': lambda a, b: a > b,
        '<': lambda a, b: a < b,
        '>=': lambda a, b: a >= b,
        '<=': lambda a, b: a <= b,
        '==': lambda a, b: a == b,
        '!=': lambda a, b: a != b
    }
    return comparators[operator]
```

**Rationale**:
- Using a dictionary of lambda functions is clean and efficient
- Alternative: use `eval()` but that's unsafe and slower
- Alternative: long if-elif chain but less maintainable

### Step 3: Process Instructions
**Task**: Execute each instruction sequentially, maintaining register state

**Implementation**:
```python
def process_instructions(instructions, verbose=False):
    """Execute all instructions and return final register state

    Args:
        instructions: List of instruction dictionaries
        verbose: If True, print register state after each modification (for debugging)

    Returns:
        Dictionary mapping register names to their final values
    """
    registers = {}  # defaultdict could work but explicit is clearer

    for i, instr in enumerate(instructions):
        # Get current value of condition register (0 if not exists)
        cond_reg_value = registers.get(instr['cond_reg'], 0)

        # Evaluate condition
        comparator = get_comparator(instr['comparator'])
        if comparator(cond_reg_value, instr['cond_val']):
            # Condition is true, apply operation
            current_value = registers.get(instr['target_reg'], 0)

            if instr['operation'] == 'inc':
                registers[instr['target_reg']] = current_value + instr['amount']
            elif instr['operation'] == 'dec':
                registers[instr['target_reg']] = current_value - instr['amount']

            if verbose:
                print(f"After instruction {i+1}: {instr['target_reg']} = {registers[instr['target_reg']]}")

    return registers
```

**Rationale**:
- Using `dict.get(key, 0)` cleanly handles non-existent registers
- Alternative: use `collections.defaultdict(int)` - slightly cleaner but less explicit
- Direct if-elif for operations is simple and readable
- Only update register if condition is true
- Optional verbose mode helps with debugging and manual verification

### Step 4: Find Maximum Value
**Task**: Determine the largest value across all registers

**Implementation**:
```python
def find_max_register_value(registers):
    """Return the maximum value in any register"""
    if not registers:
        return 0  # Edge case: no registers modified
    return max(registers.values())
```

**Rationale**:
- Built-in `max()` is optimal for this task
- Handle edge case of empty registers (though unlikely given input)

### Step 5: Main Execution Flow
**Task**: Coordinate all steps and output the result

**Implementation**:
```python
def main():
    """Main execution function"""
    try:
        # Parse input
        instructions = parse_input('input.md')
    except FileNotFoundError:
        print("Error: input.md not found")
        return
    except Exception as e:
        print(f"Error reading input: {e}")
        return

    # Process all instructions (set verbose=True for debugging)
    registers = process_instructions(instructions, verbose=False)

    # Find and print maximum value
    max_value = find_max_register_value(registers)
    print(max_value)

if __name__ == '__main__':
    main()
```

**Rationale**:
- Clear separation of concerns
- Basic error handling for missing or malformed input file
- Easy to test individual components
- Standard Python pattern with `if __name__ == '__main__'`
- Verbose mode can be enabled for debugging

## Code Structure

```
solution.py
├── parse_instruction_line(line) -> instruction dict
├── parse_input(filename) -> list of instruction dicts
├── get_comparator(operator) -> comparison function
├── process_instructions(instructions, verbose=False) -> dict of registers
├── find_max_register_value(registers) -> int
└── main() -> None (prints result)
```

## Edge Cases Handled

1. **Empty registers**: Return 0 if no registers exist (all registers implicitly start at 0)
2. **Negative amounts**: Work naturally with inc/dec operations
   - `inc -20` means add -20 (decrease by 20)
   - `dec -10` means subtract -10 (increase by 10)
3. **Non-existent registers in conditions**: Default to 0
4. **Empty lines in input**: Skip during parsing
5. **All conditions false**: Some registers may never be modified
6. **Missing input file**: Caught by try-except, clear error message

## Assumptions

- Input file is well-formed (7 space-separated parts per line)
- Comparators are valid (one of: >, <, >=, <=, ==, !=)
- Operations are valid (inc or dec)
- Register names are alphanumeric strings
- Amounts and condition values are valid integers

## Performance Characteristics

- **Time Complexity**: O(n) where n = number of instructions
  - Single pass through all instructions
  - Constant time operations per instruction
- **Space Complexity**: O(r) where r = number of unique registers
  - Dictionary to store register values
  - Typically r << n
- **Expected runtime**: < 1ms for 1000 instructions

## Alternative Approaches Considered

1. **Using `collections.defaultdict(int)`**: Slightly cleaner but less explicit
2. **Using `operator` module**: More verbose without benefit for this size
3. **Regex parsing**: Overkill for simple space-separated format
4. **Single-pass max tracking**: Could track max during processing, but separate function is clearer

## Final Notes

- Code prioritizes readability over micro-optimizations
- No external dependencies beyond Python standard library
- Solution is deterministic and straightforward
- All operations are idempotent (safe to re-run)
