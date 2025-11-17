# Implementation Summary: Molecular Replacement Calibration

## Overview
Successfully implemented a solution to calculate the number of distinct molecules that can be generated from a starting medicine molecule by performing exactly one replacement using a set of replacement rules.

## Solution Approach

### Algorithm
The solution uses a straightforward approach with three main components:

1. **Input Parsing** (`parse_input` function)
   - Reads the input file and dynamically locates the blank line separator
   - Parses replacement rules in the format "SOURCE => REPLACEMENT"
   - Extracts the medicine molecule string
   - Returns a list of rule tuples and the medicine string

2. **Pattern Finding** (`find_all_occurrences` function)
   - Searches for all occurrences of a pattern in the medicine string
   - Uses a sliding window approach to check each position
   - Handles overlapping patterns correctly (e.g., "HH" in "HHH" finds positions [0, 1])
   - Returns a list of starting indices where the pattern occurs

3. **Molecule Generation** (`solve` function)
   - For each replacement rule, finds all positions where the source pattern appears
   - For each position, generates a new molecule by replacing only that specific occurrence
   - Uses a Python set to automatically track distinct molecules (handles duplicates)
   - Returns the count of distinct molecules

### Key Design Decisions
- **Set-based deduplication**: Using a Python set automatically handles duplicate molecules without requiring manual checking
- **String slicing for replacement**: `medicine[:pos] + replacement + medicine[pos+len(source):]` cleanly performs the replacement at a specific position
- **Dynamic parsing**: The blank line separator is found dynamically rather than hard-coding line numbers, making the solution more robust
- **Simple iteration**: No need for complex optimization given the input size (~43 rules, ~468 character molecule)

## Implementation Details

### Files Created
- **solution.py**: Main solution file containing all functions and the entry point
- **test_example.txt**: Test file with the HOH example from the problem statement

### Code Structure
The solution is organized into three functions:
1. `parse_input(filename)` - Input parsing
2. `find_all_occurrences(text, pattern)` - Pattern matching
3. `solve(input_file)` - Main solution logic

### Complexity Analysis
- **Time Complexity**: O(R × M × L)
  - R = number of rules (43)
  - M = medicine length (468)
  - L = average replacement length (~5-10)
  - Total: approximately 200,000 operations
- **Space Complexity**: O(D × M) where D is the number of distinct molecules (509)
- **Actual Runtime**: < 0.1 seconds (very fast)

## Testing Process

### Unit Tests
Tested the `find_all_occurrences` function with various cases:
- ✅ Overlapping patterns: "HH" in "HHH" → [0, 1]
- ✅ Multiple non-overlapping: "AB" in "ABABAB" → [0, 2, 4]
- ✅ Single characters: "H" in "HOHOHO" → [0, 2, 4]
- ✅ Pattern not found: "XY" in "ABCDEF" → []

All unit tests passed successfully.

### Integration Test - Example Case
Tested with the HOH example from the problem statement:
- Input: Rules (H=>HO, H=>OH, O=>HH) and molecule "HOH"
- Expected output: 4 distinct molecules
- **Result: PASSED** ✅

Detailed trace showed correct generation:
- HOOH (from two different replacements, correctly counted once)
- HOHO
- OHOH
- HHHH

### Full Input Test
Ran the solution with the actual input file:
- **Answer: 509 distinct molecules**
- Validation checks:
  - ✅ 43 rules parsed correctly
  - ✅ Medicine molecule is 468 characters
  - ✅ 627 total replacement operations performed
  - ✅ 509 distinct molecules generated (81.2% unique rate)
  - ✅ 118 duplicates correctly handled
  - ✅ Output is reasonable (between number of rules and theoretical maximum)

### Edge Cases Verified
The solution correctly handles:
- Overlapping patterns (critical for accurate counting)
- Multiple rules for the same source pattern
- Duplicate molecules from different replacements
- Patterns at the start/end of the molecule
- Single character patterns
- Long replacement strings

## Results

### Final Answer
**509 distinct molecules**

### Statistics
- Total rules: 43
- Medicine length: 468 characters
- Total replacements performed: 627
- Distinct molecules: 509
- Duplicates eliminated: 118
- Unique molecule rate: 81.2%

## Conclusion
The solution successfully solves the molecular replacement calibration problem. The implementation is clean, efficient, and thoroughly tested. All tests passed, including the critical example case validation, giving high confidence in the correctness of the final answer.

The straightforward algorithm performs well for the given input size and correctly handles all edge cases including overlapping patterns and duplicate molecule detection.
