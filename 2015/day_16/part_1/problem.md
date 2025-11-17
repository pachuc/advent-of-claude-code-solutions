# Problem Report: Aunt Sue Identification

## Context
You received a gift from one of your 500 aunts named Sue. Using a "My First Crime Scene Analysis Machine" (MFCSAM), you analyzed the gift wrapping and obtained a compound signature. You need to identify which Aunt Sue sent the gift by matching this signature against your memory of each aunt's characteristics.

## Objective
Determine which Aunt Sue (numbered 1-500) gave you the gift by matching the MFCSAM analysis results against known characteristics of each aunt.

## Input Data

### MFCSAM Analysis Results (Target Signature)
The gift wrapping analysis produced the following compound counts:
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

### Aunt Sue Records
The input file contains 500 lines, one for each Aunt Sue, with the format:
```
Sue N: compound1: count1, compound2: count2, compound3: count3
```

Each aunt has exactly 3 remembered characteristics. The remaining characteristics are unknown (not zero - simply not remembered).

**Example entries:**
```
Sue 1: goldfish: 9, cars: 0, samoyeds: 9
Sue 2: perfumes: 5, trees: 8, goldfish: 8
Sue 3: pomeranians: 2, akitas: 1, trees: 5
```

## Matching Rules
To identify the correct Aunt Sue:
1. For each aunt, compare the remembered characteristics against the MFCSAM target signature
2. The remembered characteristics must ALL match the corresponding values in the target signature
3. Characteristics that are not remembered (not listed for that aunt) should be ignored - they are neither matches nor mismatches
4. The correct Aunt Sue is the one where all remembered characteristics exactly match the target signature

## Expected Output
The output should be a single number: the ID number (1-500) of the Aunt Sue who gave you the gift.

**Format:** Just the number (e.g., `213`)
