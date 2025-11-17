# Implementation Plan: Air Duct Robot Pathfinding - Part 2 (Round Trip)

## Problem Summary
Find the minimum number of steps for a robot to start at location `0`, visit all numbered locations, and **return to location `0`**. This is a Traveling Salesman Problem with a required round trip.

## Key Difference from Part 1
Part 1: Find shortest path from `0` visiting all locations (can end anywhere)
Part 2: Find shortest path from `0` visiting all locations **and returning to `0`**

The Part 1 solution can be reused with a minimal modification to the final answer calculation.

## Implementation Steps

### Step 1: Reuse Part 1 Code Structure
**Action**: Copy the entire Part 1 solution as the foundation
**Rationale**: The grid parsing, BFS distance calculation, and TSP dynamic programming logic are identical

**File Operations**:
1. Copy `part_1_solution.py` to `solution.py` in the Part 2 directory
2. Modify only the `solve_tsp()` function as described in Step 2
3. Optionally update print statements for clarity

**Files to reuse**:
- `parse_grid()` - Identical functionality
- `calculate_distances()` - Identical functionality
- `solve_tsp()` - **Needs modification** (see Step 2)

### Step 2: Modify the TSP Solver for Round Trip
**Current Part 1 logic** (line 110-111 in part_1_solution.py):
```python
full_mask = (1 << N) - 1
return min(dp[full_mask][i] for i in range(N))
```

**New Part 2 logic**:
```python
full_mask = (1 << N) - 1
start_idx = location_mapping[start_location]
return min(dp[full_mask][i] + distances[i][start_idx] for i in range(N))
```

**Explanation**:
- `dp[full_mask][i]` = minimum distance to visit all locations ending at location `i`
- `distances[i][start_idx]` = distance from location `i` back to location `0`
- We try all possible final locations before returning to `0` and take the minimum

**Important Note**: The optimal visiting order for Part 2 may differ from Part 1. While Part 1 optimizes for ending anywhere, Part 2 optimizes for the round trip, which may result in visiting locations in a different sequence to minimize the total distance including the return journey.

**Implementation details**:
- Add the return distance `+ distances[i][start_idx]` to each candidate in the min calculation
- `start_idx` should be available from the function parameters (already is)
- No other changes to the DP logic are needed

### Step 3: Update Main Function (Optional)
**Action**: Update print statements to reflect Part 2 context
**Changes**:
- Update final print to say "Minimum steps required (round trip):" for clarity
- Consider adding a print showing the Part 1 answer vs Part 2 answer for comparison

### Step 4: Input Reading
**Action**: Reuse the existing input reading logic from Part 1
**File**: Read from `input.md` (same as Part 1)
**No changes needed** - grid format is identical

### Step 5: Testing Integration
**Action**: Ensure the solution outputs only the final answer
**Requirements**:
- Print the minimum steps as the final output
- Keep debug prints for development but ensure they're informative

## Algorithm Complexity Analysis

### Time Complexity
- **BFS distance calculation**: O(N × W × H) where N = number of locations, W×H = grid size
  - For the given input: ~7 locations × 43×173 grid ≈ 52,000 operations
- **TSP DP**: O(2^N × N^2)
  - For N=7: 2^7 × 49 = 6,272 states
  - For N=8: 2^8 × 64 = 16,384 states

**Total**: Dominated by TSP which is O(2^N × N^2)

### Space Complexity
- **DP table**: O(2^N × N)
- **Distance matrix**: O(N^2)
- **Grid storage**: O(W × H)

**Total**: O(2^N × N) dominated by DP table

### Expected Performance
- For N ≤ 10 locations: Solution should complete in < 1 second
- The given input appears to have 8 locations (0-7 based on input grid)
- Algorithm is efficient enough for this problem size

## Code Structure

```python
from collections import deque

def parse_grid(grid_lines):
    """Parse grid to find numbered locations - REUSE FROM PART 1"""
    # ... (identical to Part 1)

def calculate_distances(grid, locations):
    """Calculate BFS distances between locations - REUSE FROM PART 1"""
    # ... (identical to Part 1)

def solve_tsp(distances, location_mapping, start_location=0):
    """Solve TSP with ROUND TRIP - MODIFIED FROM PART 1"""
    N = len(distances)
    start_idx = location_mapping[start_location]

    # DP logic identical to Part 1
    dp = [[float('inf')] * N for _ in range(1 << N)]
    dp[1 << start_idx][start_idx] = 0

    for mask in range(1 << N):
        for current in range(N):
            if not (mask & (1 << current)) or dp[mask][current] == float('inf'):
                continue
            for next_loc in range(N):
                if not (mask & (1 << next_loc)):
                    new_mask = mask | (1 << next_loc)
                    dp[new_mask][next_loc] = min(
                        dp[new_mask][next_loc],
                        dp[mask][current] + distances[current][next_loc]
                    )

    # MODIFIED: Add return distance to start
    full_mask = (1 << N) - 1
    return min(dp[full_mask][i] + distances[i][start_idx] for i in range(N))

def main():
    """Main function - MOSTLY REUSE FROM PART 1"""
    # Read and parse input (identical)
    # Calculate distances (identical)
    # Solve TSP (modified function)
    # Print result
```

## Implementation Checklist

- [ ] Copy Part 1 solution functions
- [ ] Modify `solve_tsp()` return statement to add round-trip distance
- [ ] Update print messages for clarity (optional)
- [ ] Test with sample input if available
- [ ] Run on actual input
- [ ] Verify output format (single integer)

## Edge Cases Handled by Part 1 Code
These don't need additional handling:
- Empty grid validation
- Location 0 existence check
- Unreachable locations detection
- Single location (N=1) - would return 0 (correctly: start at 0, no other locations to visit, already at 0)
- All locations on same row/column

**Edge Case Verification for Round Trip**:
- **N=1 case**: If only location 0 exists, `dp[full_mask][0] + distances[0][0]` = `0 + 0` = `0` ✓
- The round-trip logic correctly handles this edge case without additional code

## Expected Output
A single integer representing the minimum steps for the round trip visiting all locations starting and ending at `0`.

**Expected Relationship to Part 1**:
- Part 1 answer: 428 steps (verified in `part_1_answer.txt`)
- Part 2 answer: Will be > 428 since we must return to start
- The difference represents the cost to return from the optimal ending location to location 0
- Note: Part 2's optimal path may visit locations in a different order than Part 1 to minimize the round-trip distance
