# Problem Report: Signal Error Correction

## Context
Communications with Santa are being jammed, causing signal corruption. A repetition code protocol is being used where the same message is sent repeatedly. The repeated transmissions have been recorded but are corrupted. The task is to recover the original message using error correction.

## Objective
Decode the error-corrected message from a series of corrupted repeated transmissions.

## Algorithm
For each character position across all messages:
1. Count the frequency of each character that appears in that position
2. Select the **most frequent character** for that position
3. Combine all the most frequent characters to form the decoded message

## Input Format
- Multiple lines of equal-length strings (the corrupted message transmissions)
- Each line represents one corrupted transmission of the same message
- All lines have the same number of characters

## Example
Given these corrupted transmissions:
```
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
```

Analysis by column position:
- Position 0: 'e' is most common
- Position 1: 'a' is most common
- Position 2: 's' is most common
- Position 3: 't' is most common
- Position 4: 'e' is most common
- Position 5: 'r' is most common

Result: `easter`

## Expected Output
A single string representing the error-corrected message (lowercase letters).

## Input Data
The input file contains 598 lines of 8-character strings representing the corrupted transmissions.
