# Implementation Plan: Reindeer Racing Point System

## Overview
Simulate a 2503-second reindeer race where points are awarded each second to the reindeer(s) currently in the lead position. The goal is to find the maximum points accumulated by any reindeer.

## Algorithm Analysis

### Time Complexity
- **O(N × T)** where N = number of reindeer (9) and T = time duration (2503 seconds)
- Each second requires updating all reindeer positions and finding the leader(s)
- Total operations: ~22,500 (very manageable)

### Space Complexity
- **O(N)** for storing reindeer data structures
- We need to track: name, speed, fly_time, rest_time, current_distance, points, cycle_position

### Algorithm Choice
**Iterative Simulation** is the optimal approach:
- Direct second-by-second simulation is efficient for T=2503
- Alternative approaches (mathematical formulas) would be complex due to point-awarding logic
- The scoring system requires knowing relative positions at each timestep

## Implementation Steps

### Step 1: Input Parsing
**Goal**: Extract reindeer characteristics from input text

**Approach**:
- Read input file line by line
- Use regex to parse the pattern: `{Name} can fly {speed} km/s for {fly_time} seconds, but then must rest for {rest_time} seconds.`
- Create a data structure for each reindeer

**Data Structure**:
```python
reindeer = {
    'name': str,
    'speed': int,          # km/s
    'fly_time': int,       # seconds
    'rest_time': int,      # seconds
    'distance': int,       # current position (km)
    'points': int,         # accumulated points
    'cycle_time': int,     # position within fly-rest cycle
    'is_flying': bool      # current state
}
```

**Regex Pattern**: `(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.`

### Step 2: Initialize Simulation State
**Goal**: Set up initial state for all reindeer

**Actions**:
- Set distance = 0 for all reindeer
- Set points = 0 for all reindeer
- Set time_in_state = 0 for all reindeer
- Set is_flying = True for all reindeer

**IMPORTANT TIMING CLARIFICATION**:
- At t=0 (initial state): all reindeer are at position 0, ready to fly
- During second 1: reindeer move for the first time
- After second 1: positions are updated, then points are awarded
- The simulation loop runs from second 1 to second 2503 inclusive

### Step 3: Implement Position Update Logic
**Goal**: Calculate each reindeer's position at each second

**IMPORTANT**: Use the state machine approach from Step 7 below. The modulo approach shown here is for conceptual understanding only.

**Conceptual Algorithm (DO NOT USE)**:
```
For each reindeer at each second:
1. Determine current state (flying or resting)
   - cycle_position = current_second % (fly_time + rest_time)
   - if cycle_position < fly_time: flying
   - else: resting

2. Update distance:
   - if flying: distance += speed
   - if resting: distance += 0
```

**Why Not Use This**: The state machine approach (Step 7) is more efficient and clearer

### Step 4: Implement Leader Detection
**Goal**: Determine which reindeer(s) are in the lead each second

**Algorithm**:
```
1. Find max_distance = max(all reindeer distances)
2. Find all reindeer where distance == max_distance
3. Return list of leaders (could be multiple if tied)
```

**Efficiency**: O(N) scan through reindeer list

### Step 5: Implement Point Awarding
**Goal**: Award 1 point to each leading reindeer

**Algorithm**:
```
For each leader in leaders_list:
    leader.points += 1
```

### Step 6: Main Simulation Loop
**Goal**: Orchestrate the complete 2503-second simulation

**CRITICAL TIMING**: Per the problem statement, "at the end of each second (after positions are updated), award points"

**Algorithm**:
```python
for second in range(1, 2504):  # 1 to 2503 inclusive
    # FIRST: Update all reindeer positions (movement happens DURING the second)
    for reindeer in reindeer_list:
        update_position(reindeer)

    # SECOND: Find leader(s) (determine who is ahead AFTER movement)
    leaders = find_leaders(reindeer_list)

    # THIRD: Award points (points awarded AT THE END of the second)
    for leader in leaders:
        leader.points += 1

# Return maximum points
return max(r.points for r in reindeer_list)
```

**Timing Summary**:
1. Movement happens during the second
2. Leaders are determined after movement
3. Points are awarded at the end of the second

### Step 7: Efficient State Tracking (Optimization)
**Goal**: Track reindeer state without repeated modulo operations

**Improved Data Structure**:
```python
reindeer = {
    'name': str,
    'speed': int,
    'fly_time': int,
    'rest_time': int,
    'distance': int,
    'points': int,
    'time_in_state': int,  # seconds spent in current state
    'is_flying': bool       # True if flying, False if resting
}
```

