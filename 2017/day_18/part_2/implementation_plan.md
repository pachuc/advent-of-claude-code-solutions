# Implementation Plan: Dual-Program Communication (Part 2)

## Overview
Part 2 transforms the Part 1 sound-playing interpreter into a dual-program concurrent execution system with message passing. We need to simulate two programs running simultaneously, communicating via queues, and detect deadlock.

## Key Algorithm Considerations

### Runtime Complexity
- **Time Complexity**: O(n * i) where n is the number of instructions and i is the number of iterations
  - Each program can loop multiple times
  - Looking at the input, there are loops that send multiple values (lines 9-20 send ~127 values)
  - The actual input has ~41 instructions, but programs may execute thousands of iterations
- **Space Complexity**: O(q) where q is the maximum queue size
  - Queues can grow if one program sends faster than the other receives
  - Need efficient queue operations (deque is ideal)

### Execution Strategy
Based on analysis of the input program:
1. Programs will alternate sending and receiving
2. One program may get far ahead while the other is blocked
3. Need to execute programs in a round-robin or run-until-blocked fashion
4. **Key insight**: Continue running each program until it blocks or terminates

### Deadlock Detection
- Both programs must be in a "blocked waiting for receive" state
- Both queues must be empty
- This is the ONLY termination condition mentioned in the problem

## Step-by-Step Implementation Plan

### Step 1: Reuse Core Infrastructure from Part 1
**File**: Adapt from `part_1_solution.py`

**What to reuse:**
- `get_value()` function - Works identically for resolving operands
- Instruction parsing logic - Same input format
- Most instruction implementations (set, add, mul, mod, jgz) - Identical semantics

**What changes:**
- `snd` and `rcv` instructions have completely different semantics
- Need to track program state (running, blocked, terminated)
- Need separate register sets and program counters for each program

### Step 2: Define Program State Class
**Purpose**: Encapsulate each program's independent state

**Attributes:**
```python
class Program:
    program_id: int          # 0 or 1
    registers: defaultdict   # Initialize p to program_id, rest to 0
    pc: int                  # Program counter (starts at 0)
    message_queue: deque     # FIFO queue for incoming messages
    state: str               # "running", "blocked", or "terminated"
    send_count: int          # Track sends (only for program 1)
```

**Methods:**
- `__init__(program_id)` - Initialize with p register set correctly
- `is_blocked()` - Check if waiting on empty queue
- `is_terminated()` - Check if pc out of bounds
- `can_execute()` - Returns `True` if state == "running", `False` otherwise

### Step 3: Implement Modified Instruction Set
**File**: Core execution logic

**Instructions to implement:**

1. **`snd X`** - Modified behavior
   ```python
   - Get value of X using get_value()
   - Add value to OTHER program's queue
   - If this is program 1, increment send_count
   - Increment pc
   ```

2. **`rcv X`** - Completely new behavior
   ```python
   - If this program's queue is empty:
       - Set state to "blocked"
       - Do NOT increment pc (retry when unblocked)
       - Return control to scheduler
   - Else:
       - Pop value from queue (FIFO)
       - Store in register X
       - Set state to "running"
       - Increment pc
   ```

3. **`set`, `add`, `mul`, `mod`** - Copy from Part 1
   - Identical implementation
   - Always increment pc after execution

4. **`jgz X Y`** - Copy from Part 1
   - If value(X) > 0: pc += value(Y)
   - Else: pc += 1

### Step 4: Implement Execution Scheduler
**Purpose**: Coordinate the two programs and detect deadlock

**Algorithm**: Run-until-blocked approach (most efficient)
```python
def execute_programs(instructions):
    # Initialize two programs
    program0 = Program(0)
    program1 = Program(1)

    # Keep executing until both are blocked or terminated
    while True:
        # CRITICAL: Unblock programs if they now have messages in their queue
        # A program that was blocked waiting for a receive should transition
        # back to "running" state if the other program sent it a message
        if program0.state == "blocked" and len(program0.message_queue) > 0:
            program0.state = "running"
        if program1.state == "blocked" and len(program1.message_queue) > 0:
            program1.state = "running"

        # Try to execute program 0 until it blocks or terminates
        execute_until_blocked(program0, program1, instructions)

        # Try to execute program 1 until it blocks or terminates
        execute_until_blocked(program1, program0, instructions)

        # Check termination conditions
        if is_deadlock(program0, program1):
            break

        if both_terminated(program0, program1):
            break

    return program1.send_count
```

**Why run-until-blocked?**
- More efficient than single-step alternation
- Matches the problem description (programs can run at different speeds)
- Avoids unnecessary context switches

**State Transition Logic**:
- Before each execution cycle, check if blocked programs have received messages
- If a program is blocked but its queue is non-empty, set state back to "running"
- This allows the program to retry the rcv instruction that caused it to block

### Step 5: Implement execute_until_blocked Function
**Purpose**: Execute one program until it blocks or terminates

