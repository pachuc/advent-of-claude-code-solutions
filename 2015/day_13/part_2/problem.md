# Problem Report: Optimal Seating Arrangement with Self Included

## Problem Overview
We need to find the optimal seating arrangement around a circular table that maximizes the total happiness change, with the constraint that we (the solver) must be included in the seating arrangement.

## Context
This is a seating optimization problem where guests have preferences about who they sit next to. Each person has a happiness value (positive or negative) associated with sitting next to each other person. The total happiness for a seating arrangement is calculated by summing up all the individual happiness changes for each pair of adjacent seats.

Since the table is circular, each person has exactly two neighbors (one on each side).

## Important Constraint
**We must add ourselves to the guest list.** Our happiness relationships with all other guests are **0** (neutral). This means:
- We gain/lose 0 happiness units sitting next to anyone
- Everyone else gains/loses 0 happiness units sitting next to us

## Input Format
The input consists of multiple lines, each describing a directed happiness relationship in the format:

```
[Person A] would [gain/lose] [X] happiness units by sitting next to [Person B].
```

Where:
- `[Person A]` is the person whose happiness is being described
- `[gain/lose]` indicates whether the value is positive or negative
- `[X]` is the magnitude of the happiness change (always a positive integer in the input)
- `[Person B]` is the neighbor person

**Key Details:**
- Happiness relationships are **directed** (asymmetric): Person A's happiness from sitting next to Person B may differ from Person B's happiness from sitting next to Person A
- Both directions must be considered when calculating total happiness
- The seating is circular, so everyone has exactly 2 neighbors

## Expected Output
A single integer representing the **maximum possible total change in happiness** for the optimal seating arrangement that includes yourself.

## Calculation Method
For each seating arrangement:
1. For each person, calculate their happiness based on both neighbors (left and right)
2. Sum all individual happiness values to get the total happiness for that arrangement
3. Find the arrangement that produces the maximum total happiness

## Example Calculation
If Alice sits between Bob and Carol:
- Alice's contribution = (Alice's happiness with Bob) + (Alice's happiness with Carol)
- Bob's contribution includes: (Bob's happiness with Alice)
- Carol's contribution includes: (Carol's happiness with Alice)

The total for the entire table is the sum of all such contributions.

## Additional Notes
- This is a circular seating problem, so rotations of the same arrangement are equivalent
- The problem requires finding the optimal permutation of guests (including yourself) around a circular table
- All guests from the input must be seated, plus yourself
