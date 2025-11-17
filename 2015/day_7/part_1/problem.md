# Problem Report: Circuit Emulation

## Context
We need to emulate a circuit of wires and bitwise logic gates. Each wire has an identifier (lowercase letters) and carries a 16-bit signal (a number from 0 to 65535). Wires receive signals from gates, other wires, or specific values. Each wire can only receive from one source but can provide its signal to multiple destinations. Gates only output a signal once all their inputs have signals.

## Objective
Calculate the signal value ultimately provided to wire `a` after processing all circuit instructions.

## Input Format
The input is a series of instructions describing how to connect wires and gates. Each line follows one of these patterns:

1. **Direct assignment**: `<value> -> <wire>` or `<source_wire> -> <destination_wire>`
   - Example: `123 -> x` (assigns value 123 to wire x)
   - Example: `lx -> a` (assigns the value from wire lx to wire a)

2. **AND gate**: `<input1> AND <input2> -> <output>`
   - Example: `x AND y -> z` (bitwise AND of x and y stored in z)
   - Note: inputs can be wire identifiers OR numeric values

3. **OR gate**: `<input1> OR <input2> -> <output>`
   - Example: `x OR y -> e` (bitwise OR of x and y stored in e)

4. **LSHIFT**: `<input> LSHIFT <amount> -> <output>`
   - Example: `x LSHIFT 2 -> f` (left shift x by 2 bits, store in f)

5. **RSHIFT**: `<input> RSHIFT <amount> -> <output>`
   - Example: `y RSHIFT 2 -> g` (right shift y by 2 bits, store in g)

6. **NOT gate**: `NOT <input> -> <output>`
   - Example: `NOT x -> h` (bitwise complement of x stored in h)

## Important Details

- **Signal values**: All signals are 16-bit unsigned integers (0 to 65535)
- **Bitwise NOT**: For 16-bit values, NOT uses bitwise complement within the 16-bit range
- **Order independence**: Instructions can appear in any order. Some wires depend on others, so evaluation order must respect dependencies
- **Direct values**: Some instructions use numeric literals directly (e.g., `44430 -> b`, `1 AND fi -> fj`)

## Expected Output
A single integer representing the signal value on wire `a`.

## Example
Given this simple circuit:
```
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
```

The final signals should be:
- d: 72
- e: 507
- f: 492
- g: 114
- h: 65412
- i: 65079
- x: 123
- y: 456

## Algorithm Approach
1. Parse all instructions to understand wire dependencies
2. Evaluate wires in dependency order (or use memoization/caching to compute on demand)
3. Handle the 16-bit constraint for all operations
4. Return the final value of wire `a`
