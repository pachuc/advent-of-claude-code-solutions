# Problem Report: Polymer Reaction Simulation

## Objective
Calculate the length of a polymer string after all possible chemical reactions have completed.

## Background Context
We are simulating a polymer composed of units that can react with each other. The polymer undergoes a reduction process where adjacent units of the same type but opposite polarity destroy each other. This process continues until no more reactions are possible.

## Input Specification
- A single string representing a polymer
- The string consists of alphabetic characters (both uppercase and lowercase)
- The input will be read from `input.md`
- The input is very large (approximately 50,000 characters)

## Reaction Rules
Two adjacent units will react and be destroyed if and only if:
1. They are the same letter (same type)
2. They have opposite polarity (one uppercase, one lowercase)

Examples of reactive pairs:
- `a` and `A` react (same type, opposite polarity)
- `r` and `R` react (same type, opposite polarity)

Examples of non-reactive pairs:
- `a` and `B` do not react (different types)
- `a` and `b` do not react (different types)
- `a` and `a` do not react (same type, same polarity)
- `A` and `A` do not react (same type, same polarity)

## Processing Logic
1. Scan the polymer from left to right looking for adjacent units that can react
2. When a reactive pair is found, remove both units
3. Continue scanning and removing reactive pairs
4. The removal of one pair may create new adjacent pairs that can react
5. Repeat until no more reactions are possible

## Examples

### Example 1: `aA`
- `a` and `A` react, leaving nothing behind.
- Result: empty string (length 0)

### Example 2: `abBA`
- `bB` destroys itself, leaving `aA`
- `aA` then destroys itself, leaving nothing
- Result: empty string (length 0)

### Example 3: `abAB`
- No two adjacent units are of the same type
- Result: `abAB` (length 4)

### Example 4: `aabAAB`
- `aa` have same polarity, so no reaction
- `AA` have same polarity, so no reaction
- No reactions occur
- Result: `aabAAB` (length 6)

### Example 5: `dabAcCaCBAcCcaDA`
Step-by-step reduction:
1. `dabAcCaCBAcCcaDA` - First `cC` is removed
2. `dabAaCBAcCcaDA` - This creates `Aa`, which is removed
3. `dabCBAcCcaDA` - Either `cC` or `Cc` are removed
4. `dabCBAcaDA` - No further reactions possible

Result: `dabCBAcaDA` (length 10)

## Expected Output
A single integer representing the number of units remaining in the polymer after all possible reactions have completed.

## Implementation Notes
- The reaction process must continue until no more adjacent reactive pairs exist
- When units are removed, the units on either side become adjacent and may form a new reactive pair
- The algorithm should handle very large inputs efficiently (50,000+ characters)
