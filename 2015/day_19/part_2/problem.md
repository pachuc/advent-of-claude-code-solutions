# Problem Report: Molecule Fabrication

## Objective
Find the minimum number of steps required to fabricate a target medicine molecule starting from a single electron `e`, using a given set of replacement rules.

## Context
This is a molecule fabrication problem where we need to build a complex molecule by starting with a single electron and applying replacements iteratively. Each replacement rule allows us to substitute a specific substring with another substring in our current molecule string.

## Input Specification

The input consists of two parts:

1. **Replacement Rules**: A list of transformation rules in the format `source => target`
   - Each rule specifies that the substring `source` can be replaced with the substring `target`
   - Rules can be applied to any occurrence of the source pattern in the current molecule
   - Multiple rules may have the same source with different targets

2. **Target Molecule**: A single string representing the medicine molecule we need to fabricate
   - This is the final molecule we must reach starting from `e`

## Problem Details

- **Starting State**: Always begin with a single electron `e`
- **Goal**: Transform `e` into the target medicine molecule
- **Operations**: Apply replacement rules one at a time
  - Each step involves selecting one occurrence of a source pattern in the current molecule and replacing it with the corresponding target pattern
  - Only one replacement per step

## Example

Given the replacement rules:
```
e => H
e => O
H => HO
H => OH
O => HH
```

To make the molecule `HOH`:
1. Start with `e`
2. Apply `e => O` to get `O`
3. Apply `O => HH` to get `HH`
4. Apply `H => OH` (on the second H) to get `HOH`

This takes **3 steps**.

## Expected Output

A single integer representing the **minimum number of steps** required to transform `e` into the target medicine molecule using the provided replacement rules.

## Input Format

The input file contains:
- Lines 1-43: Replacement rules in the format `source => target`
- Line 44: Empty line (separator)
- Line 45: The target medicine molecule string

## Key Considerations

- This is a pathfinding/search problem where we need to find the shortest sequence of transformations
- The molecule strings consist of element symbols (like H, O, Ca, Si, Mg, etc.) and special structural markers (like Rn, Ar, Y)
- We need to work **forward** from `e` to the target molecule
- Multiple replacement rules may be applicable at each step, creating a branching search space
- The goal is to find the **minimum** number of steps, so this is an optimization problem
