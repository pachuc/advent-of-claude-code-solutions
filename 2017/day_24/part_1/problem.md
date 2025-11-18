# Problem Report: Electromagnetic Moat Bridge Builder

## Objective
Find the maximum strength of a valid bridge that can be built from a set of components.

## Problem Context
We need to build a bridge by connecting magnetic components. Each component can only be used once, and components must connect via matching port types.

## Input Format
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

1. **Starting Port**: The bridge must start with a port of type `0` (zero pins)

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
   - Example: Bridge `0/3`--`3/7`--`7/4` has strength = (0+3) + (3+7) + (7+4) = 24

## Expected Output
A single integer representing the maximum possible strength of any valid bridge that can be constructed from the available components.

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

The strongest valid bridge is: `0/1`--`10/1`--`9/10`
- Strength = (0+1) + (1+10) + (10+9) = 31

## Algorithm Approach Needed
This is a graph traversal/path-finding problem where we need to:
1. Start from components with a `0` port
2. Recursively/iteratively explore all possible valid bridges
3. Track which components have been used (each can only be used once)
4. Calculate the strength of each complete bridge
5. Return the maximum strength found
