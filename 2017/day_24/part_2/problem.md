# Problem Report: Electromagnetic Moat Bridge Builder - Part 2

## Part 1 Context
In Part 1, we built a bridge from magnetic components to cross a bottomless pit. Each component has two ports with different pin counts (e.g., `3/7`). Components connect when their port types match. The bridge must start with a port of type `0`. The strength of a bridge is the sum of all pin counts in all components used.

**Part 1 Goal**: Find the maximum strength bridge possible.
**Part 1 Answer**: 1656

## Part 2 Objective
The strongest bridge from Part 1 isn't long enough. Now we need to find the **longest** bridge possible, and if there are multiple bridges of the same longest length, pick the **strongest** one among those longest bridges.

## Change from Part 1
- **Part 1**: Maximize strength (no consideration for length)
- **Part 2**: Maximize length first, then maximize strength among bridges of that maximum length

## Input Format
Same as Part 1:
- A list of components, one per line
- Each component is represented as `A/B` where A and B are the number of pins on each of the two ports
- Example:
  ```
  0/2
  2/2
  2/3
  3/4
  ```

## Rules and Constraints
Same as Part 1:

1. **Starting Port**: The bridge must start with a port of type `0`

2. **Component Connection**:
   - Each component has two ports (represented as `A/B`)
   - Components can only connect if they have matching port types
   - The order within a component doesn't matter (`3/7` can connect its `3` port or its `7` port)
   - Each component can only be used once in a bridge

3. **Building the Bridge**:
   - Start with any component that has a port of type `0`
   - The next component must have a port matching the unused port of the previous component
   - Continue chaining components where the free port of the current end matches a port on an unused component
   - A bridge can be as short as one component or use all available components

4. **Bridge Strength Calculation**:
   - The strength is the sum of all pin counts in all components used
   - For a component `A/B`, add both A and B to the strength

5. **Bridge Length**:
   - The length of a bridge is the number of components used in it

## Expected Output
A single integer representing the strength of the longest bridge. If multiple bridges tie for the longest length, output the strength of the strongest one among those.

## Example

Given components:
```
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
```

The two longest bridges both have length 4:
- `0/2`--`2/2`--`2/3`--`3/4` with strength = (0+2) + (2+2) + (2+3) + (3+4) = 18
- `0/2`--`2/2`--`2/3`--`3/5` with strength = (0+2) + (2+2) + (2+3) + (3+5) = 19

The answer is **19** (the strongest among the longest bridges).

## Algorithm Approach Needed
Modify the Part 1 approach to track both length and strength:
1. During DFS exploration, track both the length (number of components) and strength of each bridge
2. Keep track of the maximum length found
3. Among all bridges with the maximum length, find the one with maximum strength
4. Return the strength of that bridge
