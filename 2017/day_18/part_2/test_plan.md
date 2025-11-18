# Test Plan: Dual-Program Communication (Part 2)

## Overview
This test plan ensures correctness of the concurrent dual-program execution system, message passing, and deadlock detection. Testing focuses on edge cases unique to the concurrent execution model.

## Test Categories

### Category 1: Basic Message Passing

#### Test 1.1: Simple Send and Receive
**Purpose**: Verify basic snd/rcv functionality

**Input**:
```
snd 42
rcv a
```

**Expected Behavior**:
- P0 sends 42 to P1's queue
- P0 blocks on rcv (own queue empty)
- P1 sends 42 to P0's queue
- P1 blocks on rcv (own queue empty)
- P0 unblocked, receives 42 into register a, PC moves to 2 (out of bounds), terminates
- P1 unblocked, receives 42 into register a, PC moves to 2 (out of bounds), terminates
- Result: P1 sent 1 value

**Validates**:
- Basic send/receive mechanics
- Queue passing between programs
- Proper termination

#### Test 1.2: Example from Problem Statement
**Purpose**: Validate against provided example

**Input**:
```
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
```

**Expected Result**: 3 (P1 sends: 1, 2, 1)

**Validates**:
- Register `p` initialized correctly (0 for P0, 1 for P1)
- FIFO queue ordering
- Deadlock detection with both programs blocked

### Category 2: Register Initialization

#### Test 2.1: Register p Initialization
**Purpose**: Ensure p starts at correct value for each program

**Input**:
```
snd p
snd p
rcv a
rcv b
```

**Expected Behavior**:
- P0 sends 0, 0 to P1
- P1 sends 1, 1 to P0
- Both receive correctly
- Result: P1 sent 2 values

**Validates**:
- P0's p register = 0
- P1's p register = 1
- Other registers still start at 0

#### Test 2.2: Other Registers Start at Zero
**Purpose**: Verify only p is special

**Input**:
```
snd a
snd b
rcv x
rcv y
```

**Expected Behavior**:
- P0 sends 0, 0 (a and b both 0)
- P1 sends 0, 0
- Both receive and terminate
- Result: P1 sent 2 values

**Validates**:
- All non-p registers initialize to 0
- P1's other registers also start at 0

### Category 3: Deadlock Detection

#### Test 3.1: Both Programs Blocked with Empty Queues
**Purpose**: Basic deadlock scenario

**Input**:
```
rcv a
```

**Expected Behavior**:
- P0 blocks immediately (queue empty)
- P1 blocks immediately (queue empty)
- Immediate deadlock
- Result: P1 sent 0 values

**Validates**:
- Deadlock detection with no sends
- Empty queue blocking

#### Test 3.2: Deadlock After Exchange
**Purpose**: Deadlock after some execution

**Input**:
```
snd 1
snd 2
rcv a
rcv b
rcv c
```

**Expected Behavior**:
- Programs exchange values
- Both eventually block waiting for third value
- Result: P1 sent 2 values

**Validates**:
- Partial execution before deadlock
- Deadlock with non-empty send history

#### Test 3.3: One Program Sends Many, Then Deadlock
**Purpose**: Asymmetric execution

**Input**:
```
jgz p 3
snd 1
snd 2
snd 3
rcv a
```

**Expected Behavior**:
- P0 (p=0): jgz condition is false (0 not > 0), doesn't jump, sends 1, 2, 3 to P1's queue
- P0 blocks on rcv (own queue is empty)
- P1 (p=1): jgz condition is true (1 > 0), jumps 3 instructions ahead to rcv
- P1 blocks on rcv (own queue is empty initially)
- P1 wakes up (has 1, 2, 3 in queue from P0), receives 1, then blocks again on next iteration
- Actually, P1 receives 1 into register a, then PC increments past end of program, terminates
- P0 remains blocked (P1 never sent anything)
- One program blocked, one terminated, but P0's queue is empty → effectively deadlock
- Result: P1 sent 0 values

**Validates**:
- Programs can execute different paths based on p register
- Asymmetric execution where one program terminates without sending
- Handling case where one program never sends

