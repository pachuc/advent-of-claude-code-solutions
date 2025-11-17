# Problem Report: Modified Repetition Code Decoding (Part 2)

## Context from Part 1
In Part 1, communications with Santa were being jammed, causing signal corruption. A repetition code protocol was being used where the same message is sent repeatedly. The task was to recover the original message by finding the **most frequent character** at each position across all transmissions. This yielded the answer `qzedlxso`.

## Part 2: Modified Repetition Code
It turns out a **modified repetition code** was actually being used. In this modified protocol, the sender transmits what looks like random data, but for each character position, the character they actually want to send is **slightly less likely** than the others. Even with signal-jamming noise, the original message can be reconstructed by choosing the **least common character** at each position.

## Objective
Decode the original message from the same set of corrupted repeated transmissions, but using the modified decoding methodology: selecting the **least frequent character** at each position instead of the most frequent.

## Algorithm Change
For each character position across all messages:
1. Count the frequency of each character that appears in that position
2. Select the **least frequent character** for that position (this is the key difference from Part 1)
3. Combine all the least frequent characters to form the decoded message

## Input Format
- Multiple lines of equal-length strings (the corrupted message transmissions)
- Each line represents one corrupted transmission of the same message
- All lines have the same number of characters
- The input is the same 598 lines of 8-character strings used in Part 1

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

Analysis by column position (using **least common** instead of most common):
- Position 0: 'a' is least common
- Position 1: 'd' is least common
- Position 2: 'v' is least common
- Position 3: 'e' is least common
- Position 4: 'n' is least common
- Position 5: 't' is least common

Result: `advent`

(Note: In Part 1, the same input yielded `easter` using most common characters)

## Expected Output
A single string representing the decoded original message (lowercase letters).

## Key Difference from Part 1
- **Part 1**: Used `Counter.most_common(1)[0][0]` to get the most frequent character
- **Part 2**: Must use the least frequent character instead (e.g., `Counter.most_common()[-1][0]` or similar approach)
