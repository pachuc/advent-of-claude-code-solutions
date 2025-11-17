# Problem Report: String Literal Character Count

## Context
Santa needs to calculate how much storage space his list will take when stored digitally. The list contains string literals with escape sequences, and we need to understand the difference between the code representation and the actual in-memory representation.

## Objective
Calculate the difference between:
1. The number of characters in the **code representation** of string literals (raw text)
2. The number of characters in the **in-memory representation** (parsed/interpreted values)

## Input Format
- A file containing multiple lines
- Each line contains one double-quoted string literal
- Whitespace should be disregarded

## Escape Sequences to Handle
The following escape sequences may appear in the strings:

1. `\\` - Represents a single backslash character
2. `\"` - Represents a single double-quote character
3. `\x##` - Represents a single character where ## are two hexadecimal digits (e.g., `\x27` represents an apostrophe)

## Examples

| String Literal | Code Characters | Memory Characters | Explanation |
|---------------|-----------------|-------------------|-------------|
| `""` | 2 | 0 | Two quotes, empty string |
| `"abc"` | 5 | 3 | Two quotes + 3 letters = 5 code chars; just "abc" = 3 memory chars |
| `"aaa\"aaa"` | 10 | 7 | Contains escaped quote; 6 'a's + 1 quote char = 7 memory chars |
| `"\x27"` | 6 | 1 | Hex escape sequence for apostrophe; counts as 1 char in memory |

**Example Calculation:**
- Total code characters: 2 + 5 + 10 + 6 = 23
- Total memory characters: 0 + 3 + 7 + 1 = 11
- **Answer: 23 - 11 = 12**

## Expected Output
A single integer representing:
```
(sum of all code characters) - (sum of all memory characters)
```

## Algorithm Requirements
For each line in the input:
1. Count the total number of characters in the raw string literal (code representation)
2. Parse the string literal and count the actual characters it represents in memory:
   - Don't count the surrounding double quotes
   - `\\` counts as 1 character
   - `\"` counts as 1 character
   - `\x##` counts as 1 character
   - All other characters count as 1 character each
3. Sum up the differences across all lines
