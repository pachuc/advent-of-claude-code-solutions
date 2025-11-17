# Problem Report: Password Generation Algorithm

## Objective
Generate the next valid password based on a given current password by incrementing it according to specific rules until all validation criteria are met.

## Context
Santa needs a new password after his previous one expired. To help him remember it, the new password is derived by incrementing the old password repeatedly until a valid password is found according to corporate security policy.

## Input
- A single string representing the current password
- The password is exactly 8 lowercase letters (a-z)
- Example input: `vzbxkghb`

## Password Incrementing Rules
Passwords increment like counting in base-26:
- Start from the rightmost letter and increment it by one position in the alphabet
- If a letter is 'z', it wraps around to 'a' and carries over to the next letter to the left
- Examples of incrementing: `xx` → `xy` → `xz` → `ya` → `yb`

## Password Validation Requirements
A valid password must satisfy ALL three requirements:

### Requirement 1: Increasing Straight
- Must contain at least one sequence of three consecutive letters in alphabetical order
- Valid examples: `abc`, `bcd`, `cde`, ..., `xyz`
- Letters must be consecutive in the alphabet (no skipping)
- Invalid example: `abd` (skips 'c')

### Requirement 2: Forbidden Characters
- Must NOT contain the letters `i`, `o`, or `l`
- These are excluded because they can be mistaken for other characters

### Requirement 3: Two Non-Overlapping Pairs
- Must contain at least two different, non-overlapping pairs of identical letters
- Valid pairs: `aa`, `bb`, `cc`, ..., `zz`
- The pairs must be non-overlapping (e.g., `aaa` counts as only one pair)
- The pairs must be different letters (e.g., `aa` and `bb`, not `aa` and `aa`)

## Algorithm
1. Start with the given password
2. Increment the password according to the incrementing rules
3. Check if the password meets all three validation requirements
4. If valid, this is the answer
5. If not valid, repeat from step 2

## Expected Output
- A single string: the next valid password after the input password
- The output should be exactly 8 lowercase letters
- Format: plain text string with no additional formatting

## Examples
- Input: `abcdefgh` → Output: `abcdffaa`
- Input: `ghijklmn` → Output: `ghjaabcc`
  - (Skips passwords starting with `ghi...` because `i` is forbidden)

## Notes
- `hijklmmn` has the straight `hij` but contains forbidden letters `i` and `l` (invalid)
- `abbceffg` has pairs `bb` and `ff` but no increasing straight (invalid)
- `abbcegjk` only has one pair `bb`, needs two different pairs (invalid)
