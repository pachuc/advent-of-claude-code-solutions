# Problem Report: Molecular Replacement Calibration

## Context
We need to calibrate a molecular replacement machine that can transform molecules through single-step replacements. The machine works by taking an input molecule and applying replacement rules to generate new molecules. The calibration process requires determining how many distinct molecules can be generated in exactly one replacement step from a starting molecule.

## Objective
Calculate the number of **distinct molecules** that can be created by performing exactly **one replacement** on a given medicine molecule using a set of replacement rules.

## Input Format
The input consists of two parts:

1. **Replacement Rules** (lines 1-43): A list of molecular replacement rules in the format:
   - `SOURCE => REPLACEMENT`
   - Each line defines a rule where a substring `SOURCE` can be replaced with `REPLACEMENT`
   - Multiple rules can have the same source element (e.g., multiple rules for "H")

2. **Medicine Molecule** (line 45): A single long string representing the starting molecule that needs to be processed

The two sections are separated by a blank line.

## Processing Rules
- Apply each replacement rule to **every possible position** where the source pattern appears in the medicine molecule
- Replacements are done **without regard for surrounding characters** (pattern matching is straightforward substring matching)
- Each replacement generates a new molecule
- Only perform **one replacement per generated molecule** (not chained replacements)
- The same molecule can be generated multiple ways, but should only be **counted once** (distinct molecules only)

## Example
Given rules:
```
H => HO
H => OH
O => HH
```

Starting with molecule `HOH`:
- First `H` can be replaced with `HO` → `HOOH`
- First `H` can be replaced with `OH` → `OHOH`
- Second `H` can be replaced with `HO` → `HOHO`
- Second `H` can be replaced with `OH` → `HOOH` (duplicate)
- Middle `O` can be replaced with `HH` → `HHHH`

Result: **4 distinct molecules** (HOOH, HOHO, OHOH, HHHH)

## Expected Output
A single integer representing the count of distinct molecules that can be generated after performing all possible single replacements on the medicine molecule.
