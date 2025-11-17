# Problem Report: RTG and Microchip Transportation Puzzle

## Objective
Find the minimum number of steps required to move all Radioisotope Thermoelectric Generators (RTGs) and microchips from their initial positions across four floors to the fourth floor using an elevator.

## Context
We are in a facility with 4 floors and an elevator. The fourth floor has an assembling machine that requires all RTGs and microchips to be brought to it. We start on the first floor with the elevator.

## Safety Constraints (Critical Rules)

1. **Microchip Frying Rule**: A microchip will be destroyed if it is on the same floor as another RTG (not its own) UNLESS it is connected to its own RTG
   - Safe: Microchip + its own RTG (connected for power/shielding)
   - Safe: Microchip alone (no RTGs present)
   - Safe: Multiple microchips together (microchips don't affect each other)
   - UNSAFE: Microchip with a different RTG (will fry the chip)

2. **Elevator Constraints**:
   - Can carry at most 2 items (RTGs or microchips) in addition to yourself
   - Must carry at least 1 item (cannot move empty)
   - Stops at each floor long enough for items to irradiate each other
   - Each elevator move counts as 1 step

## Input Format
The input describes the initial state of each floor in natural language:
- Each line describes what one floor contains
- Items are either generators (e.g., "strontium generator") or microchips (e.g., "strontium-compatible microchip")
- Each element type (strontium, plutonium, etc.) has both a generator and a microchip that must be paired safely

### Example Input
```
The first floor contains a strontium generator, a strontium-compatible microchip, a plutonium generator, and a plutonium-compatible microchip.
The second floor contains a thulium generator, a ruthenium generator, a ruthenium-compatible microchip, a curium generator, and a curium-compatible microchip.
The third floor contains a thulium-compatible microchip.
The fourth floor contains nothing relevant.
```

## Expected Output
A single integer representing the minimum number of steps (elevator moves) required to transport all items to the fourth floor.

## Example Solution
Initial state (using H=Hydrogen, L=Lithium, M=Microchip, G=Generator, E=Elevator):
```
F4 .  .  .  .  .
F3 .  .  .  LG .
F2 .  HG .  .  .
F1 E  .  HM .  LM
```

Goal state (all items on floor 4):
```
F4 E  HG HM LG LM
F3 .  .  .  .  .
F2 .  .  .  .  .
F1 .  .  .  .  .
```

This example requires **11 steps** to complete.

## Algorithm Requirements
The solution must:
1. Parse the input to determine initial positions of all RTGs and microchips
2. Find a valid sequence of moves that brings all items to floor 4
3. Validate that each state does not violate the frying rule
4. Optimize to find the MINIMUM number of steps
5. Return a single integer (the step count)

## Problem Type
This is a state-space search problem, likely requiring:
- Breadth-first search (BFS) to guarantee minimum steps
- State representation (floor positions of elevator and all items)
- Valid move generation (respecting elevator capacity and safety rules)
- Visited state tracking to avoid cycles
- Goal state detection (all items on floor 4)
