# Problem Report: Traveling Salesman Problem (TSP) - Shortest Route

## Context
Santa needs to visit multiple locations in a single night. He has been given distances between every pair of locations. The goal is to help him find the most efficient route.

## Objective
Find the **shortest distance** Santa can travel to visit all locations exactly once. He can start and end at any two different locations.

## Input Format
The input consists of distance specifications between pairs of locations in the format:
```
Location1 to Location2 = distance
```

Each line represents a bidirectional distance (the distance from Location1 to Location2 is the same as from Location2 to Location1).

**Example Input:**
```
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
```

**Actual Input:**
The input file contains 28 distance specifications between 8 locations:
- Faerun
- Norrath
- Tristram
- AlphaCentauri
- Arbre
- Snowdin
- Tambi
- Straylight

## Constraints
1. Each location must be visited **exactly once**
2. Santa can start at **any location**
3. Santa can end at **any location** (different from the start)
4. The distances are bidirectional (symmetric)

## Expected Output
A single integer representing the minimum total distance for a route that visits all locations exactly once.

**Example Output:**
For the example with 3 locations (London, Dublin, Belfast), the answer is `605` because the shortest route is London -> Dublin -> Belfast = 464 + 141 = 605.

## Problem Type
This is a classic Traveling Salesman Problem (TSP) variant where:
- We need to find a Hamiltonian path (not a cycle, since start and end can be different)
- We're looking for the minimum total distance
- With N locations, there are N! / 2 unique paths to consider (divided by 2 due to bidirectionality)

## Algorithm Approach
Since the number of locations is small (8 in the actual input), a brute-force approach generating all permutations of routes is feasible:
1. Parse the input to build a distance graph/matrix
2. Generate all possible permutations of locations
3. Calculate the total distance for each permutation
4. Return the minimum distance found
