# Problem Report: String Classification (Nice vs Naughty)

## Context
Santa needs to classify a list of strings as either "nice" or "naughty" using a new, improved model for determining string niceness.

## Objective
Count how many strings in the input satisfy ALL the criteria for being classified as "nice".

## Input
- A list of strings (one per line)
- Each string consists of lowercase letters only
- Input is provided in `input.md` (1000 strings total)

## Classification Rules

A string is classified as **"nice"** if it satisfies BOTH of the following conditions:

### Condition 1: Non-overlapping Pair
The string must contain a pair of any two letters that appears at least twice in the string **without overlapping**.

**Examples:**
- `xyxy` is valid (the pair `xy` appears twice without overlapping)
- `aabcdefgaa` is valid (the pair `aa` appears twice without overlapping)
- `aaa` is NOT valid for this condition alone (the pair `aa` overlaps with itself)

### Condition 2: Letter Repeat with One Between
The string must contain at least one letter which repeats with exactly one letter between them.

**Examples:**
- `xyx` is valid (letter `x` repeats with `y` between them)
- `abcdefeghi` is valid (letter `e` repeats with `f` between them: `efe`)
- `aaa` is valid (letter `a` repeats with `a` between them)

## Test Cases

### Nice Strings:
1. `qjhvhtzxzqqjkmpb` - Has pair `qj` appearing twice AND has `zxz` (z repeats with x between)
2. `xxyxx` - Has pair `xx` appearing twice AND has `xyx` (x repeats with y between)

### Naughty Strings:
1. `uurcxstgmygtbstg` - Has pair `tg` appearing twice BUT no letter repeats with one between
2. `ieodomkazucvgmuy` - Has `odo` (letter repeats with one between) BUT no pair appears twice

## Expected Output
A single integer representing the total count of "nice" strings in the input.

## Output Format
The answer should be a single number (integer) representing the count of nice strings.
