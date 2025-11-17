# Problem Report: Reindeer Race Simulation

## Objective
Simulate a race between reindeer to determine which reindeer travels the farthest distance after exactly 2503 seconds.

## Context
We are simulating the Reindeer Olympics where reindeer race by alternating between flying at their top speed and resting to recover energy. Each reindeer has different flight characteristics (speed, flight duration, and rest duration). We need to calculate the total distance each reindeer travels and identify the winner.

## Reindeer Behavior Model
- Reindeer can only be in one of two states: **flying** or **resting**
- When flying, a reindeer always flies at its top speed (constant km/s)
- When resting, a reindeer does not move at all (0 km/s)
- Reindeer always spend whole seconds in either state
- Each reindeer follows a cycle:
  1. Fly at top speed for a specified number of seconds
  2. Rest for a specified number of seconds
  3. Repeat this cycle

## Input Format
The input consists of multiple lines, where each line describes one reindeer with the following format:

```
[Name] can fly [speed] km/s for [fly_time] seconds, but then must rest for [rest_time] seconds.
```

Where:
- `[Name]`: The name of the reindeer (string)
- `[speed]`: The flying speed in km/s (integer)
- `[fly_time]`: The number of seconds the reindeer can fly before needing to rest (integer)
- `[rest_time]`: The number of seconds the reindeer must rest before it can fly again (integer)

### Example Input
```
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
```

## Calculation Details

### Race Duration
The race lasts exactly **2503 seconds**.

### Distance Calculation
For each reindeer, calculate the total distance traveled after 2503 seconds by:
1. Determining at each second whether the reindeer is flying or resting based on its cycle
2. If flying: add (speed × 1 second) to the total distance
3. If resting: add 0 to the total distance
4. Continue for all 2503 seconds

### Example Calculation
Using the example reindeer after 1000 seconds:
- **Comet** (14 km/s for 10s, rest for 127s):
  - Cycle length: 10 + 127 = 137 seconds
  - After 1000 seconds: travels **1120 km**
- **Dancer** (16 km/s for 11s, rest for 162s):
  - Cycle length: 11 + 162 = 173 seconds
  - After 1000 seconds: travels **1056 km**
- **Winner**: Comet with 1120 km

## Expected Output
A single integer representing the distance (in kilometers) that the winning reindeer has traveled after exactly 2503 seconds.

The output should be the maximum distance among all reindeer.
