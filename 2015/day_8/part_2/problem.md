# Problem Report: String Encoding

## Objective
Calculate the total number of additional characters needed when encoding string literals according to specific escaping rules.

## Context
We need to encode string literals (which are already escaped) into a new representation where the encoded string itself becomes a valid string literal. This is essentially "re-escaping" strings - taking strings that contain escape sequences and creating new strings that represent those original strings as literals.

## Input
- A file containing multiple lines, where each line is a string literal enclosed in double quotes
- String literals may contain:
  - Regular ASCII characters
  - Escape sequences like `\"` (escaped quote)
  - Escape sequences like `\\` (escaped backslash)
  - Hexadecimal escape sequences like `\x27` (hex character codes)

## Encoding Rules
When encoding a string literal, we need to:
1. Wrap the entire string in double quotes
2. Escape any double quotes inside the string by adding a backslash before them
3. Escape any backslashes inside the string by adding another backslash before them
4. The result is a new string literal that represents the original string

## Examples of Encoding

| Original String | Original Length | Encoded String | Encoded Length | Difference |
|----------------|-----------------|----------------|----------------|------------|
| `""` | 2 | `"\"\""` | 6 | +4 |
| `"abc"` | 5 | `"\"abc\""` | 9 | +4 |
| `"aaa\"aaa"` | 10 | `"\"aaa\\\"aaa\""` | 16 | +6 |
| `"\x27"` | 6 | `"\"\\x27\""` | 11 | +5 |

## Expected Output
A single integer representing the total difference between:
- The sum of all encoded string lengths (after encoding)
- The sum of all original string lengths (as written in the input file)

In other words: `(total encoded length) - (total original code length)`

## Algorithm Steps
1. Read each line from the input file
2. For each string literal:
   - Count its original length (number of characters in the code representation)
   - Encode it according to the rules (escape `"` and `\` characters, wrap in quotes)
   - Count the encoded length
   - Calculate the difference
3. Sum all the differences
4. Output the total as a single integer
