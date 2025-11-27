# Implementation Plan - Part 2: Last Cart Standing

## Overview
Modify the Part 1 solution to handle cart collision removal and find the last remaining cart instead of finding the first collision.

## Core Algorithm Changes

### 1. Cart State Management
**Objective:** Track which carts are still active vs removed

**Implementation:**
- Add a `removed` boolean attribute to the `Cart` class (default `False`)
- When collision detected, mark both involved carts as `removed = True`
- Filter out removed carts from movement processing

**Reuse from Part 1:** The entire `Cart` class structure, just add one attribute

### 2. Modified Collision Detection
**Objective:** Remove both carts on collision and continue simulation

**Changes to Part 1 logic:**
- In the simulation loop, after moving each cart, check for collisions
- When collision detected between cart `i` and cart `j`:
  - Mark both `carts[i].removed = True` and `carts[j].removed = True`
  - Continue simulation (don't return immediately)
- **Important:** Skip carts that are already removed when iterating

**Key Implementation Details:**
- During each tick's movement phase:
  - Sort all carts (including removed ones for index stability)
  - Iterate through cart indices
  - Skip the cart if `carts[i].removed == True`
  - After moving cart `i`, check collisions with ALL other carts
  - If collision found, mark BOTH carts as removed immediately
  - Continue to next cart (skip any cart that's now marked removed)

### 3. Termination Condition
**Objective:** Stop when only one cart remains

**Implementation:**
- After each complete tick (all carts have moved):
  - Count active carts: `active = [c for c in carts if not c.removed]`
  - If `len(active) == 1`: return position of that cart
  - If `len(active) == 0`: error condition (shouldn't happen)

**Return Format:** Same as Part 1: `X,Y` format

### 4. Modified Simulation Loop
**Objective:** Continuous simulation with cart removal

**Algorithm Structure:**
```python
def simulate(track, carts):
    while True:
        # Sort all carts (including removed) for consistent ordering
        # Note: We keep removed carts in the list to maintain stable indices
        carts.sort(key=lambda c: (c.y, c.x))

        # Track positions where collisions occurred this tick
        # This handles multi-cart pile-ups correctly
        collision_positions = set()

        # Move each cart in order
        for i in range(len(carts)):
            # Skip if this cart was already removed
            if carts[i].removed:
                continue

            # Move the cart
            move_cart(carts[i], track)

            # Get current position
            pos = (carts[i].x, carts[i].y)

            # Check if this cart landed on a position where a collision happened this tick
            # This handles 3+ cart pile-ups: if Cart A and B collided at (5,5),
            # and Cart C later moves to (5,5), Cart C should also be removed
            if pos in collision_positions:
                carts[i].removed = True
                continue

            # Check for collisions with other active carts
            for j in range(len(carts)):
                if i != j and not carts[j].removed:
                    if carts[i].x == carts[j].x and carts[i].y == carts[j].y:
                        # Collision! Remove both carts and mark position
                        carts[i].removed = True
                        carts[j].removed = True
                        collision_positions.add(pos)
                        break  # Stop checking, this cart is removed

        # Check termination condition
        active_carts = [c for c in carts if not c.removed]
        if len(active_carts) == 1:
            return (active_carts[0].x, active_carts[0].y)
        elif len(active_carts) == 0:
            raise Exception("No carts remaining!")
```

**Key Implementation Details:**
- **Collision positions tracking**: The `collision_positions` set tracks where collisions occurred during the current tick
- **Set lifecycle**: The set is created fresh at the start of each tick and discarded at the end. Collision positions from previous ticks are not tracked
- **Multi-cart pile-ups**: If Cart A and Cart B collide at position (5,5), the position is added to `collision_positions`. If Cart C later moves to (5,5) in the same tick, it's also marked as removed
- **Stable indices**: We never delete carts from the list, only mark them as removed, so indices remain stable throughout iteration
- **Collision timing**: Collisions are detected immediately after each cart moves, not at the end of the tick
- **Why this works**: When a cart moves and collides, both carts are marked removed AND the position is added to collision_positions. Any subsequent cart moving to that position in the same tick will see the position in the set and be removed, even though the original colliding carts are already marked removed

## Components to Reuse from Part 1

**100% Reusable (no changes needed):**
1. `parse_input()` - Track and cart parsing
2. `turn_left()` - Direction transformation
3. `turn_right()` - Direction transformation
4. `apply_curve()` - Curve handling
5. `get_direction_delta()` - Movement deltas
6. `move_cart()` - Individual cart movement logic
7. All direction and track handling logic

**Needs Modification:**
1. `Cart.__init__()` - Add `self.removed = False`
2. `simulate()` - Complete rewrite per algorithm above
3. `solve()` - Change to match new return format (though format is same)

## Step-by-Step Implementation

### Step 1: Update Cart Class
- Add `self.removed = False` in `Cart.__init__()`

### Step 2: Rewrite simulate() Function
- Implement the new simulation loop as described above
- Handle cart removal on collision
- Check for single cart remaining after each tick
- Return the position of the last cart

### Step 3: Update solve() Function
- Call the new `simulate()` function
- Return format remains `X,Y` (same as Part 1)

### Step 4: Test with Sample Input
- Verify collision removal works correctly
- Verify simulation continues after collisions
- Verify correct cart remains at the end

## Edge Cases to Handle

1. **Multiple simultaneous collisions in one tick**: Each collision should be detected independently and all involved carts removed
2. **Cart collides with already-removed cart**: Should not happen if we skip removed carts correctly
3. **Moving cart collides with stationary cart that hasn't moved yet this tick**: Collision should be detected immediately after the moving cart's move
4. **Multi-cart pile-up** (3+ carts converge on same position):
   - Example: Cart A moves to (5,5), Cart B is already at (5,5) → both removed, position marked
   - Then Cart C moves to (5,5) → Cart C should also be removed (handled by collision_positions set)
   - All carts reaching a collision position in the same tick are removed
5. **All carts collide (even number scenario)**: Should raise "No carts remaining!" exception
6. **Last two carts collide**: Should raise "No carts remaining!" exception

## Performance Considerations

- **Time Complexity:** O(T × C²) where T is number of ticks and C is cart count
  - Since C decreases over time (carts removed), average case is better
  - For ~17 carts and track size ~150×150, this is very fast

- **Space Complexity:** O(W × H + C) for track grid and cart list
  - No additional space needed beyond Part 1

- **Optimization:** Could maintain active cart list separately, but unnecessary for this input size

## File Structure

**Input:** `input.md` (same as Part 1)

**Output:** `X,Y` coordinates of last remaining cart

**Main script:** `solution.py` - adapted from `part_1_solution.py`

## Critical Implementation Notes

### Addressing Multi-Cart Pile-Ups

The most critical aspect of this implementation is correctly handling scenarios where 3+ carts converge on the same position during one tick:

**Problem Scenario:**
1. Cart A at (4,5) moves right to (5,5)
2. Cart B at (5,5) hasn't moved yet
3. A and B collide → both marked removed
4. Cart C at (6,5) moves left to (5,5)
5. **Without collision_positions**: Cart C would NOT be detected as colliding (A and B are removed)
6. **With collision_positions**: Cart C sees (5,5) in the set and is correctly removed

**Solution:**
- Maintain a `collision_positions` set for each tick
- When two carts collide, add their position to the set
- Before checking cart-to-cart collisions, check if position is in the set
- This ensures ALL carts reaching a collision position are removed

This mechanism is essential for correctness and differentiates a correct solution from a buggy one.
