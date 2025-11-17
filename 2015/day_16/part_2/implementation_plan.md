# Implementation Plan: Finding the Real Aunt Sue (Part 2)

## Problem Summary
Find which of 500 Aunt Sues matches the MFCSAM reading, using special comparison rules for certain compounds due to an outdated retroencabulator.

## Differences from Part 1
**Part 1** used exact matching (==) for all compounds.

**Part 2** (this problem) introduces range-based comparisons for 4 specific compounds:
- **cats** and **trees**: Must be GREATER THAN (>) the target value
- **pomeranians** and **goldfish**: Must be LESS THAN (<) the target value
- All other compounds still use exact matching (==)

This change reflects the "outdated retroencabulator" producing range-based readings for some compounds.

## Target MFCSAM Values
```
children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0
vizslas: 0, goldfish: 5, trees: 3, cars: 2, perfumes: 1
```

## Matching Rules
1. **Greater than rules**: cats > 7, trees > 3
2. **Less than rules**: pomeranians < 3, goldfish < 5
3. **Exact match rules**: children, samoyeds, akitas, vizslas, cars, perfumes must equal exactly
4. **Unknown compounds**: If a compound is not listed for an Aunt Sue, ignore it (don't disqualify)

## Algorithm Design

### Approach
**Linear Search with Rule-Based Filtering** - O(n) time complexity where n = 500

This is optimal because:
- We must check every Aunt Sue at least once to find the match
- Each Sue has only 3 compounds to check (constant time per Sue)
- Total time: O(500 × 3) = O(1500) operations - trivial
- No need for complex data structures or optimization

### Step-by-Step Implementation

#### Step 1: Define Target Values and Rules
```python
# Store target MFCSAM values in a dictionary
target = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}

# Define which compounds use which comparison rules
greater_than_compounds = {'cats', 'trees'}
less_than_compounds = {'pomeranians', 'goldfish'}
# All others use exact match
```

#### Step 2: Parse Input File
```python
# Read input.md file line by line
# For each line like "Sue 1: goldfish: 9, cars: 0, samoyeds: 9"
# Extract:
#   - Sue number: 1
#   - Compounds: {'goldfish': 9, 'cars': 0, 'samoyeds': 9}

# Parsing approach:
# 1. Open and read input.md file
# 2. For each line, strip whitespace (including newlines)
# 3. Split on ":" to separate "Sue N" from compounds
# 4. Extract N from first part using split() and convert to int
# 5. Split remaining part on ", " to get individual compound:value pairs
# 6. For each pair, split on ": " to get compound name and value
# 7. Convert value to int (not string)
# 8. Store in dictionary: sue_number -> {compound: value, ...}

# Example parsing for "Sue 1: goldfish: 9, cars: 0, samoyeds: 9":
# - "Sue 1".split() -> ["Sue", "1"] -> int("1") = 1
# - "goldfish: 9, cars: 0, samoyeds: 9".split(", ")
#   -> ["goldfish: 9", "cars: 0", "samoyeds: 9"]
# - For each: "goldfish: 9".split(": ") -> ["goldfish", "9"] -> int("9") = 9
```

#### Step 3: Create Matching Function
```python
def matches_target(sue_compounds, target, greater_than, less_than):
    """
    Check if a Sue's compounds match the target according to rules.

    Args:
        sue_compounds: dict of {compound: value} for this Sue
        target: dict of target MFCSAM values
        greater_than: set of compounds that need > comparison
        less_than: set of compounds that need < comparison

    Returns:
        bool: True if all of Sue's compounds match, False otherwise
    """
    for compound, value in sue_compounds.items():
        target_value = target[compound]

        # Use positive logic for clarity
        if compound in greater_than:
            # For cats and trees, actual value must be GREATER THAN target
            if not (value > target_value):
                return False
        elif compound in less_than:
            # For pomeranians and goldfish, actual value must be LESS THAN target
            if not (value < target_value):
                return False
        else:  # exact match required
            if value != target_value:
                return False

    return True
```

#### Step 4: Iterate Through All Sues
```python
# For each Sue (1 to 500):
#   - Get her compounds dictionary
#   - Call matches_target()
#   - If returns True, this is the answer
#   - Return Sue's number

# Assumption: Problem guarantees exactly one Sue will match
# No need to handle cases of zero or multiple matches
```

#### Step 5: Output Result
```python
# Print the Sue number to stdout as a single integer (between 1 and 500)
print(matching_sue_number)
```

## File Structure
```
solution.py
├── Read input.md file
├── Parse all 500 Sues into data structure
├── Define target values and comparison rules
├── Implement matching function
├── Search for matching Sue
└── Output result
```

## Input Validation Assumptions
Since this is a scripting problem (not production code):
- **Assume input.md exists** and is readable
- **Assume input is well-formed**: 500 lines, valid format ("Sue N: compound: value, ...")
- **Assume exactly one Sue will match** (problem guarantees this)
- **Assume all compound names are valid** (no typos or unknown compounds)
- **No need for extensive validation** or error messages
- **Focus on correctness of matching logic** rather than defensive programming

## Complexity Analysis
- **Time Complexity**: O(n) where n = 500 Sues
  - Each Sue has exactly 3 compounds to check
  - Each compound check is O(1)
  - Total operations: 500 Sues × 3 compounds = 1500 comparisons (still O(n))
- **Space Complexity**: O(n) to store all Sues
  - Could optimize to O(1) by checking each Sue immediately after parsing
  - But with only 500 Sues, optimization is unnecessary

## Edge Cases Handled
1. **Unlisted compounds**: Ignored (not checked) ✓
2. **Boundary values**:
   - cats: must be > 7 (so 8+ matches)
   - trees: must be > 3 (so 4+ matches)
   - pomeranians: must be < 3 (so 0, 1, 2 match)
   - goldfish: must be < 5 (so 0, 1, 2, 3, 4 match)
3. **Exact matches**: All other compounds must equal exactly

## Implementation Notes
- Use Python's string parsing (split, strip)
- Regular expressions could be used but are overkill for this simple format
- Dictionary lookups provide clean, readable code
- Set membership tests are O(1) and efficient for rule checking