```python
def execute_until_blocked(current_program, other_program, instructions):
    executed_count = 0

    while current_program.can_execute():
        # Check if pc is out of bounds
        if not (0 <= current_program.pc < len(instructions)):
            current_program.state = "terminated"
            break

        # Get current instruction
        instruction = instructions[current_program.pc]
        op = instruction[0]

        # Execute instruction
        if op == "snd":
            value = get_value(instruction[1], current_program.registers)
            other_program.message_queue.append(value)
            if current_program.program_id == 1:
                current_program.send_count += 1
            current_program.pc += 1

        elif op == "rcv":
            if len(current_program.message_queue) == 0:
                current_program.state = "blocked"
                break  # Stop execution, don't increment pc
            else:
                value = current_program.message_queue.popleft()
                current_program.registers[instruction[1]] = value
                current_program.state = "running"
                current_program.pc += 1

        elif op == "set":
            # ... standard implementation
            current_program.pc += 1

        # ... other instructions

        executed_count += 1

        # Safety check to prevent infinite loops in a single run
        # Increased to 10 million since legitimate loops can be long
        # (e.g., input has loops that may execute many iterations)
        if executed_count > 10000000:
            break

    return executed_count > 0
```

### Step 6: Implement Deadlock and Termination Detection
**Purpose**: Determine when both programs are permanently stuck or completed

```python
def is_deadlock(program0, program1):
    # Both must be blocked on receive
    both_blocked = (program0.state == "blocked" and
                    program1.state == "blocked")

    # Both queues must be empty
    both_empty = (len(program0.message_queue) == 0 and
                  len(program1.message_queue) == 0)

    return both_blocked and both_empty

def both_terminated(program0, program1):
    """Check if both programs have terminated naturally (pc out of bounds)"""
    return (program0.state == "terminated" and
            program1.state == "terminated")
```

**Critical insight**: If a program is blocked but the other has items in its queue, it's NOT deadlock - the blocked program will eventually get unblocked when the other sends.

### Step 7: Main Solve Function
**Purpose**: Orchestrate the entire solution

```python
from collections import deque, defaultdict

def solve(input_file='input.md'):
    # Parse instructions (reuse Part 1 logic)
    instructions = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                instructions.append(line.split())

    # Create two programs
    program0 = Program(0)
    program1 = Program(1)

    # Execute until deadlock or termination
    while True:
        # Unblock programs that now have messages waiting
        if program0.state == "blocked" and len(program0.message_queue) > 0:
            program0.state = "running"
        if program1.state == "blocked" and len(program1.message_queue) > 0:
            program1.state = "running"

        # Execute program 0 until blocked/terminated
        execute_until_blocked(program0, program1, instructions)

        # Execute program 1 until blocked/terminated
        execute_until_blocked(program1, program0, instructions)

        # Check deadlock
        if is_deadlock(program0, program1):
            break

        # Check both terminated (off end of code)
        if both_terminated(program0, program1):
            break

    return program1.send_count
```

**Note**: Import statements needed at top of file:
- `from collections import deque, defaultdict`

## Implementation Notes

### Data Structures
- **`collections.deque`**: Use for queues (O(1) append and popleft)
- **`collections.defaultdict(int)`**: Use for registers (auto-initialize to 0)
- **Simple list**: Use for instructions (parsed once, read-only)

### Edge Cases to Handle
1. **Empty queue receive**: Must block, not crash
2. **Program counter out of bounds**: Terminate gracefully
3. **Both programs terminate normally**: Not just deadlock
4. **One program terminates while other is blocked**: Still deadlock
5. **Register `p` initialization**: Critical for correct behavior

### Optimization Considerations
- Run programs until blocked (not single-step) for efficiency
- Use deque for O(1) queue operations
- Avoid copying data structures unnecessarily
- Early termination on deadlock detection

### Code Organization
```
solution.py
├── Imports                  # from collections import deque, defaultdict
├── get_value()              # Reused from Part 1
├── class Program            # New: encapsulate program state
├── execute_until_blocked()  # New: run one program
├── is_deadlock()           # New: detect deadlock
├── both_terminated()       # New: detect normal termination
├── solve()                 # Modified from Part 1
└── main block              # Test and run
```

## Expected Behavior on Example Input

Given example from problem:
```
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
```

**Execution trace:**
1. P0 sends 1, 2, 0 (p=0) to P1's queue → P1 queue: [1, 2, 0]
2. P0 blocks on `rcv a` (own queue empty)
3. Scheduler checks: P1 has messages, P1 is still running
4. P1 sends 1, 2, 1 (p=1) to P0's queue → P0 queue: [1, 2, 1]
5. P1 blocks on `rcv a` (own queue empty)
6. Scheduler unblocks P0 (has messages), P0 state → "running"
7. P0 receives: a=1, b=2, c=1 (from P1's sends)
8. P0 blocks on `rcv d` (queue empty)
9. Scheduler unblocks P1 (has messages), P1 state → "running"
10. P1 receives: a=1, b=2, c=0 (from P0's sends)
11. P1 blocks on `rcv d` (queue empty)
12. Scheduler checks: both blocked, both queues empty → DEADLOCK
13. Return P1's send_count = 3

## Validation Approach
- Implement the example test case first
- Verify send counting is accurate
- Ensure deadlock detection works correctly
- Test with actual input
