# Problem Report: Finding Prototype Fabric Box IDs (Part 2)

## Context from Part 1

In Part 1, we validated a list of box IDs from a warehouse by calculating a checksum. We counted how many box IDs had letters appearing exactly twice and exactly three times, then multiplied these counts together. The checksum we calculated was 6200, confirming our list of box IDs is complete.

## Part 2 Objective

Now that we have confirmed our complete list of box IDs, we need to find the two specific boxes that contain the prototype fabric. These two boxes have IDs that differ by **exactly one character at the same position**.

## Input

- The same list of box IDs from Part 1 (strings, one per line in input.md)
- Each box ID is a string of lowercase letters
- All box IDs have the same length

## Algorithm Requirements

1. Compare pairs of box IDs to find two IDs that differ by exactly one character at the same position
2. "Differ by exactly one character" means:
   - All positions must have the same character EXCEPT for exactly one position
   - The differing position must be at the same index in both strings
   - The length of both strings must be the same

3. Once the two matching box IDs are found, extract the common letters by removing the one differing character

## Expected Output

A string containing only the common letters between the two correct box IDs (with the differing character removed).

## Example Walkthrough

Given these box IDs:
```
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
```

Analysis:
- `abcde` vs `axcye`: differ at positions 1 (b vs x) and 3 (d vs y) → 2 differences, not a match
- `fghij` vs `fguij`: differ only at position 2 (h vs u) → exactly 1 difference, THIS IS THE MATCH!

Output: Remove the differing character from either ID:
- `fghij` with position 2 removed = `fgij`
- `fguij` with position 2 removed = `fgij`

Result: `fgij`

## Output Format

The output should be a single string with no additional formatting, newlines, or text - just the common letters.