### Category 4: Program Termination

#### Test 4.1: Program Runs Off End
**Purpose**: Verify termination by pc out of bounds

**Input**:
```
snd 1
```

**Expected Behavior**:
- P0 sends 1, pc goes to 1 (out of bounds), terminates
- P1 sends 1, pc goes to 1 (out of bounds), terminates
- Both terminate naturally
- Result: P1 sent 1 value

**Validates**:
- Natural termination detection
- pc bounds checking
- No infinite loop

#### Test 4.2: Different Execution Paths Leading to Deadlock
**Purpose**: Programs execute different code paths based on p

**Input**:
```
jgz p 2
snd 1
rcv a
rcv b
```

**Expected Behavior**:
- P0 (p=0) doesn't jump, sends 1 to P1's queue, blocks on rcv a (own queue empty)
- P1 (p=1) jumps over snd, goes directly to rcv a, blocks (own queue empty)
- P1 wakes up (has 1 in queue), receives 1 into a, then blocks on rcv b (queue empty)
- P0 still blocked (P1 never sent anything)
- Both blocked, both queues empty → Deadlock
- Result: P1 sent 0 values

**Validates**:
- Different execution paths based on conditional jumps
- Asymmetric send patterns
- Deadlock with different execution histories

### Category 5: Queue Mechanics

#### Test 5.1: FIFO Ordering
**Purpose**: Verify first-in-first-out

**Input**:
```
snd 10
snd 20
snd 30
rcv a
rcv b
rcv c
set x a
add x b
add x c
mul x -1
snd x
rcv d
```

**Expected Behavior**:
- P0 sends 10, 20, 30
- P1 sends 10, 20, 30
- P0 receives in order: 10, 20, 30
- P1 receives in order: 10, 20, 30
- P0 computes (10+20+30)*-1 = -60, sends -60
- P1 computes (10+20+30)*-1 = -60, sends -60
- Eventually deadlock on next rcv
- Result: P1 sent 4 values (10, 20, 30, -60)

**Validates**:
- Correct FIFO ordering
- Queue doesn't reorder values
- Arithmetic with received values
- Negative results from computation

#### Test 5.2: Large Queue Buildup
**Purpose**: One program sends many before other receives

**Input**:
```
set i 5
snd i
add i -1
jgz i -2
rcv a
rcv b
rcv c
```

**Expected Behavior**:
- P0 sends 5, 4, 3, 2, 1 (loop 5 times)
- P1 sends 5, 4, 3, 2, 1
- Both start receiving
- Eventually deadlock on 4th receive
- Result: P1 sent 5 values

**Validates**:
- Queue can hold multiple values
- Correct loop execution
- Receives drain queue in order

### Category 6: Send Counting

#### Test 6.1: Only Count Program 1 Sends
**Purpose**: Ensure only P1 sends are counted

**Input**:
```
snd 1
snd 2
snd 3
rcv a
rcv b
rcv c
```

