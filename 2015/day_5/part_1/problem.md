# Problem Report: String Classification (Nice vs Naughty)

## Objective
Determine how many strings in a given text file meet the criteria for being classified as "nice" strings.

## Context
Santa needs help analyzing strings in his text file to determine which ones are "nice" versus "naughty" based on specific character pattern rules.

## Input
- A text file containing strings, one per line
- Each string consists of lowercase letters (a-z)
- The input file contains 1000 strings

## Classification Rules

A string is classified as **"nice"** if it meets ALL of the following criteria:

### 1. Vowel Count Requirement
- Must contain at least 3 vowels
- Only these characters count as vowels: `a`, `e`, `i`, `o`, `u`
- The same vowel can be counted multiple times

### 2. Double Letter Requirement
- Must contain at least one letter that appears twice in a row (consecutive identical characters)
- Examples: `xx`, `aa`, `bb`, `dd`

### 3. Forbidden Substring Requirement
- Must NOT contain any of these substrings: `ab`, `cd`, `pq`, `xy`
- Even if these substrings would satisfy other requirements, their presence makes the string naughty

## Examples

### Nice Strings:
- `ugknbfddgicrmopn` - has 3+ vowels (`u`, `i`, `o`), has double letter (`dd`), no forbidden substrings
- `aaa` - has 3+ vowels (three `a`s), has double letter (`aa`), no forbidden substrings

### Naughty Strings:
- `jchzalrnumimnmhp` - fails because it has no double letter (even though it has enough vowels)
- `haegwjzuvuyypxyu` - fails because it contains forbidden substring `xy`
- `dvszwmarrgswjxmb` - fails because it only has 1 vowel (needs at least 3)

## Expected Output
- A single integer representing the count of "nice" strings in the input file
- Format: Just the number (e.g., `255`)

## Algorithm Requirements
1. Read each string from the input file
2. For each string, check all three criteria:
   - Count vowels (a, e, i, o, u) - must be >= 3
   - Check for at least one pair of consecutive identical characters
   - Check that none of the forbidden substrings (ab, cd, pq, xy) appear
3. If all three criteria are met, count the string as "nice"
4. Return the total count of nice strings
