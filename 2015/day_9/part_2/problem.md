# Problem Report: Traveling Salesman Problem - Finding Longest Route

## Objective
Find the **longest possible route** that visits each location exactly once. This is a variation of the classic Traveling Salesman Problem (TSP), where instead of finding the shortest route, we need to find the longest route.

## Context
Santa wants to travel between various locations, visiting each location exactly once. He can start and end at any two different locations. The goal is to determine the maximum total distance he can travel while satisfying these constraints.

## Input Format
The input consists of distance measurements between pairs of locations, formatted as:
```
Location1 to Location2 = Distance
```

Each line represents a bidirectional connection (the distance from Location1 to Location2 is the same as from Location2 to Location1).

### Example from input.md:
- Faerun to Norrath = 129
- Faerun to Tristram = 58
- AlphaCentauri to Snowdin = 12
- etc.

The input represents a complete graph where every location is connected to every other location with a specific distance.

## Constraints
1. Visit each location **exactly once** (Hamiltonian path problem)
2. Can start at any location
3. Can end at any location (different from the start)
4. Each distance can only be traversed once in the route

## Expected Output
A single integer representing the **total distance of the longest possible route**.

### Example
Given a simplified set of distances:
- Dublin to London = 464
- London to Belfast = 518
- Dublin to Belfast = 141

The longest route would be: Dublin -> London -> Belfast = 464 + 518 = **982**

## Algorithm Requirements
1. Parse the input to extract all unique locations and their pairwise distances
2. Generate all possible permutations of visiting the locations (all possible routes)
3. For each route, calculate the total distance
4. Return the maximum total distance found

## Notes
- This is a "maximization" variant of TSP (as opposed to the typical minimization)
- With N locations, there are (N-1)!/2 unique routes to consider (accounting for bidirectional paths)
- The problem is NP-hard, but for small inputs (like the one provided with 8 locations), brute force enumeration is feasible