**Expected Behavior**:
- P0 sends 3 values (NOT counted)
- P1 sends 3 values (COUNTED)
- Result: 3 (only P1's sends)

**Validates**:
- Send counter is program-specific
- Only P1 sends affect result

#### Test 6.2: Zero Sends from Program 1
**Purpose**: P1 never sends

**Input**:
```
jgz p 2
snd 1
rcv a
```

**Expected Behavior**:
- P0 (p=0) doesn't jump, sends 1
- P1 (p=1) jumps over snd, blocks on rcv
- Deadlock
- Result: 0 (P1 never sent)

**Validates**:
- Counter starts at 0
- Can return 0 if P1 doesn't send

### Category 7: Complex Control Flow

#### Test 7.1: Backward Jump Loop with Send Counting
**Purpose**: Verify send counting works correctly in loops with backward jumps

**Input**:
```
set counter 3
snd counter
add counter -1
jgz counter -2
rcv x
```

**Expected Behavior**:
- P0: counter=3, sends 3, counter=2, jumps back, sends 2, counter=1, jumps back, sends 1, counter=0, no jump, rcv blocks
- P1: Same pattern, sends 3, 2, 1
- Both receive from each other's queues and eventually deadlock
- Result: P1 sent 3 values

**Validates**:
- Backward jump mechanics
- Loop execution with countdown
- Send counting in loops

#### Test 7.2: Loops with Sends
**Purpose**: Verify send counting in loops

**Input**:
```
set a 3
snd a
add a -1
jgz a -2
rcv b
```

**Expected Behavior**:
- P0 sends 3, 2, 1 (loop 3 times)
- P1 sends 3, 2, 1
- Both try to receive, deadlock
- Result: P1 sent 3 values

**Validates**:
- Send counting in loops
- Correct loop termination
- Jump mechanics

#### Test 7.3: Conditional Sends Based on p
**Purpose**: Different behavior per program

**Input**:
```
jgz p 4
snd 100
snd 200
jgz 1 2
snd 300
snd 400
rcv a
```

**Expected Behavior**:
- P0 (p=0): sends 100, 200, jumps, sends 300, 400
- P1 (p=1): jumps, sends 300, 400
- Different send counts, complex interaction
- Result: P1 sent 2 values (300, 400)

**Validates**:
- Conditional execution based on p
- Different code paths per program
- Correct jump offsets

### Category 8: Edge Cases

#### Test 8.1: Negative Values in Queue
**Purpose**: Ensure negative numbers work

**Input**:
```
set a -10
snd a
rcv b
```

**Expected Behavior**:
- Programs exchange -10
- Both terminate
- Result: P1 sent 1 value

**Validates**:
- Negative values in queues
- Negative register values

#### Test 8.2: Send Literal vs Register
**Purpose**: Both send modes work

**Input**:
```
snd 42
set x 99
snd x
rcv a
rcv b
```

**Expected Behavior**:
- Programs send 42 (literal), then 99 (register)
- Both receive both values
- Deadlock on next receive
- Result: P1 sent 2 values

**Validates**:
- snd with literal
- snd with register
- Both modes counted correctly

#### Test 8.3: Receive Updates Register Correctly
**Purpose**: rcv stores in correct register

**Input**:
```
snd 77
rcv x
snd x
rcv y
```

**Expected Behavior**:
- P0 sends 77
- P0 receives 77 into x
- P0 sends 77 (value of x)
- Complex exchange
- Result: P1 sent 2 values

**Validates**:
- rcv stores to specified register
- Can send received value
- Register values persist

## Validation Strategy

### Phase 1: Unit Tests
1. Test example from problem (must return 3)
2. Test basic send/receive
3. Test p register initialization
4. Test deadlock detection

### Phase 2: Edge Case Tests
1. Empty queues
2. Large queues
3. Negative values
4. Zero sends

### Phase 3: Actual Input Validation
1. Run with actual input
2. Verify program terminates (no infinite loop)
3. Verify result is reasonable (likely in thousands based on input analysis)
4. Check execution completes in reasonable time (<1 second)
5. Verify the program detected actual deadlock (both programs blocked, both queues empty)
6. Run program twice to ensure result is deterministic (should get same answer both times)
7. If known answer available, compare against it

### Expected Performance
- **Input size**: ~41 instructions
- **Estimated sends**: Looking at input, program has a loop sending ~127 values (lines 9-20), and more sends in later loops (lines 24-41). P1 likely sends hundreds to thousands of values.
- **Expected runtime**: Should complete in <1 second

## How to Verify Correctness

### Manual Trace (Small Example)
- Manually trace the example program step-by-step
- Verify queue contents at each step
- Confirm deadlock detection triggers correctly
- Validate send count matches manual count

### Automated Tests
- Implement all test cases as functions
- Assert expected results
- Run full test suite before submitting

### Actual Input Sanity Checks
- Result should be > 0 (P1 must send something)
- Result should be < 1,000,000 (reasonable upper bound)
- Program should not infinite loop (timeout check)
- Both programs should eventually deadlock or terminate

## Success Criteria
- All unit tests pass
- Example test returns 3
- Actual input produces a result in reasonable time
- No infinite loops
- Deadlock detection works reliably
