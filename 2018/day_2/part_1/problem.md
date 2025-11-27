# Problem Report: Inventory Management System Checksum

## Context
We need to validate a list of box IDs by calculating a checksum. This checksum helps verify that we haven't missed any boxes during our scan.

## Objective
Calculate a checksum value based on the characteristics of box ID strings.

## Input
- A list of box IDs (strings)
- Each box ID is a string containing lowercase letters
- The input file contains one box ID per line

## Algorithm Requirements

For each box ID in the list:
1. Count the frequency of each letter in the box ID
2. Determine if ANY letter appears exactly 2 times (if yes, count this box toward the "twos" total)
3. Determine if ANY letter appears exactly 3 times (if yes, count this box toward the "threes" total)
4. Important: Each box ID can count toward both "twos" and "threes" if it has letters meeting both criteria
5. Important: Each box ID counts at most ONCE for "twos" (even if multiple letters appear exactly twice)
6. Important: Each box ID counts at most ONCE for "threes" (even if multiple letters appear exactly three times)

After processing all box IDs:
- Multiply the total count of box IDs with "twos" by the total count of box IDs with "threes"
- This product is the checksum

## Expected Output
A single integer representing the checksum value.

## Example Walkthrough

Given these box IDs:
- `abcdef` - no letter appears exactly 2 or 3 times → counts for neither
- `bababc` - has two 'a' AND three 'b' → counts for both twos and threes
- `abbcde` - has two 'b' → counts for twos only
- `abcccd` - has three 'c' → counts for threes only
- `aabcdd` - has two 'a' AND two 'd' → counts for twos once (not twice!)
- `abcdee` - has two 'e' → counts for twos only
- `ababab` - has three 'a' AND three 'b' → counts for threes once (not twice!)

Results:
- Box IDs with exactly two of any letter: 4 (bababc, abbcde, aabcdd, abcdee)
- Box IDs with exactly three of any letter: 3 (bababc, abcccd, ababab)
- Checksum: 4 × 3 = 12

## Output Format
The output should be a single integer with no additional formatting or text.
