# Problem Report: Dual-Program Communication (Part 2)

## Objective
Implement a system that runs two copies of the Duet assembly program **concurrently**, where they communicate with each other via message queues. Count **how many times program 1 sends a value** before both programs deadlock or terminate.

## Context from Part 1
In Part 1, we interpreted the Duet assembly language as a sound-playing system where `snd` played sounds and `rcv` recovered the last sound frequency. The answer for Part 1 was 7071.

**Part 2 reveals the true purpose**: The assembly code is meant to run two programs simultaneously that communicate with each other, not play sounds at all.

## Key Changes from Part 1

### Modified Instructions:
- **`snd X`** - Now **sends** the value of X to the other program's message queue (instead of playing a sound)
- **`rcv X`** - Now **receives** the next value from this program's queue and stores it in register X. If the queue is empty, the program **waits** (blocks) until a value is sent to it. Values are received in the order they were sent.

### Other instructions remain the same:
- `set X Y` - Sets register X to the value of Y
- `add X Y` - Increases register X by the value of Y
- `mul X Y` - Multiplies register X by the value of Y
- `mod X Y` - Sets register X to X modulo Y
- `jgz X Y` - Jumps with offset Y if X > 0

## Input
The input is the same assembly program from Part 1 (same instructions), but now interpreted with the new semantics for `snd` and `rcv`.

## New Program Initialization Rules

1. **Two programs run simultaneously**: Program 0 and Program 1
2. Each program has its own set of registers (independent state)
3. Each program has its own message queue for receiving values
4. **The register `p` is initialized differently for each program**:
   - Program 0: register `p` starts at 0
   - Program 1: register `p` starts at 1
5. All other registers start at 0 (as before)

## Execution Model

### Message Passing:
- When a program executes `snd X`, the value is added to the **other** program's queue
- When a program executes `rcv X`, it retrieves the next value from **its own** queue
- A program can never receive a message it sent (each has its own queue)
- Values are received in FIFO order (first sent, first received)

### Blocking and Deadlock:
- If a program executes `rcv` when its queue is empty, it **waits** (blocks) until a value arrives
- If **both** programs are waiting for values (both blocked on `rcv` with empty queues), they are in **deadlock**
- When deadlock occurs, both programs terminate
- Programs can run at different speeds (one can be ahead of the other)

## Expected Output
A single integer: **The total number of times program 1 sent a value** (executed the `snd` instruction) before both programs terminated.

## Example Walkthrough

Given this program:
```
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
```

Execution:
1. **Program 0** sends: 1, 2, 0 (since p=0 for program 0) → these go to Program 1's queue
2. **Program 1** sends: 1, 2, 1 (since p=1 for program 1) → these go to Program 0's queue
3. **Program 0** receives from its queue: `a=1`, `b=2`, `c=1`
4. **Program 1** receives from its queue: `a=1`, `b=2`, `c=0`
5. Both programs try to `rcv d`, but both queues are empty → **deadlock**
6. Both programs terminate

In this example, **program 1 sent 3 values** (1, 2, 1), so the answer would be 3.

## Implementation Requirements

The solution should:
1. Parse the input instructions (same as Part 1)
2. Create two separate program instances, each with:
   - Its own registers (with `p` initialized to 0 or 1)
   - Its own program counter
   - Its own message queue
3. Simulate concurrent execution by alternating or interleaving the programs
4. Track how many times program 1 executes `snd`
5. Detect deadlock: both programs blocked on `rcv` with empty queues
6. Return the count of sends from program 1

## Implementation Notes

- Programs don't need to run in lockstep; one can execute many instructions while the other is blocked
- A program only blocks when it executes `rcv` with an empty queue
- The simulation continues until deadlock or both programs terminate normally (run off the end of the code)
- Need to carefully track which program is blocked vs. ready to execute
