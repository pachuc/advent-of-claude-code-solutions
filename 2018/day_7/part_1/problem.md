# Problem Report: Topological Sort with Alphabetical Ordering

## Context
We need to assemble a sleigh by completing a series of steps in the correct order. The steps have dependencies - certain steps must be completed before others can begin.

## Objective
Determine the correct order in which to complete all assembly steps, respecting all dependency constraints.

## Input Format
The input consists of multiple lines, each describing a dependency between two steps:
```
Step X must be finished before step Y can begin.
```

Where:
- `X` is a single letter representing a prerequisite step
- `Y` is a single letter representing a dependent step
- This means step `X` must be completed before step `Y` can start

## Constraints and Rules
1. Each step is represented by a single uppercase letter (A-Z)
2. A step can only begin when ALL of its prerequisite steps are completed
3. **When multiple steps are ready to begin (all prerequisites met), choose the step that comes first alphabetically**
4. All steps must eventually be completed

## Output Format
A single string containing all step letters in the order they should be completed.

Example: `CABDFE`

## Example Walkthrough

Given these dependencies:
```
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
```

Dependency graph:
```
  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
```

Execution order:
1. Only `C` is available (no prerequisites) → complete `C`
2. Both `A` and `F` are available; `A` comes first alphabetically → complete `A`
3. `B`, `D`, and `F` are available; `B` comes first alphabetically → complete `B`
4. `D` and `F` are available; `D` comes first alphabetically → complete `D`
5. Only `F` is available → complete `F`
6. Only `E` is available (now all prerequisites are met) → complete `E`

**Result**: `CABDFE`

## Algorithm Requirements
This is a topological sort problem with the additional constraint that when multiple nodes are available, we must select them in alphabetical order. The solution should:
1. Build a dependency graph from the input
2. Track which steps have no remaining prerequisites
3. Repeatedly select the alphabetically first available step
4. Mark that step as complete and update dependencies
5. Continue until all steps are completed
