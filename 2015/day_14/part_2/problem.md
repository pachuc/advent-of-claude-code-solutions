# Problem Report: Reindeer Racing with Point-Based Scoring

## Objective
Calculate the winning reindeer's point total after 2503 seconds using a new scoring system where points are awarded each second to the reindeer currently in the lead.

## Context
This is a reindeer racing simulation where reindeer move in bursts (fly for a period, then rest for a period, repeating). Instead of determining the winner by distance traveled, the new scoring system awards 1 point per second to whichever reindeer is currently in the lead position (furthest distance). If multiple reindeer are tied for the lead, they each get 1 point.

## Input Format
The input consists of multiple lines, each describing one reindeer's characteristics:
- Format: `{Name} can fly {speed} km/s for {fly_time} seconds, but then must rest for {rest_time} seconds.`
- Each reindeer has three properties:
  - **Speed**: km/s traveled while flying
  - **Fly time**: consecutive seconds the reindeer can fly before resting
  - **Rest time**: consecutive seconds the reindeer must rest after flying

Example input lines:
```
Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds.
Cupid can fly 22 km/s for 2 seconds, but then must rest for 41 seconds.
```

## Simulation Requirements

### Movement Pattern
Each reindeer follows a repeating cycle:
1. Fly at their speed for their fly_time duration
2. Rest (0 km/s) for their rest_time duration
3. Repeat

### Scoring System
- At the end of each second (after positions are updated), award 1 point to the reindeer(s) currently in the lead
- If multiple reindeer are tied for the lead distance, each tied reindeer gets 1 point
- Continue for exactly 2503 seconds

### Example
Given two reindeer:
- Dancer: 27 km/s for 5 seconds, rest 132 seconds
- Comet: 18 km/s for 6 seconds, rest 103 seconds

After 1000 seconds: Dancer has 689 points, Comet has 312 points (Dancer wins)

## Expected Output
A single integer representing the total points accumulated by the winning reindeer after exactly 2503 seconds.

## Key Considerations
1. Track each reindeer's position (distance) at every second
2. Track each reindeer's point total
3. Determine the lead reindeer(s) at each second
4. Award points accordingly
5. The answer is the maximum points any reindeer has after 2503 seconds
