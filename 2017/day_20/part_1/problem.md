# Problem Report: Particle Swarm - Finding Closest Particle

## Problem Overview
We need to simulate a particle system and determine which particle will stay closest to the origin point `<0,0,0>` in the long term. This is a physics simulation problem where particles move in 3D space with position, velocity, and acceleration.

## Input Format
The input is a list of particles, one per line, where each particle is numbered starting from 0 (first line = particle 0, second line = particle 1, etc.).

Each particle line contains three 3D vectors in the format:
```
p=<X,Y,Z>, v=<X,Y,Z>, a=<X,Y,Z>
```

Where:
- `p` = position (X, Y, Z coordinates)
- `v` = velocity (X, Y, Z components)
- `a` = acceleration (X, Y, Z components)

Example input lines:
```
p=<1199,-2918,1457>, v=<-13,115,-8>, a=<-7,8,-10>
p=<2551,2418,-1471>, v=<-106,-108,39>, a=<-6,-5,6>
```

## Particle Update Rules
Each tick, ALL particles are updated simultaneously using the following sequence:
1. Increase the X velocity by the X acceleration
2. Increase the Y velocity by the Y acceleration
3. Increase the Z velocity by the Z acceleration
4. Increase the X position by the X velocity (using the newly updated velocity)
5. Increase the Y position by the Y velocity (using the newly updated velocity)
6. Increase the Z position by the Z velocity (using the newly updated velocity)

## Distance Metric
Distance from origin is measured using **Manhattan distance**:
```
distance = |X| + |Y| + |Z|
```
This is the sum of the absolute values of the particle's X, Y, and Z position coordinates.

## Goal
Determine which particle will stay closest to position `<0,0,0>` **in the long term**.

This is asking for the particle that will have the smallest Manhattan distance from the origin as time approaches infinity, not necessarily at any specific point in time.

## Key Insight
In the long term, the particle with the smallest acceleration magnitude will stay closest to the origin. If accelerations are equal, the particle with the smallest velocity magnitude will stay closest. This is because:
- Acceleration dominates position over time (quadratic growth)
- Velocity affects position linearly
- Initial position becomes negligible over long time periods

## Expected Output
The output should be a single integer: the **index number** (starting from 0) of the particle that will stay closest to the origin in the long term.

For example, if particle 5 will stay closest in the long term, the answer is: `5`
