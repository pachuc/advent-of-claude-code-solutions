# Implementation Plan: Particle Swarm - Finding Closest Particle

## Problem Analysis

### Key Insights
1. **Long-term behavior**: As time approaches infinity, acceleration dominates the particle's movement
2. **Manhattan distance**: We use |X| + |Y| + |Z| as our distance metric
3. **Physics**: Position grows quadratically with acceleration, linearly with initial velocity
4. **Asymptotic behavior**: Initial position becomes negligible over time

### Mathematical Foundation
For a particle with initial position p₀, velocity v₀, and acceleration a, after t time steps:
- Position: p(t) = p₀ + v₀·t + a·t²/2
- As t → ∞, the a·t² term dominates
- Therefore, the particle with smallest acceleration magnitude will stay closest

### Algorithm Strategy
We don't need to simulate the physics! We can use the mathematical insight:
1. **Primary criterion**: Compare Manhattan distance of acceleration vectors
2. **Tiebreaker 1**: If accelerations are equal, compare velocity magnitudes
3. **Tiebreaker 2**: If both are equal, compare initial position magnitudes

This gives us O(n) time complexity instead of O(n·t) for simulation.

## Implementation Steps

### Step 1: Input Parsing
**Objective**: Parse the input file to extract particle data

**Details**:
- Read all lines from input file
- For each line, extract position (p), velocity (v), and acceleration (a) vectors
- Use regular expressions to parse the format: `p=<X,Y,Z>, v=<X,Y,Z>, a=<X,Y,Z>`
- Store each particle's data with its index (line number starting from 0)

**Data Structure**:
```python
particles = [
    {
        'index': 0,
        'p': (x, y, z),  # position tuple
        'v': (x, y, z),  # velocity tuple
        'a': (x, y, z)   # acceleration tuple
    },
    ...
]
```

**Implementation approach**:
- Use `re.findall()` or `re.match()` to extract numeric values
- Handle negative numbers correctly with pattern `-?\d+`
- Store as integers (input appears to use integers)
- Add basic validation to ensure 9 numbers are extracted per line

### Step 2: Manhattan Distance Function
**Objective**: Create a helper function to calculate Manhattan distance

**Details**:
- Input: A 3D vector (x, y, z)
- Output: |x| + |y| + |z|
- This will be reused for position, velocity, and acceleration vectors

**Function signature**:
```python
def manhattan_distance(vector):
    x, y, z = vector
    return abs(x) + abs(y) + abs(z)
```

### Step 3: Find Closest Particle
**Objective**: Determine which particle stays closest in the long term

**Algorithm**:
1. For each particle, calculate:
   - Acceleration magnitude (Manhattan distance of acceleration vector)
   - Velocity magnitude (Manhattan distance of velocity vector)
   - Position magnitude (Manhattan distance of position vector)

2. Create a list of tuples: (accel_mag, vel_mag, pos_mag, particle_index)

3. Find the minimum using Python's built-in comparison:
   - Python compares tuples lexicographically
   - This automatically gives us the tiebreaking behavior we need
   - First compares acceleration, then velocity, then position

4. Return the particle index of the minimum

**Mathematical Justification for Tiebreaking**:
- When accelerations are equal (a₁ = a₂), the quadratic terms in p(t) = p₀ + v₀·t + ½a·t² cancel out
- We're left comparing p₁(t) = p₀₁ + v₀₁·t vs p₂(t) = p₀₂ + v₀₂·t
- As t → ∞, the linear velocity term dominates, so we compare velocity magnitudes
- When both accelerations and velocities are equal, only initial position differs
- Therefore the tiebreaking hierarchy (acceleration → velocity → position) is mathematically sound

**Implementation approach**:
```python
def find_closest_particle(particles):
    """
    Find particle that stays closest to origin in the long term.

    Mathematical basis:
    - Position: p(t) = p₀ + v₀·t + ½a·t²
    - As t → ∞, the t² term dominates
    - Therefore: particle with smallest |a| will be closest
    - Tiebreakers: velocity magnitude (t term), then position magnitude (constant)
    """
    if not particles:
        raise ValueError("No particles found in input")

    candidates = []
    for particle in particles:
        accel_mag = manhattan_distance(particle['a'])
        vel_mag = manhattan_distance(particle['v'])
        pos_mag = manhattan_distance(particle['p'])
        candidates.append((accel_mag, vel_mag, pos_mag, particle['index']))

    # Find minimum - tuple comparison handles tiebreaking automatically
    closest = min(candidates)
    return closest[3]  # return the index
```

