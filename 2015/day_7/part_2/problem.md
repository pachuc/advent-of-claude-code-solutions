# Problem Report: Circuit Signal Simulation (Part 2)

## Objective
We need to simulate a circuit of wires and bitwise logic gates to determine what signal is ultimately provided to wire `a` after applying a specific modification based on Part 1's result.

## Context
This is a circuit emulation puzzle involving wires that carry 16-bit signals (values from 0 to 65535). Each wire receives a signal from a gate, another wire, or a specific value. Gates only provide output when all inputs are available.

## Part 2 Specific Instructions
1. First, run the circuit simulation with the original instructions to find the signal on wire `a`
2. Take the signal value from wire `a` (from step 1)
3. Override wire `b` with that signal value
4. Reset all other wires (including wire `a`) to their initial state
5. Run the circuit simulation again with the modified wire `b`
6. Report the new signal ultimately provided to wire `a`

## Input Format
The input consists of circuit instructions, one per line. Each instruction follows one of these patterns:

- **Direct assignment:** `<value> -> <wire>` (e.g., `123 -> x`)
- **AND gate:** `<input1> AND <input2> -> <wire>` (e.g., `x AND y -> z`)
- **OR gate:** `<input1> OR <input2> -> <wire>` (e.g., `x OR y -> z`)
- **NOT gate:** `NOT <input> -> <wire>` (e.g., `NOT e -> f`)
- **LSHIFT (left shift):** `<input> LSHIFT <amount> -> <wire>` (e.g., `p LSHIFT 2 -> q`)
- **RSHIFT (right shift):** `<input> RSHIFT <amount> -> <wire>` (e.g., `y RSHIFT 2 -> g`)

Where:
- `<value>` is a decimal number (0-65535)
- `<wire>` is an identifier made of lowercase letters
- `<input>`, `<input1>`, `<input2>` can be either a wire identifier or a numeric value
- `<amount>` is a numeric value for shift operations

## Operations
All operations are bitwise and work with 16-bit unsigned integers:
- **AND:** Bitwise AND of two inputs
- **OR:** Bitwise OR of two inputs
- **NOT:** Bitwise complement (NOT x = 65535 - x for 16-bit)
- **LSHIFT:** Left shift (multiply by 2^amount, with overflow)
- **RSHIFT:** Right shift (integer divide by 2^amount)

## Expected Output
A single integer representing the signal value on wire `a` after:
1. Running the original circuit
2. Taking wire `a`'s original signal and overriding wire `b` with it
3. Resetting and re-running the circuit with the modified wire `b` value

## Algorithm Requirements
1. Parse all circuit instructions
2. Implement a dependency resolution system (gates only fire when all inputs are available)
3. Run the circuit simulation to completion (first run)
4. Extract the signal from wire `a`
5. Modify the instruction for wire `b` to use the value from step 4
6. Clear all wire values and re-run the simulation
7. Return the final signal on wire `a`

## Notes
- Wires can only receive signals from one source
- Wires can provide signals to multiple destinations
- The circuit must be evaluated respecting dependencies (topological order or iterative evaluation until stable)
- All values are 16-bit unsigned integers (0-65535)