**State Update Logic** (USE THIS APPROACH):
```python
def update_reindeer(reindeer):
    # time_in_state tracks seconds COMPLETED in current state
    if reindeer['is_flying']:
        # Move forward while flying
        reindeer['distance'] += reindeer['speed']
        reindeer['time_in_state'] += 1

        # Check if we've completed the flying period
        if reindeer['time_in_state'] >= reindeer['fly_time']:
            # Transition to resting
            reindeer['is_flying'] = False
            reindeer['time_in_state'] = 0
    else:  # resting
        # No movement while resting (distance stays the same)
        reindeer['time_in_state'] += 1

        # Check if we've completed the resting period
        if reindeer['time_in_state'] >= reindeer['rest_time']:
            # Transition to flying
            reindeer['is_flying'] = True
            reindeer['time_in_state'] = 0
```

**Why This Approach**:
- More efficient than modulo calculations each second
- Clearer state management with explicit transitions
- time_in_state counts seconds completed, making transition logic clear

## Code Structure

### Functions to Implement:

1. **`parse_input(filename: str) -> List[Dict]`**
   - Read file and parse each line
   - Return list of reindeer dictionaries

2. **`initialize_reindeer(parsed_data: List[tuple]) -> List[Dict]`**
   - Create reindeer data structures with initial state
   - Return list of initialized reindeer

3. **`update_reindeer_position(reindeer: Dict) -> None`**
   - Update single reindeer's position and state
   - Mutates reindeer dictionary in place

4. **`find_leaders(reindeer_list: List[Dict]) -> List[Dict]`**
   - Find all reindeer with maximum distance
   - Return list of leader reindeer

5. **`simulate_race(reindeer_list: List[Dict], duration: int) -> int`**
   - Main simulation loop
   - Return maximum points achieved

6. **`main()`**
   - Orchestrate the overall solution
   - Read input, run simulation, print result

## Pseudocode

```
FUNCTION main():
    reindeer_data = parse_input("input.md")
    reindeer_list = initialize_reindeer(reindeer_data)
    max_points = simulate_race(reindeer_list, 2503)
    PRINT max_points

FUNCTION parse_input(filename):
    reindeer_data = []
    FOR each line in file:
        MATCH line with regex
        EXTRACT name, speed, fly_time, rest_time
        APPEND (name, speed, fly_time, rest_time) to reindeer_data
    RETURN reindeer_data

FUNCTION initialize_reindeer(parsed_data):
    reindeer_list = []
    FOR each (name, speed, fly_time, rest_time) in parsed_data:
        CREATE reindeer dict with:
            name, speed, fly_time, rest_time
            distance = 0
            points = 0
            time_in_state = 0
            is_flying = True
        APPEND reindeer to reindeer_list
    RETURN reindeer_list

FUNCTION update_reindeer_position(reindeer):
    IF reindeer.is_flying:
        reindeer.distance += reindeer.speed
        reindeer.time_in_state += 1
        IF reindeer.time_in_state >= reindeer.fly_time:
            reindeer.is_flying = False
            reindeer.time_in_state = 0
    ELSE:
        reindeer.time_in_state += 1
        IF reindeer.time_in_state >= reindeer.rest_time:
            reindeer.is_flying = True
            reindeer.time_in_state = 0

FUNCTION find_leaders(reindeer_list):
    max_distance = MAX(r.distance FOR r in reindeer_list)
    leaders = [r FOR r in reindeer_list IF r.distance == max_distance]
    RETURN leaders

FUNCTION simulate_race(reindeer_list, duration):
    FOR second FROM 1 TO duration:
        FOR each reindeer in reindeer_list:
            update_reindeer_position(reindeer)

        leaders = find_leaders(reindeer_list)

        FOR each leader in leaders:
            leader.points += 1

    max_points = MAX(r.points FOR r in reindeer_list)
    RETURN max_points
```

## Implementation Notes

### Edge Cases Handled:
1. **Multiple leaders**: When reindeer tie for distance, all get points
2. **Cycle transitions**: Proper state tracking when switching between fly/rest
3. **Initial state**: All reindeer start in flying state at time 0

### Validation Checkpoints:
1. Verify parsing extracts all 9 reindeer correctly
2. Check that distance calculations match expected values at sample times
3. Confirm point totals align with example (Dancer: 689 points at 1000s)

### Performance Considerations:
- Total operations: 9 reindeer × 2503 seconds × 2 operations ≈ 45,000 ops
- Memory: 9 dictionaries with ~8 fields each (negligible)
- Runtime: Expected < 100ms for this input size

## File Structure
```
solution.py          # Main implementation
input.md             # Problem input (9 reindeer)
problem.md           # Problem description
```

## Expected Output
A single integer representing the winning reindeer's point total after 2503 seconds.
