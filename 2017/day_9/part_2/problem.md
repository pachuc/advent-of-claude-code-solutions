# Problem Report: Stream Processing - Part 2 (Garbage Character Count)

## Context from Part 1

In Part 1, we parsed a stream of characters containing nested groups (delimited by `{` and `}`) and garbage (delimited by `<` and `>`). We calculated a score based on the nesting depth of all groups, while properly handling:
- **Groups**: Nested structures starting with `{` and ending with `}`
- **Garbage**: Content between `<` and `>` that should be ignored
- **Cancellation**: The `!` character inside garbage cancels the next character, including `<`, `>`, or another `!`

Part 1's answer was: **23588** (the total score of all groups)

## Part 2 Objective

Count the total number of non-canceled characters **within the garbage** sections of the stream.

## What Changed from Part 1

Instead of scoring groups, we now need to:
1. Identify all garbage sections (content between `<` and `>`)
2. Count only the characters inside the garbage (not the `<` and `>` delimiters themselves)
3. Exclude any canceled characters and the `!` doing the canceling

## Input Format

- Same as Part 1: A single line of text containing a character stream
- The stream consists of groups (delimited by `{` and `}`) and garbage (delimited by `<` and `>`)

## Parsing Rules (Same as Part 1)

### Garbage
- Garbage starts with `<` and ends with `>`
- The leading `<` and trailing `>` **do not count** toward the character count
- Between `<` and `>`, almost any character can appear

### Cancellation
- Inside garbage, the `!` character cancels the next character
- Both the `!` and the canceled character **do not count** toward the character count
- Any character following `!` is ignored, including `<`, `>`, or another `!`

### Groups
- Groups (`{` and `}`) are still present but **not relevant** for Part 2
- We only care about counting characters inside garbage sections

## Expected Output

A single integer representing the total count of non-canceled characters within all garbage sections.

## Examples

### Garbage Character Counting Examples

- `<>` → **0** characters (empty garbage)
- `<random characters>` → **17** characters (count all letters, spaces, etc.)
- `<<<<>` → **3** characters (three `<` characters before the closing `>`)
- `<{!>}>` → **2** characters (the `{` and `}` count; the `>` after `!` is canceled and doesn't count)
- `<!!>` → **0** characters (the second `!` is canceled by the first `!`, then the `>` closes)
- `<!!!>>` → **0** characters (second `!` cancels third `!`, first `>` is canceled, second `>` closes)
- `<{o"i!a,<{i<a>` → **10** characters (counts: `{`, `o`, `"`, `i`, `,`, `<`, `{`, `i`, `<`, `a`)

Note: In the last example, `!a` represents the `!` canceling the `a`, so neither counts.

## Algorithm Approach

1. Iterate through the character stream one character at a time
2. Track whether we are currently inside garbage (between `<` and `>`)
3. When we encounter `<` (outside garbage), enter garbage mode but don't count it
4. When inside garbage:
   - If we encounter `!`, skip both the `!` and the next character (don't count either)
   - If we encounter `>`, exit garbage mode (don't count the `>`)
   - Otherwise, count the character
5. Return the total count of characters inside garbage

## Key Differences from Part 1

- **Part 1**: Calculated scores based on group nesting depth
- **Part 2**: Counts characters inside garbage sections
- **Part 1**: Groups were important, garbage was ignored
- **Part 2**: Garbage is important, groups are irrelevant
