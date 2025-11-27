# Problem Report: Optimized Polymer Reaction (Part 2)

## Objective
Find the shortest possible polymer length by removing all instances of one problematic unit type, then fully reacting the resulting polymer.

## Background Context from Part 1
We are working with a polymer composed of units that react with each other. The polymer undergoes a reduction process where adjacent units of the same type but opposite polarity destroy each other. This process continues until no more reactions are possible.

**Part 1 Result:** The original polymer, when fully reacted without any removals, produces a length of 11546 units.

## Part 2 Enhancement
One of the unit types is preventing the polymer from collapsing as much as it should. We need to:
1. Try removing all instances of each possible unit type (both uppercase and lowercase)
2. Fully react the remaining polymer for each removal
3. Find which unit type removal produces the shortest polymer
4. Return the length of that shortest polymer

## Input Specification
- A single string representing a polymer
- The string consists of alphabetic characters (both uppercase and lowercase)
- The input will be read from `input.md`
- The input is very large (approximately 50,000 characters)

## Reaction Rules (Same as Part 1)
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
1. Identify all unique unit types in the polymer (ignoring case)
2. For each unit type (e.g., 'a', 'b', 'c', ...):
   - Remove all instances of that unit type (both 'a' and 'A', both 'b' and 'B', etc.)
   - Fully react the remaining polymer using the reaction algorithm from Part 1
   - Record the final length
3. Return the minimum length found across all unit type removals

## Example Walkthrough
Using the polymer `dabAcCaCBAcCcaDA`:

- **Removing all A/a units:** `dbcCCBcCcD` → fully reacts to `dbCBcD` (length 6)
- **Removing all B/b units:** `daAcCaCAcCcaDA` → fully reacts to `daCAcaDA` (length 8)
- **Removing all C/c units:** `dabAaBAaDA` → fully reacts to `daDA` (length 4)
- **Removing all D/d units:** `abAcCaCBAcCcaA` → fully reacts to `abCBAc` (length 6)

In this example, removing all C/c units produces the shortest polymer with length **4**.

## Expected Output
A single integer representing the length of the shortest polymer achievable by removing all instances of exactly one unit type and fully reacting the result.

## Implementation Notes
- You can reuse the reaction algorithm from Part 1
- Need to test removing each of the 26 possible unit types (A-Z, case-insensitive)
- For each test, remove both uppercase and lowercase versions of the unit
- The algorithm should handle very large inputs efficiently (50,000+ characters)
- You only need to test unit types that actually exist in the polymer (optimization)
