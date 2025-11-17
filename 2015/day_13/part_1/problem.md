# Problem Report: Optimal Circular Seating Arrangement

## Objective
Find the optimal seating arrangement for a group of people around a circular table that maximizes the total happiness change.

## Context
We have a list of people attending a dinner. Each person has preferences about sitting next to others, expressed as happiness units (positive for gain, negative for loss). Since the table is circular, each person will have exactly two neighbors. We need to find the arrangement that produces the maximum total happiness.

## Input Format
The input consists of lines following this pattern:
```
<Person1> would <gain|lose> <number> happiness units by sitting next to <Person2>.
```

Where:
- `<Person1>` is the name of a person
- `<gain|lose>` indicates whether happiness increases or decreases
- `<number>` is the magnitude of the happiness change (always positive integer)
- `<Person2>` is the name of another person

**Important Notes:**
- Happiness changes are directional (Person A sitting next to Person B has a different value than Person B sitting next to Person A)
- Both directions are provided in the input
- When two people sit next to each other, BOTH of their happiness changes apply to the total

## Algorithm Requirements
1. Parse all happiness relationships from the input
2. Generate all possible seating arrangements around a circular table
3. For each arrangement:
   - Calculate the total happiness by summing:
     - Each person's happiness from their left neighbor
     - Each person's happiness from their right neighbor
   - Remember: In a circular arrangement, the first and last person are also neighbors
4. Find and return the arrangement with the maximum total happiness

## Calculation Example
Given arrangement: Alice - David - Carol - Bob (circular)
- Alice next to David: Alice loses 2, David gains 46 = -2 + 46 = 44
- David next to Carol: David gains 41, Carol gains 55 = 41 + 55 = 96
- Carol next to Bob: Carol gains 60, Bob loses 7 = 60 - 7 = 53
- Bob next to Alice: Bob gains 83, Alice gains 54 = 83 + 54 = 137
- **Total: 44 + 96 + 53 + 137 = 330**

## Expected Output
A single integer representing the maximum total happiness change possible across all seating arrangements.

## Implementation Considerations
- This is a variant of the Traveling Salesman Problem (TSP) for circular arrangements
- Due to circular symmetry, you can fix one person's position to reduce redundant permutations
- The number of unique arrangements for N people is (N-1)!/2
- With 8 people in the actual input, there are 2,520 unique arrangements to check
- Use parsing to extract person names, gain/lose indicator, and numerical values
- Store relationships in a data structure (e.g., map/dictionary) for efficient lookup
