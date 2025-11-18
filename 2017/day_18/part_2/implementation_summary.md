# Implementation Summary: Dual-Program Communication (Part 2)

## Overview
Successfully implemented a dual-program concurrent execution system where two copies of the Duet assembly program run simultaneously and communicate via message queues. The solution tracks how many times Program 1 sends a value before both programs deadlock.

## Solution Approach

### Key Design Decisions

1. **Program Class Encapsulation**: Created a `Program` class to encapsulate each program's independent state:
   - `program_id`: Identifies the program (0 or 1)
   - `registers`: Dictionary of register values (with `p` initialized to program ID)
   - `pc`: Program counter for tracking instruction position
   - `message_queue`: FIFO deque for incoming messages
   - `state`: Current execution state ("running", "blocked", or "terminated")
   - `send_count`: Tracks sends (only for Program 1)

2. **Reused Core Logic from Part 1**:
   - `get_value()` function: Resolves operands to integer values
   - Instruction parsing logic: Same input format
   - Arithmetic instructions (set, add, mul, mod, jgz): Identical semantics

3. **Modified Instructions for Part 2**:
   - `snd X`: Now sends value to the other program's queue (instead of playing sound)
   - `rcv X`: Now receives from own queue and blocks if empty (instead of recovering sound)

4. **Execution Strategy**: Run-until-blocked approach
   - Execute each program until it blocks on receive or terminates
   - More efficient than single-step alternation
   - Programs can run at different speeds (one may get ahead while other is blocked)

### Implementation Structure

**solution.py** contains:
1. `get_value()`: Reused from Part 1 for operand resolution
2. `Program` class: Encapsulates program state
3. `execute_until_blocked()`: Runs one program until it blocks or terminates
4. `is_deadlock()`: Detects deadlock condition (both blocked, both queues empty)
5. `both_terminated()`: Detects normal termination (both programs off end of code)
6. `solve()`: Main orchestration function with dual-program execution loop
7. Test suite with 5 comprehensive tests

### Execution Flow

The main solve function follows this pattern:

1. Parse instructions from input
2. Initialize two Program instances (with p=0 and p=1 respectively)
3. Loop until deadlock or termination:
   - Unblock any programs that now have messages in their queues
   - Execute Program 0 until it blocks or terminates
   - Execute Program 1 until it blocks or terminates
   - Check for deadlock (both blocked with empty queues)
   - Check if both programs terminated naturally
4. Return Program 1's send count

### Critical Implementation Details

1. **State Transitions**: Programs transition from "running" to "blocked" when executing `rcv` with an empty queue. They transition back to "running" when a message arrives in their queue.

2. **Deadlock Detection**: Deadlock occurs only when:
   - Both programs are in "blocked" state
   - Both message queues are empty
   - This prevents false positives when one program is blocked but the other still has messages to send

3. **Message Passing**: When a program executes `snd`, the value is added to the OTHER program's queue (not its own). Values are received in FIFO order.

4. **Register p Initialization**: Critical for correct behavior - Program 0 has p=0, Program 1 has p=1, allowing different execution paths based on conditional jumps.

## Files Created

- **solution.py**: Complete implementation with Program class, execution logic, deadlock detection, and test suite

## Testing Process

### Test Suite Results

All 5 tests passed successfully:

1. **Example Test (from problem statement)**:
   - Programs send 1, 2, p and receive until deadlock
   - Expected: 3, Got: 3 ✓

2. **Simple Send/Receive Test**:
   - Basic message passing between programs
   - Expected: 1, Got: 1 ✓

3. **Register p Initialization Test**:
   - Verifies p is set to 0 for Program 0 and 1 for Program 1
   - Expected: 2, Got: 2 ✓

4. **Immediate Deadlock Test**:
   - Both programs block immediately on receive
   - Expected: 0, Got: 0 ✓

5. **Loop with Sends Test**:
   - Programs loop and send multiple values
   - Expected: 3, Got: 3 ✓

### Actual Input Testing

- **Result**: 8001
- **Execution time**: < 1 second
- **Deterministic**: Multiple runs produced the same result
- **No infinite loops**: Program terminated as expected
- **Deadlock detection**: Both programs properly blocked with empty queues

### Validation Checks

✓ Result is > 0 (Program 1 sent messages)
✓ Result is reasonable (in thousands, as expected from input analysis)
✓ Program terminates in reasonable time
✓ Result is deterministic across multiple runs
✓ All test cases pass
✓ Deadlock detection works correctly

## Algorithm Complexity

- **Time Complexity**: O(n × i) where n is the number of instructions and i is the number of iterations
  - The actual input has 41 instructions
  - Programs loop multiple times (especially lines 9-20 which send ~127 values)
  - Actual execution involved thousands of instruction executions

- **Space Complexity**: O(q) where q is the maximum queue size
  - Used `collections.deque` for O(1) append and popleft operations
  - Queues grow temporarily when one program sends faster than the other receives

## Key Insights

1. **Adapting Part 1**: Successfully reused ~70% of Part 1 code (parsing, get_value, arithmetic instructions)

2. **State Management**: The Program class cleanly encapsulates state, making it easy to manage two independent program instances

3. **Efficient Execution**: Run-until-blocked approach is much more efficient than single-stepping both programs

4. **Deadlock vs Termination**: Important to distinguish between deadlock (both blocked) and normal termination (both finished)

5. **Message Queues**: Using deque provides efficient O(1) operations for FIFO queue management

## Final Answer

**8001** - Program 1 sent 8001 values before both programs deadlocked.
