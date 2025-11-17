# Problem Report: Look-and-Say Sequence (Part 2)

## Objective
Calculate the length of a string after applying the "look-and-say" transformation process 50 times to the given input.

## Background: The Look-and-Say Process
The look-and-say sequence (also known as the Conway sequence) is a method of describing a sequence of digits by reading consecutive runs of the same digit aloud.

### Transformation Rules
For each step, take the current string and replace each consecutive run of identical digits with:
1. The count of how many times the digit appears consecutively
2. Followed by the digit itself

### Examples of the Transformation
- `1` → `11` (one 1)
- `11` → `21` (two 1s)
- `21` → `1211` (one 2, one 1)
- `1211` → `111221` (one 1, one 2, two 1s)
- `111221` → `312211` (three 1s, two 2s, one 1)

## Input
- **Format**: A string of digits
- **Provided Input**: `1321131112`
- **Source**: input.md

## Task
Apply the look-and-say transformation process **50 times** (iteratively, where each iteration uses the output from the previous iteration as its input).

## Expected Output
- **Type**: An integer
- **Value**: The length of the final string after 50 iterations
- **Format**: Just the numeric length value

## Important Notes
- This is Part 2 of a two-part problem. Part 1 required 40 iterations; Part 2 increases this to 50 iterations.
- Only the length is needed, not the actual final string itself.
- The sequence grows rapidly with each iteration, so the final string will be very long.
