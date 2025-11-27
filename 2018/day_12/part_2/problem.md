# Problem Report: Plant Growth Simulation (Part 2)

## Overview
This is Part 2 of the plant growth simulation problem. Instead of simulating 20 generations, we need to simulate **50 billion generations** (50,000,000,000). This requires detecting patterns rather than brute-force simulation, as simulating 50 billion iterations directly is computationally infeasible.

## Part 1 Context (Completed)
In Part 1, we simulated plant growth for 20 generations and calculated the sum of pot indices containing plants. The answer was **2767**.

### How Plant Growth Works
- Pots are numbered with pot 0 in the center, extending infinitely left (negative numbers) and right (positive numbers)
- Each pot either contains a plant (`#`) or is empty (`.`)
- For each generation, a pot's next state is determined by examining a 5-pot window: the pot itself, 2 pots to its left, and 2 pots to its right
- Spreading rules map each 5-character pattern (like `.##.#`) to a result (`#` or `.`)
- All changes happen simultaneously each generation

## Part 2 Challenge

### The Task
Simulate **fifty billion generations** (50,000,000,000) and calculate the sum of pot numbers containing plants.

### Why This Is Different
Simulating 50 billion iterations directly is impossible. The key insight is that the pattern of plants will eventually stabilize and either:
1. Repeat exactly (cycle)
2. Shift in the same direction each generation (steady state)

When the pattern stabilizes, we can use mathematics to extrapolate to generation 50 billion without simulating every single generation.

### Input Format
Same as Part 1:
1. **Initial State**: Line starting with `initial state: ` followed by `#` and `.` characters representing pots starting from pot 0
2. **Spreading Rules**: Lines in format `LLCRR => N` where `LLCRR` is a 5-character pattern and `N` is the result (`#` or `.`)

### Expected Approach
1. Simulate generations until a pattern is detected (either repeating or steady-state)
2. Detect when the pattern stabilizes:
   - The set of plants relative to each other stays the same
   - The pattern may shift left or right by a constant amount each generation
3. Once stability is detected, calculate the rate of change
4. Extrapolate to generation 50 billion using the detected pattern

### Expected Output
A single integer: the sum of all pot numbers containing plants after 50 billion generations.

### Key Considerations
- **Pattern Detection**: Compare generations to find when the relative pattern of plants stops changing
- **Steady State**: Once stable, track how much the pattern shifts per generation
- **Extrapolation**: If at generation G the sum is S, and each generation adds D to the sum, then at generation 50 billion, the sum would be: S + (50000000000 - G) * D
- **Efficiency**: Only simulate until pattern stabilizes (likely within a few hundred or thousand generations at most)

### Example Logic
If after 100 generations:
- The pattern of plants is stable (same relative positions)
- The pattern shifts right by 1 pot each generation
- Each shift adds 50 to the sum (if there are 50 plants)
- Then we can calculate: `current_sum + (50000000000 - 100) * 50`

### Output Format
A single integer representing the sum of all pot numbers containing plants after 50,000,000,000 generations.
