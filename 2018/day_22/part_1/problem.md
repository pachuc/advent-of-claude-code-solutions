# Problem Report: Cave Risk Level Calculation

## Objective
Calculate the total risk level for a rectangular cave system region bounded by coordinates `0,0` (mouth of the cave) and the target coordinates.

## Context
We need to help locate a friend who has taken shelter in a cave system. The cave is divided into square regions, each with a specific type (rocky, narrow, or wet). To assess the area before entering, we must calculate the total risk level of the rectangular region from the cave mouth to the target location.

## Input Specification
The input consists of two values:
- **depth**: An integer representing the depth of the cave system
- **target**: Two comma-separated integers `X,Y` representing the target coordinates

Example input:
```
depth: 3558
target: 15,740
```

## Algorithm Requirements

### Step 1: Calculate Geologic Index
For each region at coordinates `X,Y`, determine its geologic index using the first applicable rule:
1. Region at `0,0` (cave mouth): geologic index = `0`
2. Region at target coordinates: geologic index = `0`
3. If `Y = 0`: geologic index = `X * 16807`
4. If `X = 0`: geologic index = `Y * 48271`
5. Otherwise: geologic index = `erosion_level(X-1, Y) * erosion_level(X, Y-1)`

### Step 2: Calculate Erosion Level
For each region:
```
erosion_level = (geologic_index + depth) % 20183
```

### Step 3: Determine Region Type
Based on erosion level modulo 3:
- `erosion_level % 3 = 0`: **rocky** (risk level = 0)
- `erosion_level % 3 = 1`: **wet** (risk level = 1)
- `erosion_level % 3 = 2`: **narrow** (risk level = 2)

### Step 4: Calculate Total Risk Level
Sum the risk levels of all regions in the rectangle where:
- `X` ranges from `0` to `target_X` (inclusive)
- `Y` ranges from `0` to `target_Y` (inclusive)

## Output Specification
A single integer representing the total risk level for the rectangular region.

## Example
Given:
- depth = 510
- target = 10,10

The total risk level for the rectangle from `0,0` to `10,10` is **114**.

## Important Notes
- Coordinates use format `X,Y` where both are non-negative integers
- `X` increases to the right, `Y` increases downward
- The geologic index calculation for most regions depends on erosion levels of adjacent regions, so regions must be calculated in order (row by row or ensuring dependencies are resolved)
- The modulo operation uses value `20183` for erosion level calculation
