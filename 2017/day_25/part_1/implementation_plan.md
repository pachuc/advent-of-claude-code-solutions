# Implementation Plan: Turing Machine Simulator

## Problem Analysis

We need to simulate a Turing machine for **12,172,063 steps** with 6 states (A-F). The machine operates on an infinite tape of binary values, starting with all zeros.

### Key Considerations

1. **Performance**: With 12M+ steps, efficiency is critical
2. **Data Structure**: Need efficient tape representation that handles both positive and negative indices
3. **Parsing**: Must correctly parse state machine rules from input
4. **Memory**: Only store non-zero tape values to minimize memory usage

### Algorithm Complexity

- **Time Complexity**: O(n) where n = number of steps (unavoidable, must execute each step)
- **Space Complexity**: O(m) where m = number of cells written to (likely much less than n)
- **Critical optimization**: Use dictionary/hash map for tape to avoid array resizing

## Step-by-Step Implementation Plan

### Step 1: Input Parsing Module

**Objective**: Parse the input blueprint into usable data structures

**Approach**:
```python
# Parse initial state (extract from "Begin in state X.")
# Parse number of steps (extract from "Perform a diagnostic checksum after N steps.")
# Parse state definitions into nested dictionary structure
```

**Data Structure Design**:
```python
states = {
    'A': {
        0: {'write': 1, 'move': 1, 'next_state': 'B'},   # move: 1 for right, -1 for left
        1: {'write': 0, 'move': -1, 'next_state': 'C'}
    },
    'B': { ... },
    ...
}
```

**Implementation Details**:
- Use regex or string parsing to extract state names
- Use regex to extract numbers (0/1 for values, steps count)
- Use keywords "right" and "left" to determine move direction (+1 or -1)
- Store all state transitions in a nested dictionary for O(1) lookup

**Edge Cases**:
- Handle both uppercase and lowercase state names
- Handle variations in spacing/formatting
- Ensure all required states are parsed

### Step 2: Tape Data Structure

**Objective**: Implement an efficient tape that supports infinite extension in both directions

**Approach**: Use a dictionary (defaultdict) to represent the tape
```python
from collections import defaultdict
tape = defaultdict(int)  # Defaults to 0 for unset positions
```

**Rationale**:
- Dictionary provides O(1) read/write access
- Only stores non-zero values, saving memory
- Naturally handles negative and positive indices
- Much more efficient than a list that needs resizing

**Alternative Considered**: List with dynamic resizing
- Rejected because: requires index offsetting, expensive resizing operations, wastes memory on zeros

### Step 3: Turing Machine Simulator Core

**Objective**: Implement the main simulation loop

**Algorithm**:
```python
def simulate_turing_machine(states, initial_state, num_steps):
    tape = defaultdict(int)
    cursor = 0
    current_state = initial_state

    for step in range(num_steps):
        # 1. Read current value
        current_value = tape[cursor]

        # 2. Get rule for current state and value
        rule = states[current_state][current_value]

        # 3. Write new value
        tape[cursor] = rule['write']

        # 4. Move cursor
        cursor += rule['move']

        # 5. Transition to next state
        current_state = rule['next_state']

    return tape
```

**Performance Optimizations**:
- Pre-compute state lookup dictionary (done in parsing) - O(1) rule lookups
- Use integer arithmetic for cursor movement (+1 or -1, no conditionals)
- Use dictionary (defaultdict) for tape instead of list - avoids resizing overhead
- Store move direction as integer to avoid string comparison in loop

**Why This Is Efficient**:
- Single loop with O(1) operations per iteration
- No nested loops or recursion
- Minimal memory allocation during execution (dictionary only grows as needed)
- Dictionary lookups are O(1) average case
- The bottleneck is simply the 12M+ iterations, which is unavoidable

### Step 4: Checksum Calculation

**Objective**: Count the number of 1s on the tape after simulation

**Approach**:
```python
def calculate_checksum(tape):
    return sum(tape.values())
    # This works because tape values are only 0 or 1
    # We could also use: sum(1 for value in tape.values() if value == 1)
```

**Rationale**:
- Since tape values are binary (0 or 1), summing all values counts the 1s
- O(m) complexity where m = number of cells written to
- Note: Even if we explicitly write 0 to positions, sum() still works correctly

