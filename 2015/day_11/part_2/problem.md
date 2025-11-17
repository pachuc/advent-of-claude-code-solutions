# Problem Report: Santa's Password Generator (Part 2)

## Context
Santa's password has expired again. This is Part 2 of a two-part puzzle.

**Part 1 Summary:**
- Started with password: `vzbxkghb`
- Found the next valid password: `vzbxxyzz`

**Part 2 Task:**
- Santa's password (`vzbxxyzz`) has now expired again
- We need to find the next valid password after `vzbxxyzz`
- This is essentially finding the second valid password in the sequence

## Objective
Generate the next valid password after the current password by incrementing it until all validation rules are satisfied.

## Input
- The original input file contains: `vzbxkghb` (the starting password from Part 1)
- However, for Part 2, we use the Part 1 answer as our starting point: `vzbxxyzz`
- We need to find the next valid password after `vzbxxyzz`

## Password Rules
A valid password must satisfy ALL of the following requirements:

1. **Increasing Straight Requirement**: Must contain at least one sequence of three consecutive increasing letters (e.g., `abc`, `bcd`, `cde`, ..., `xyz`)
   - The letters must be consecutive in the alphabet with no gaps
   - Example: `abc` is valid, but `abd` is not (skips 'c')

2. **Forbidden Characters**: Must NOT contain the letters `i`, `o`, or `l`
   - These letters can be mistaken for other characters and are confusing
   - Any password containing these letters is invalid

3. **Pair Requirement**: Must contain at least two different, non-overlapping pairs of identical letters
   - Examples of valid pairs: `aa`, `bb`, `zz`
   - The two pairs must be different letters (e.g., `aa` and `bb` is valid, but `aa` and `aa` overlapping is not)
   - The pairs cannot overlap

## Password Incrementing Logic
Passwords increment like base-26 numbers using lowercase letters:
- Start from the rightmost letter
- Increment it by one position in the alphabet
- If the letter is `z`, wrap it to `a` and carry over to the next letter to the left
- Repeat until a letter doesn't wrap around

Examples:
- `xx` → `xy` → `xz` → `ya` → `yb`
- `azz` → `baa`

## Validation Examples
- `hijklmmn`: INVALID - contains forbidden letters `i` and `l` (even though it has the straight `hij` and pair `mm`)
- `abbceffg`: INVALID - lacks an increasing straight (even though it has pairs `bb` and `ff`)
- `abbcegjk`: INVALID - only has one pair `bb`, needs at least two different pairs
- `abcdefgh` → next valid: `abcdffaa`
- `ghijklmn` → next valid: `ghjaabcc` (skips passwords with `i`)

## Expected Output
A single string of exactly 8 lowercase letters representing the next valid password after `vzbxxyzz`.

## Algorithm Overview
1. Start with the Part 1 answer: `vzbxxyzz`
2. Increment the password using the incrementing rules
3. Check if the new password meets all three validation rules
4. If valid, return it as the answer
5. If not valid, repeat from step 2

Note: You can reuse the exact same algorithm from Part 1, just start from `vzbxxyzz` instead of the original input.

## Important Notes
- The password must be incremented at least once (we're looking for the NEXT password, not validating the current one)
- All three rules must be satisfied simultaneously
- The incrementing process should continue until a valid password is found
