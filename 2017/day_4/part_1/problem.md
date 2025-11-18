# Problem Report: High-Entropy Passphrase Validation

## Context
A new system security policy requires all accounts to use passphrases instead of passwords. This system needs validation to ensure passphrases meet security requirements.

## Objective
Count how many passphrases in the given input list are valid according to the security policy.

## Input Specification
- The input is a list of passphrases, one per line
- Each passphrase consists of a series of words (lowercase letters) separated by spaces
- Example input format:
  ```
  aa bb cc dd ee
  aa bb cc dd aa
  aa bb cc dd aaa
  ```

## Validation Rules
A valid passphrase must contain **no duplicate words**.

### Examples:
- `aa bb cc dd ee` → **VALID** (all words are unique)
- `aa bb cc dd aa` → **INVALID** (the word "aa" appears twice)
- `aa bb cc dd aaa` → **VALID** ("aa" and "aaa" are different words)

## Output Specification
- Output should be a single integer representing the total count of valid passphrases
- Format: Just the number (e.g., `477`)

## Algorithm Requirements
For each passphrase in the input:
1. Split the passphrase into individual words
2. Check if any word appears more than once
3. If no duplicates exist, count the passphrase as valid
4. Return the total count of valid passphrases
