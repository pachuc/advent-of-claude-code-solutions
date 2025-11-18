# Problem Report: Memory Reallocation Cycle Detection

## Objective
Detect when a memory reallocation routine enters an infinite loop by counting how many redistribution cycles occur before a previously-seen configuration repeats.

## Context
A debugger is attempting to repair a memory reallocation routine that balances blocks across memory banks. The routine gets stuck in an infinite loop, repeatedly cycling through configurations. We need to determine when this loop begins.

## Input
- A single line containing space-separated integers
- Each integer represents the number of blocks in a memory bank
- Memory banks are indexed starting from the first number (index 0)
- Example: `11 11 13 7 0 15 5 5 4 4 1 1 7 1 15 11` (16 memory banks)

## Algorithm Requirements

### Reallocation Process
Each redistribution cycle follows these rules:

1. **Select the bank**: Find the memory bank with the most blocks
   - If there's a tie, choose the bank with the lowest index

2. **Redistribute blocks**:
   - Remove all blocks from the selected bank (bank becomes 0)
   - Starting with the next bank (by index), place one block at a time
   - Continue sequentially through banks, wrapping around to index 0 after the last bank
   - Continue until all blocks from the selected bank have been distributed

3. **Track configurations**: After each redistribution, record the configuration of all memory banks

4. **Detect repetition**: Stop when a configuration appears that has been seen before (including the initial state)

### Example Walkthrough
Initial state: `0 2 7 0`

- Cycle 1: Bank 2 has 7 blocks → Redistribute → `2 4 1 2`
- Cycle 2: Bank 1 has 4 blocks → Redistribute → `3 1 2 3`
- Cycle 3: Bank 0 has 3 blocks (wins tie) → Redistribute → `0 2 3 4`
- Cycle 4: Bank 3 has 4 blocks → Redistribute → `1 3 4 1`
- Cycle 5: Bank 2 has 4 blocks → Redistribute → `2 4 1 2`

Configuration `2 4 1 2` was seen after Cycle 1, so the answer is **5** cycles.

## Expected Output
A single integer representing the number of redistribution cycles completed before a repeated configuration is encountered.

## Key Implementation Details
- Track all seen configurations (can use a set or hash structure)
- Handle index wrapping correctly when redistributing blocks
- Remember that tie-breaking favors the **lowest index**
- Count cycles, not unique configurations
