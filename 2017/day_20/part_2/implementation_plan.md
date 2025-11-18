# Implementation Plan: Particle Swarm Part 2 - Collision Detection

## Overview
Part 2 requires simulating particle collisions, which is fundamentally different from Part 1. While Part 1 used mathematical analysis (finding particle with smallest acceleration), Part 2 requires actual simulation because collisions create non-linear dynamics that can't be predicted analytically.

**Key Difference**: Part 1 found the answer analytically; Part 2 requires step-by-step simulation.

## Algorithm Approach

### Core Strategy
**Simulation-based approach** - We must simulate the particle system tick by tick, detecting and removing collisions at each step, until the system stabilizes (no more collisions occur).

### Time Complexity
- **Input Size**: 1000 particles
- **Per-tick operations**: O(n) for updates + O(n) for collision detection using hash map
- **Expected ticks**: Typically <100 ticks for particles to diverge
- **Total complexity**: O(t × n) where t is number of ticks, n is number of particles
- **Practical runtime**: Should complete in under a second for 1000 particles

### Space Complexity
- O(n) for particle storage
- O(n) for position-to-particle mapping during collision detection

## Step-by-Step Implementation

### Step 1: Reuse Parsing Logic from Part 1
**File**: `part_1_solution.py` has `parse_particles()` function

**Action**: Copy the `parse_particles()` function directly as it works perfectly for our needs.

**Implementation**:
- Function extracts position (p), velocity (v), and acceleration (a) from each line
- Uses regex to parse numbers: `re.findall(r'-?\d+', line)`
- Returns list of particle dictionaries with 'index', 'p', 'v', 'a'

### Step 2: Implement Particle Update Function
**Purpose**: Update particle position and velocity according to physics rules

**Function signature**: `update_particle(particle) -> particle`

**Algorithm**:
```python
def update_particle(particle):
    """
    Update particle velocity and position for one tick.

    Order matters (per problem spec):
    1. v += a  (update velocity by acceleration)
    2. p += v  (update position by NEW velocity)
    """
    # Unpack current state
    px, py, pz = particle['p']
    vx, vy, vz = particle['v']
    ax, ay, az = particle['a']

    # Step 1: Update velocity
    vx += ax
    vy += ay
    vz += az

    # Step 2: Update position with NEW velocity
    px += vx
    py += vy
    pz += vz

    # Return updated particle
    return {
        'index': particle['index'],
        'p': (px, py, pz),
        'v': (vx, vy, vz),
        'a': (ax, ay, az)
    }
```

**Key consideration**: Use tuples for positions to make them hashable (needed for collision detection).

### Step 3: Implement Collision Detection
**Purpose**: Find all particles that share the same position

**Function signature**: `detect_collisions(particles) -> set of indices to remove`

**Algorithm**:
```python
def detect_collisions(particles):
    """
    Detect all particles that collide (share same position).

    Returns: set of particle indices that should be removed
    """
    # Map position -> list of particle indices at that position
    position_map = {}

    for particle in particles:
        pos = particle['p']
        if pos not in position_map:
            position_map[pos] = []
        position_map[pos].append(particle['index'])

    # Find all positions with 2+ particles (collisions)
    indices_to_remove = set()
    for pos, particle_indices in position_map.items():
        if len(particle_indices) >= 2:
            # ALL particles at this position are destroyed
            indices_to_remove.update(particle_indices)

    return indices_to_remove
```

**Why hash map?** O(1) lookup per particle = O(n) total time for collision detection.

**Key detail**: If 3+ particles collide at same position, ALL are destroyed (not just 2).

### Step 4: Implement Simulation Loop
**Purpose**: Run simulation until no more collisions occur

**Function signature**: `simulate_with_collisions(particles, max_ticks_without_collision=50) -> int`