### Step 4: Main Function
**Objective**: Orchestrate the solution

**Details**:
1. Read input from file (input.md)
2. Parse particles
3. Find closest particle
4. Print the result

**Implementation approach**:
```python
def main():
    # Read input
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse particles
    particles = parse_particles(lines)

    # Find closest
    result = find_closest_particle(particles)

    # Output
    print(result)
```

### Step 5: Complete Solution Structure
**File**: `solution.py`

**Complete structure**:
```python
import re

def parse_particles(lines):
    """Parse input lines into particle data structures"""
    particles = []
    for index, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            continue

        # Extract all numbers (including negatives)
        numbers = list(map(int, re.findall(r'-?\d+', line)))

        # Basic validation: ensure we have exactly 9 numbers (3 for p, 3 for v, 3 for a)
        assert len(numbers) == 9, f"Expected 9 numbers on line {index}, got {len(numbers)}"

        # First 3 are position, next 3 are velocity, last 3 are acceleration
        particle = {
            'index': index,
            'p': tuple(numbers[0:3]),
            'v': tuple(numbers[3:6]),
            'a': tuple(numbers[6:9])
        }
        particles.append(particle)
    return particles

def manhattan_distance(vector):
    """Calculate Manhattan distance of a 3D vector"""
    return abs(vector[0]) + abs(vector[1]) + abs(vector[2])

def find_closest_particle(particles):
    """
    Find particle that stays closest to origin in the long term.

    Mathematical basis:
    - Position: p(t) = p₀ + v₀·t + ½a·t²
    - As t → ∞, the t² term dominates
    - Therefore: particle with smallest |a| will be closest
    - Tiebreakers: velocity magnitude (t term), then position magnitude (constant)
    """
    if not particles:
        raise ValueError("No particles found in input")

    candidates = []
    for particle in particles:
        accel_mag = manhattan_distance(particle['a'])
        vel_mag = manhattan_distance(particle['v'])
        pos_mag = manhattan_distance(particle['p'])
        candidates.append((accel_mag, vel_mag, pos_mag, particle['index']))

    closest = min(candidates)
    return closest[3]

def main():
    with open('input.md', 'r') as f:
        lines = f.readlines()

    particles = parse_particles(lines)
    result = find_closest_particle(particles)
    print(result)

if __name__ == '__main__':
    main()
```

## Complexity Analysis

### Time Complexity: O(n)
- Parsing: O(n) where n is number of particles
- Finding minimum: O(n)
- Total: O(n)

### Space Complexity: O(n)
- Storing particle data: O(n)
- Candidates list: O(n)

### Input Size Considerations
With 1000 particles, this approach is highly efficient:
- No simulation needed (would be O(n·t) where t could be very large)
- Linear scan is optimal for this problem
- Memory usage is minimal

## Edge Cases Handled

1. **Negative coordinates**: Regex pattern `-?\d+` handles negative numbers
2. **Ties in acceleration**: Tiebreaking by velocity magnitude (mathematically justified)
3. **Ties in acceleration and velocity**: Tiebreaking by position magnitude
4. **All equal**: Returns lowest index (first particle in min comparison)
5. **Empty input**: Raises ValueError if no particles are provided
6. **Malformed lines**: Assertion error if line doesn't contain exactly 9 numbers
7. **Empty lines**: Skipped during parsing

## Validation of Mathematical Approach

Why we don't need simulation:
- Physics equation: p(t) = p₀ + v₀·t + ½a·t²
- As t → ∞: The t² term dominates
- Therefore: lim(t→∞) distance ∝ |acceleration|
- The particle with smallest |a| will eventually be closest
- Initial position and velocity only matter for tiebreaking

This mathematical approach is both correct and vastly more efficient than simulation.
