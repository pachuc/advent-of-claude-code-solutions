# Implementation Plan - Part 2: Finding Non-Overlapping Claim

## Problem Summary
Find the ID of the single claim that doesn't overlap with any other claim. We know from Part 1 that we have a working grid-based solution for tracking claim overlaps.

## High-Level Approach
Reuse the Part 1 grid approach with an additional check: after building the overlap grid, iterate through each claim and verify if ALL of its cells have a count of exactly 1 (meaning only that claim covers those cells).

## Algorithm Efficiency Analysis
- **Input Size**: 1,286 claims (based on input.md)
- **Grid Size**: At most ~1000x1000 = 1,000,000 cells (likely less based on actual claims)
- **Time Complexity**: O(N × A) where N = number of claims, A = average area per claim
  - Building grid: O(N × A) - mark each claim's cells
  - Checking claims: O(N × A) - verify each claim's cells
  - Overall: O(N × A) which is acceptable
- **Space Complexity**: O(W × H) for the grid, where W and H are fabric dimensions

This is efficient for the input size. Alternative approaches like checking every pair of claims would be O(N²) which is worse.

## Step-by-Step Implementation Plan

### Step 1: Reuse Part 1 Code Structure
- **Action**: Copy the core components from `part_1_solution.py`
- **Components to reuse**:
  - `Claim` namedtuple definition
  - `parse_claim()` function - parses claim format
  - `get_fabric_dimensions()` function - calculates required grid size
  - `create_fabric_grid()` function - initializes grid
  - `mark_claim_on_grid()` function - marks claims on grid
- **Rationale**: These functions are proven to work and handle the exact same input format

### Step 2: Build the Overlap Grid
- **Action**: Use the same grid-building logic from Part 1
- **Process**:
  1. Parse all claims from input.md
  2. Calculate fabric dimensions
  3. Create grid initialized to zeros
  4. For each claim, increment the counter for every cell it covers
- **Result**: Grid where each cell contains the count of how many claims cover it
- **Code reference**: `part_1_solution.py:82-108` (main function logic)

### Step 3: Implement Non-Overlapping Claim Checker
- **Action**: Create a new function `is_claim_non_overlapping(grid, claim)`
- **Logic**:
  ```
  For each cell (x, y) covered by the claim:
      If grid[y][x] != 1:
          return False  # This cell is shared or has multiple claims
  return True  # All cells are exclusively claimed by this claim
  ```
- **Edge Cases**:
  - Claim extends beyond grid bounds: Should not happen if grid dimensions are correctly calculated
  - All cells must be exactly 1 (not 0, not 2+)
- **Time Complexity**: O(claim.width × claim.height) per claim

### Step 4: Find the Non-Overlapping Claim
- **Action**: Iterate through all claims and check each one
- **Logic**:
  ```
  for claim in claims:
      if is_claim_non_overlapping(grid, claim):
          return claim.id
  ```
- **Assumptions**: Problem guarantees exactly one such claim exists (no error handling needed)
- **Return**: The claim ID (integer)
- **Note**: No need to handle "not found" case since problem guarantees exactly one non-overlapping claim

### Step 5: Main Function and Output
- **Action**: Update main() function
- **Process**:
  1. Read and parse input (reuse from Part 1)
  2. Build grid (reuse from Part 1)
  3. Mark all claims on grid (reuse from Part 1)
  4. Find non-overlapping claim (new logic from Step 4)
  5. Print the claim ID
- **Output Format**: Single integer (the claim ID)

### Step 6: Input/Output Handling
- **Input**: Read from `input.md` (same as Part 1)
- **Output**: Print result to stdout
- **No file writing needed**: Just print the answer

## Code Organization
```
part_2_solution.py:
- Imports (re, collections.namedtuple)
- Claim namedtuple
- parse_claim() - reused
- get_fabric_dimensions() - reused
- create_fabric_grid() - reused
- mark_claim_on_grid() - reused
- is_claim_non_overlapping() - NEW (checks if single claim is non-overlapping)
- main() - modified from Part 1 (includes loop to find non-overlapping claim)

Note: The find logic can be inlined in main() rather than creating a separate
find_non_overlapping_claim() function, since it's a simple loop.
```

## Testing Strategy Reference
The implementation should support the test cases defined in `test_plan.md`:
- Example case from problem (claims #1, #2, #3 → answer: 3)
- Actual input (1,286 claims)
- Edge cases for grid bounds verification

## Key Differences from Part 1
1. **Part 1**: Count cells with count >= 2
2. **Part 2**: Find claim where ALL cells have count == 1
3. **Part 1**: Returns integer count
4. **Part 2**: Returns claim ID

## Potential Pitfalls to Avoid
1. **Off-by-one errors**: Ensure cell iteration matches Part 1 (inclusive ranges)
2. **Grid indexing**: Remember grid[y][x] not grid[x][y]
3. **Early termination**: Can return as soon as we find the non-overlapping claim
4. **Empty input**: Assume input is valid based on problem statement