**Algorithm**:
```python
def simulate_with_collisions(particles, max_ticks_without_collision=50):
    """
    Simulate particle system with collision removal.

    Args:
        particles: List of particle dictionaries
        max_ticks_without_collision: Number of ticks without collision before termination (default: 50)

    Returns: number of particles remaining after all collisions resolved
    """
    particles = list(particles)  # Make a copy to avoid modifying original

    # CRITICAL: Check for initial collisions (particles starting at same position)
    # This must happen BEFORE the first update
    indices_to_remove = detect_collisions(particles)
    if indices_to_remove:
        particles = [p for p in particles if p['index'] not in indices_to_remove]

    # If all particles destroyed initially, return early
    if len(particles) == 0:
        return 0

    # Track ticks without collisions for termination
    ticks_without_collision = 0
    MAX_ITERATIONS = 1000  # Safety limit to prevent infinite loops

    for iteration in range(MAX_ITERATIONS):
        # Step 1: Update all particles simultaneously
        particles = [update_particle(p) for p in particles]

        # Step 2: Detect collisions
        indices_to_remove = detect_collisions(particles)

        # Step 3: Remove colliding particles
        if indices_to_remove:
            particles = [p for p in particles if p['index'] not in indices_to_remove]
            ticks_without_collision = 0  # Reset counter
        else:
            ticks_without_collision += 1

        # Step 4: Check termination conditions
        if len(particles) == 0:
            return 0

        if ticks_without_collision >= max_ticks_without_collision:
            # No collisions for N ticks - system has stabilized
            return len(particles)

    # If we reach max iterations, the system should have stabilized by now
    # This is a safety measure in case of bugs
    raise RuntimeError(f"Simulation did not converge after {MAX_ITERATIONS} iterations")
```

**Termination logic**:
1. **Initial collision check**: Check if particles start at the same position (before any updates)
2. **No particles left**: Return 0
3. **No collisions for N ticks**: Particles have diverged, no more collisions will occur
   - N=50 is conservative (particles with acceleration diverge quickly)
   - Made configurable via parameter for testing different thresholds
   - Empirically, most Advent of Code problems stabilize within 10-20 ticks
4. **Max iterations safety**: Prevents infinite loops if there's a bug

**Why 50 ticks default?**:
- Particles with different accelerations diverge quadratically (distance ∝ t²)
- After 50 ticks with no collision, particles are far apart and moving away
- This is a heuristic that may need adjustment, but should work for typical inputs
- Made configurable to allow testing different values

### Step 5: Implement Main Function
**Purpose**: Read input, run simulation, output result

```python
def main():
    # Read input file
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse particles (reuse from Part 1)
    particles = parse_particles(lines)

    # Run simulation
    result = simulate_with_collisions(particles)

    # Output result
    print(result)
```

## Code Structure

```
solution.py:
├── parse_particles(lines)           [Reuse from Part 1]
├── update_particle(particle)         [New - physics update]
├── detect_collisions(particles)      [New - collision detection]
├── simulate_with_collisions(particles) [New - main simulation loop]
└── main()                            [Modified from Part 1]
```

## Optimization Considerations

### Why This Algorithm is Efficient
1. **Hash-based collision detection**: O(n) per tick instead of O(n²) pairwise comparison
2. **Early termination**: Stops when particles diverge (typically <100 ticks)
3. **In-place updates**: Minimal memory allocation
4. **Initial collision check**: Prevents unnecessary updates for particles that start colliding

### Potential Optimizations (Not Needed for 1000 particles)
- **Spatial partitioning**: Use grid or octree if millions of particles
- **Parallel processing**: Update particles in parallel (overkill for n=1000)
- **Mathematical bounds**: Prove when collisions are impossible (complex, not worth it)

### Trade-offs
- **Convergence threshold (default 50 ticks)**:
  - Too low: Might miss late collisions
  - Too high: Unnecessary computation
  - 50 is a good middle ground for this problem size
  - Made configurable to allow experimentation and testing

### Debugging Features
- **Optional verbose mode**: Add a `verbose=False` parameter to print simulation progress:
  ```python
  def simulate_with_collisions(particles, max_ticks_without_collision=50, verbose=False):
      if verbose:
          print(f"Starting simulation with {len(particles)} particles")
      # ... in the loop ...
      if verbose and indices_to_remove:
          print(f"Tick {iteration}: {len(indices_to_remove)} particles collided")
  ```
  This helps with debugging but is not required for the solution

## Edge Cases to Handle
1. **All particles collide**: Return 0
2. **No collisions ever**: Return original count after N ticks
3. **Multi-particle collisions**: Destroy all particles at same position (not just pairs)
4. **Particles starting at same position**: Check for collisions BEFORE first update
5. **Empty input**: Should not occur based on problem, but parse_particles handles it
6. **Infinite loop prevention**: MAX_ITERATIONS safety limit

## Expected Performance
- **Input size**: 1000 particles
- **Expected ticks**: 20-100 ticks until stabilization
- **Operations per tick**: 1000 updates + 1000 collision checks = 2000 ops
- **Total operations**: ~200,000 operations
- **Runtime**: <100ms on modern hardware

## Dependencies
- `re` module (for parsing - already used in Part 1)
- No external libraries needed (pure Python)

## Testing Strategy Reference
See `test_plan.md` for comprehensive testing approach including:
- Example verification
- Edge case testing
- Performance validation
- Collision detection correctness
