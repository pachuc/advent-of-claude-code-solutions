# Problem Report: Particle Swarm Part 2 - Collision Detection

## Context from Part 1
In Part 1, we simulated a particle system where particles move in 3D space with position, velocity, and acceleration. We found which particle would stay closest to the origin `<0,0,0>` in the long term (answer: particle 243).

Each particle has:
- Position `p` = (X, Y, Z coordinates)
- Velocity `v` = (X, Y, Z components)
- Acceleration `a` = (X, Y, Z components)

**Particle Update Rules** (same as Part 1):
Each tick, ALL particles are updated simultaneously:
1. Increase the X velocity by the X acceleration
2. Increase the Y velocity by the Y acceleration
3. Increase the Z velocity by the Z acceleration
4. Increase the X position by the X velocity (using the newly updated velocity)
5. Increase the Y position by the Y velocity (using the newly updated velocity)
6. Increase the Z position by the Z velocity (using the newly updated velocity)

## Part 2: What's Different
In Part 2, we need to **remove particles that collide**. The goal shifts from finding the closest particle to counting how many particles survive after all collisions are resolved.

## Collision Rules
1. **Collision Detection**: Particles collide if their positions **exactly match** at any point in time
2. **Simultaneous Collisions**: More than two particles can collide at the same time and place
3. **Collision Removal**: Once particles collide, they are **immediately removed** and cannot collide with anything else after that tick
4. **All colliding particles are destroyed**: If 3 particles occupy the same position, all 3 are destroyed (not just 2 of them)

## Example Walkthrough
```
Initial state:
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>  (particle 0)
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>  (particle 1)
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>  (particle 2)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>  (particle 3)

After tick 1:
p=<-3,0,0> (particle 0)
p=<-2,0,0> (particle 1)
p=<-1,0,0> (particle 2)
p=< 2,0,0> (particle 3)

After tick 2:
p=< 0,0,0> (particle 0)
p=< 0,0,0> (particle 1)
p=< 0,0,0> (particle 2)
p=< 1,0,0> (particle 3)

Particles 0, 1, and 2 all occupy <0,0,0> - they collide and are destroyed!

After tick 3:
p=< 0,0,0> (particle 3 only)

Result: 1 particle remains
```

## Input Format
Same as Part 1. The input is a list of particles, one per line, where each particle is numbered starting from 0.

Each particle line contains:
```
p=<X,Y,Z>, v=<X,Y,Z>, a=<X,Y,Z>
```

Example input lines:
```
p=<1199,-2918,1457>, v=<-13,115,-8>, a=<-7,8,-10>
p=<2551,2418,-1471>, v=<-106,-108,39>, a=<-6,-5,6>
```

## Goal
Simulate the particle system over time, removing particles that collide, until no more collisions will occur. Then count how many particles remain.

## Implementation Considerations
1. **Simulation Duration**: We need to run the simulation long enough to detect all possible collisions
2. **Termination Condition**: Stop when either:
   - No particles remain, OR
   - No collisions occur for a sufficient number of ticks (particles have diverged)
3. **Collision Detection**: After each tick's position update, check if any particles share the exact same position
4. **Batch Removal**: All particles at the same position must be removed together (if 3 particles collide, all 3 are destroyed)

## Expected Output
The output should be a single integer: the **number of particles** that remain after all collisions are resolved.

For the example above, the answer would be: `1`
