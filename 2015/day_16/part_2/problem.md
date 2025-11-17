# Problem Report: Finding the Real Aunt Sue (Part 2)

## Context
You have 500 aunts named Sue, and you need to identify which one gave you a gift. You've analyzed the gift wrapping using the My First Crime Scene Analysis Machine (MFCSAM), which detected specific compounds and their quantities.

## The MFCSAM Reading (Target Values)
The MFCSAM analysis of the gift wrapping produced these results:
- children: 3
- cats: 7
- samoyeds: 2
- pomeranians: 3
- akitas: 0
- vizslas: 0
- goldfish: 5
- trees: 3
- cars: 2
- perfumes: 1

## Important: Part 2 Modification - Outdated Retroencabulator
The MFCSAM has an outdated retroencabulator, so the output values are not always exact. Some readings indicate **ranges** rather than exact values:

### Special Matching Rules:
1. **cats** and **trees**: The actual values must be **GREATER THAN** the MFCSAM reading
   - Due to unpredictable nuclear decay of cat dander and tree pollen
   - cats: actual value must be > 7
   - trees: actual value must be > 3

2. **pomeranians** and **goldfish**: The actual values must be **FEWER THAN** the MFCSAM reading
   - Due to modial interaction of magnetoreluctance
   - pomeranians: actual value must be < 3
   - goldfish: actual value must be < 5

3. **All other compounds** (children, samoyeds, akitas, vizslas, cars, perfumes): Must match **exactly**

## Input Format
The input consists of 500 lines, one for each Aunt Sue (numbered 1-500). Each line has the format:
```
Sue N: compound1: value1, compound2: value2, compound3: value3
```

Each Aunt Sue has exactly 3 compounds listed. The compounds not listed are unknown (not zero, just not remembered).

### Example Input Lines:
```
Sue 1: goldfish: 9, cars: 0, samoyeds: 9
Sue 2: perfumes: 5, trees: 8, goldfish: 8
Sue 3: pomeranians: 2, akitas: 1, trees: 5
```

## Task
Find which Aunt Sue matches the MFCSAM reading, considering:
1. The special range-based matching rules for cats, trees, pomeranians, and goldfish
2. Exact matching for all other compounds
3. Unknown/unlisted compounds should not disqualify a match (they are ignored)

An Aunt Sue is a match if:
- For every compound she has listed, it matches the MFCSAM reading according to the appropriate rule
- All unlisted compounds are ignored (treated as unknown)

## Expected Output
Output the **number** of the Aunt Sue who matches the MFCSAM reading with the Part 2 rules applied.

The output should be a single integer representing Sue's number (between 1 and 500).