**Memory Optimization (Optional)**:
To save memory by not storing zeros, we could modify the simulation:
```python
if rule['write'] == 1:
    tape[cursor] = 1
elif cursor in tape:
    del tape[cursor]  # Remove explicit 0s to save memory
```
This is optional since the tape likely won't accumulate many zeros.

### Step 5: Main Program Flow

**Objective**: Tie everything together

**Structure**:
```python
def main(input_file='input.md'):
    # 1. Read input file with basic error handling
    try:
        with open(input_file, 'r') as f:
            input_text = f.read()
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
        return None

    # 2. Parse input
    initial_state, num_steps, states = parse_input(input_text)

    # 3. Simulate
    tape = simulate_turing_machine(states, initial_state, num_steps)

    # 4. Calculate checksum
    checksum = calculate_checksum(tape)

    # 5. Output result
    print(checksum)
    return checksum

if __name__ == "__main__":
    main()
```

**Design Note**:
- `parse_input` accepts a string (not filename) for testability
- `main` accepts optional filename parameter to support testing with different inputs
- Basic error handling for missing files (keeps it simple for a script)
- Returns checksum for testing purposes

### Step 6: Parsing Implementation Details

**Regex Patterns Needed**:
```python
import re

# Extract initial state
initial_pattern = r"Begin in state ([A-Z])\."

# Extract number of steps
steps_pattern = r"after (\d+) steps"

# Extract state blocks
state_pattern = r"In state ([A-Z]):(.*?)(?=In state [A-Z]:|$)"

# Within each state, extract rules
value_pattern = r"If the current value is ([01]):(.*?)(?=If the current value is [01]:|$)"

# Extract write value
write_pattern = r"Write the value ([01])"

# Extract move direction
move_pattern = r"Move one slot to the (left|right)"

# Extract next state
next_pattern = r"Continue with state ([A-Z])"
```

**Parsing Algorithm**:

**Approach 1 (Recommended - Simpler)**:
```python
# Split on "In state X:" to get blocks
blocks = re.split(r'In state ([A-Z]):', text)[1:]  # Skip first empty element
states = {}
for i in range(0, len(blocks), 2):
    state_name = blocks[i]
    state_content = blocks[i+1]
    # Parse state_content for both value conditions
```

**Approach 2 (Regex with lookahead)**:
```python
# Use regex with DOTALL flag and lookahead
state_pattern = r"In state ([A-Z]):(.*?)(?=In state [A-Z]:|$)"
matches = re.findall(state_pattern, text, re.DOTALL)
for state_name, state_content in matches:
    # Parse state_content
```

**For each state block**:
1. Extract state name
2. Find two value conditions (0 and 1)
3. For each condition, extract write value, move direction, next state
4. Build nested dictionary entry

**Note**: Approach 1 is simpler and doesn't require DOTALL flag handling

## Complete Function Organization

```
parse_input(input_text: str) -> (initial_state: str, num_steps: int, states: dict)
    - Parses input string into structured data
    - Returns initial state, step count, and state machine rules

simulate_turing_machine(states: dict, initial_state: str, num_steps: int) -> dict
    - Runs the Turing machine simulation
    - Returns the tape (as defaultdict) after all steps

calculate_checksum(tape: dict) -> int
    - Counts 1s on the tape
    - Returns the diagnostic checksum

main(input_file: str = 'input.md') -> int
    - Orchestrates the entire process
    - Returns checksum (for testing)
```

**Key Design Decision**: `parse_input` accepts a string (not filename) to make it testable with different inputs. The `main` function handles file I/O.

## Expected Performance

- **Runtime**: ~10-30 seconds for 12M steps (depends on hardware)
  - Estimated based on ~400K-1.2M iterations/second in Python
  - This is typical for simple dictionary operations in a tight loop
  - Actual performance depends on CPU speed and Python version
- **Memory**: O(unique cells written) - likely < 100MB
  - Only stores non-zero tape positions
  - Expected tape range is probably a few thousand positions
- **Bottleneck**: The simulation loop itself (unavoidable - must execute each step)

## Requirements

- **Python Version**: Python 3.x (requires `defaultdict` from collections)
- **Required Imports**:
  ```python
  from collections import defaultdict
  import re
  ```
- **No external dependencies**: Uses only Python standard library

## Implementation Order

1. Write input parsing functions first
2. Test parsing with the actual input
3. Implement tape and simulation core
4. Test with small examples (6 steps from problem)
5. Run full simulation with actual input
6. Calculate and output checksum
