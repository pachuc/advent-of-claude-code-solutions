# Problem Report: Look-and-Say Sequence

## Objective
Calculate the length of a string after applying the "look-and-say" transformation 40 times.

## Background
The look-and-say sequence (also known as the Morris number sequence) is a method of describing a sequence of digits by counting consecutive runs of the same digit.

## Algorithm Description
The look-and-say transformation works as follows:
- Take a string of digits
- Identify each consecutive run of the same digit
- Replace each run with: [count of digits][the digit itself]

### Examples of Single Transformation
- `1` → `11` (one 1)
- `11` → `21` (two 1s)
- `21` → `1211` (one 2, one 1)
- `1211` → `111221` (one 1, one 2, two 1s)
- `111221` → `312211` (three 1s, two 2s, one 1)

## Input
- A string of digits: `1321131112`
- Number of iterations: 40

## Processing Requirements
1. Start with the input string
2. Apply the look-and-say transformation
3. Use the result as input for the next iteration
4. Repeat for a total of 40 iterations

## Output
- The **length** (number of characters) of the final string after 40 iterations
- Output should be a single integer

## Implementation Notes
- Process the string by scanning left to right
- Count consecutive identical digits
- Build the new string by appending count + digit for each run
- The sequence grows exponentially with each iteration
