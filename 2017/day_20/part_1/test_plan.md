# Testing Plan: Particle Swarm - Finding Closest Particle

## Testing Strategy Overview

We need to verify that our mathematical approach correctly identifies the particle that stays closest to the origin in the long term. The testing strategy has three levels:
1. **Unit tests**: Verify individual functions work correctly
2. **Integration tests**: Verify the complete solution with known cases
3. **Validation tests**: Verify against the actual input

## Test 1: Unit Test - Manhattan Distance Function

### Objective
Verify the Manhattan distance calculation is correct for various 3D vectors.

### Test Cases

| Input Vector | Expected Output | Description |
|--------------|-----------------|-------------|
| (0, 0, 0) | 0 | Origin |
| (1, 2, 3) | 6 | All positive |
| (-1, -2, -3) | 6 | All negative |
| (1, -2, 3) | 6 | Mixed signs |
| (-5, 0, 5) | 10 | Contains zero |
| (100, 200, 300) | 600 | Large values |

### Implementation
```python
def test_manhattan_distance():
    assert manhattan_distance((0, 0, 0)) == 0
    assert manhattan_distance((1, 2, 3)) == 6
    assert manhattan_distance((-1, -2, -3)) == 6
    assert manhattan_distance((1, -2, 3)) == 6
    assert manhattan_distance((-5, 0, 5)) == 10
    assert manhattan_distance((100, 200, 300)) == 600
    print("✓ Manhattan distance tests passed")
```

## Test 2: Unit Test - Input Parsing

### Objective
Verify that particle data is correctly extracted from input lines.

### Test Cases

**Test Case 1**: Standard format
```
Input: "p=<1199,-2918,1457>, v=<-13,115,-8>, a=<-7,8,-10>"
Expected:
  - p = (1199, -2918, 1457)
  - v = (-13, 115, -8)
  - a = (-7, 8, -10)
```

**Test Case 2**: All positive
```
Input: "p=<1,2,3>, v=<4,5,6>, a=<7,8,9>"
Expected:
  - p = (1, 2, 3)
  - v = (4, 5, 6)
  - a = (7, 8, 9)
```

**Test Case 3**: All negative
```
Input: "p=<-1,-2,-3>, v=<-4,-5,-6>, a=<-7,-8,-9>"
Expected:
  - p = (-1, -2, -3)
  - v = (-4, -5, -6)
  - a = (-7, -8, -9)
```

**Test Case 4**: Contains zeros
```
Input: "p=<0,0,0>, v=<0,0,0>, a=<0,0,0>"
Expected:
  - p = (0, 0, 0)
  - v = (0, 0, 0)
  - a = (0, 0, 0)
```

**Test Case 5**: Large numbers
```
Input: "p=<1199,-2918,1457>, v=<-13,115,-8>, a=<-7,8,-10>"
Expected:
  - p = (1199, -2918, 1457)
  - v = (-13, 115, -8)
  - a = (-7, 8, -10)
```

### Implementation
```python
def test_parsing():
    test_lines = [
        "p=<1199,-2918,1457>, v=<-13,115,-8>, a=<-7,8,-10>",
        "p=<1,2,3>, v=<4,5,6>, a=<7,8,9>",
        "p=<-1,-2,-3>, v=<-4,-5,-6>, a=<-7,-8,-9>",
        "p=<0,0,0>, v=<0,0,0>, a=<0,0,0>",
        ""  # Empty line (should be skipped)
    ]

    particles = parse_particles(test_lines)

    # Should have 4 particles (empty line skipped)
    assert len(particles) == 4

    assert particles[0]['p'] == (1199, -2918, 1457)
    assert particles[0]['v'] == (-13, 115, -8)
    assert particles[0]['a'] == (-7, 8, -10)

    assert particles[1]['p'] == (1, 2, 3)
    assert particles[1]['v'] == (4, 5, 6)
    assert particles[1]['a'] == (7, 8, 9)

    assert particles[2]['p'] == (-1, -2, -3)
    assert particles[2]['v'] == (-4, -5, -6)
    assert particles[2]['a'] == (-7, -8, -9)

    assert particles[3]['p'] == (0, 0, 0)
    assert particles[3]['v'] == (0, 0, 0)
    assert particles[3]['a'] == (0, 0, 0)

    print("✓ Parsing tests passed")
```

## Test 3: Integration Test - Simple Known Cases

### Objective
Verify the complete solution with manually crafted test cases where we know the answer.

### Test Case 1: Clear Winner (Different Accelerations)
```
Particles:
0: p=<0,0,0>, v=<0,0,0>, a=<10,0,0>   # accel magnitude = 10
1: p=<0,0,0>, v=<0,0,0>, a=<1,0,0>    # accel magnitude = 1  ← WINNER
2: p=<0,0,0>, v=<0,0,0>, a=<5,0,0>    # accel magnitude = 5

Expected: Particle 1
Reason: Smallest acceleration magnitude
```

### Test Case 2: Tiebreaker by Velocity
```
Particles:
0: p=<0,0,0>, v=<10,0,0>, a=<1,0,0>   # accel=1, vel=10
1: p=<0,0,0>, v=<2,0,0>, a=<1,0,0>    # accel=1, vel=2   ← WINNER
2: p=<0,0,0>, v=<5,0,0>, a=<1,0,0>    # accel=1, vel=5

Expected: Particle 1
Reason: Same acceleration, smallest velocity magnitude
```

### Test Case 3: Tiebreaker by Position
```
Particles:
0: p=<100,0,0>, v=<1,0,0>, a=<1,0,0>  # accel=1, vel=1, pos=100
1: p=<10,0,0>, v=<1,0,0>, a=<1,0,0>   # accel=1, vel=1, pos=10  ← WINNER
2: p=<50,0,0>, v=<1,0,0>, a=<1,0,0>   # accel=1, vel=1, pos=50

Expected: Particle 1
Reason: Same acceleration and velocity, smallest position magnitude
```

### Test Case 4: Negative Accelerations
```
Particles:
0: p=<0,0,0>, v=<0,0,0>, a=<-3,-4,0>  # accel magnitude = 7  ← WINNER
1: p=<0,0,0>, v=<0,0,0>, a=<5,5,0>    # accel magnitude = 10
2: p=<0,0,0>, v=<0,0,0>, a=<-4,-4,0>  # accel magnitude = 8

Expected: Particle 0
Reason: Smallest acceleration magnitude (Manhattan distance)
```

### Test Case 5: 3D Vectors
```
Particles:
0: p=<1,2,3>, v=<-1,-2,-3>, a=<1,1,1>    # accel=3
1: p=<5,5,5>, v=<10,10,10>, a=<0,1,0>    # accel=1  ← WINNER
2: p=<0,0,0>, v=<0,0,0>, a=<2,0,0>       # accel=2

Expected: Particle 1
Reason: Smallest acceleration magnitude
```

### Test Case 6: Direction vs Magnitude
```
Particles:
0: p=<0,0,0>, v=<0,0,0>, a=<3,0,0>    # accel magnitude = 3 (positive direction)
1: p=<0,0,0>, v=<0,0,0>, a=<-3,0,0>   # accel magnitude = 3 (negative direction)
2: p=<0,0,0>, v=<0,0,0>, a=<0,3,0>    # accel magnitude = 3 (different axis)

Expected: Particle 0 (first one when all tied)
Reason: All have same acceleration magnitude; direction doesn't matter
```

### Implementation
```python
def test_known_cases():
    # Test Case 1
    particles1 = [
        {'index': 0, 'p': (0,0,0), 'v': (0,0,0), 'a': (10,0,0)},
        {'index': 1, 'p': (0,0,0), 'v': (0,0,0), 'a': (1,0,0)},
        {'index': 2, 'p': (0,0,0), 'v': (0,0,0), 'a': (5,0,0)}
    ]
    assert find_closest_particle(particles1) == 1

    # Test Case 2
    particles2 = [
        {'index': 0, 'p': (0,0,0), 'v': (10,0,0), 'a': (1,0,0)},
        {'index': 1, 'p': (0,0,0), 'v': (2,0,0), 'a': (1,0,0)},
        {'index': 2, 'p': (0,0,0), 'v': (5,0,0), 'a': (1,0,0)}
    ]
    assert find_closest_particle(particles2) == 1

    # Test Case 3
    particles3 = [
        {'index': 0, 'p': (100,0,0), 'v': (1,0,0), 'a': (1,0,0)},
        {'index': 1, 'p': (10,0,0), 'v': (1,0,0), 'a': (1,0,0)},
        {'index': 2, 'p': (50,0,0), 'v': (1,0,0), 'a': (1,0,0)}
    ]
    assert find_closest_particle(particles3) == 1

    # Test Case 4
    particles4 = [
        {'index': 0, 'p': (0,0,0), 'v': (0,0,0), 'a': (-3,-4,0)},
        {'index': 1, 'p': (0,0,0), 'v': (0,0,0), 'a': (5,5,0)},
        {'index': 2, 'p': (0,0,0), 'v': (0,0,0), 'a': (-4,-4,0)}
    ]
    assert find_closest_particle(particles4) == 0

    # Test Case 5
    particles5 = [
        {'index': 0, 'p': (1,2,3), 'v': (-1,-2,-3), 'a': (1,1,1)},
        {'index': 1, 'p': (5,5,5), 'v': (10,10,10), 'a': (0,1,0)},
        {'index': 2, 'p': (0,0,0), 'v': (0,0,0), 'a': (2,0,0)}
    ]
    assert find_closest_particle(particles5) == 1

    # Test Case 6: Direction vs Magnitude
    particles6 = [
        {'index': 0, 'p': (0,0,0), 'v': (0,0,0), 'a': (3,0,0)},
        {'index': 1, 'p': (0,0,0), 'v': (0,0,0), 'a': (-3,0,0)},
        {'index': 2, 'p': (0,0,0), 'v': (0,0,0), 'a': (0,3,0)}
    ]
    assert find_closest_particle(particles6) == 0  # All tied, first wins

    print("✓ Known cases tests passed")
```

## Test 4: Validation Test - Simulation Verification

### Objective
For a small subset of particles, verify our mathematical approach matches actual simulation results.

### Methodology
1. Take the first 10 particles from the actual input
2. Run simulations for increasing time steps: 1,000, 10,000, and 100,000
3. Track which particle has the smallest distance at each time step
4. Verify that our answer matches the particle that dominates in later time steps
5. The particle our algorithm picks should match simulation results at 100,000 steps
6. **Rationale for 100,000 steps**: For particles with similar accelerations but different velocities,
   it may take many steps for the quadratic term to dominate the linear term. 100,000 steps provides
   sufficient time for asymptotic behavior to manifest.

### Implementation
```python
def simulate_particle(p, v, a, steps):
    """Simulate a particle for given number of steps, return final distance"""
    pos = list(p)
    vel = list(v)
    acc = list(a)

    for _ in range(steps):
        # Update velocity
        vel[0] += acc[0]
        vel[1] += acc[1]
        vel[2] += acc[2]

        # Update position
        pos[0] += vel[0]
        pos[1] += vel[1]
        pos[2] += vel[2]

    return abs(pos[0]) + abs(pos[1]) + abs(pos[2])

def test_simulation_validation():
    # Read first 10 particles
    with open('input.md', 'r') as f:
        lines = f.readlines()[:10]

    particles = parse_particles(lines)
    predicted = find_closest_particle(particles)

    # Simulate for increasing time steps to verify convergence
    for steps in [1000, 10000, 100000]:
        distances = []
        for particle in particles:
            dist = simulate_particle(
                particle['p'],
                particle['v'],
                particle['a'],
                steps
            )
            distances.append((dist, particle['index']))

        simulated_winner = min(distances)[1]

        print(f"After {steps:6d} steps: predicted={predicted}, simulated={simulated_winner}")

        # At 100,000 steps, asymptotic behavior should dominate
        if steps >= 100000:
            assert predicted == simulated_winner, \
                f"Mismatch at {steps} steps: predicted {predicted} vs simulated {simulated_winner}"

    print("✓ Simulation validation passed")
```

## Test 5: Actual Input Validation

### Objective
Verify the solution runs successfully on the actual input and produces a valid answer.

### Checks
1. File can be read successfully
2. All 1000 particles are parsed correctly
3. Result is an integer between 0 and 999
4. No exceptions or errors occur
5. (Optional) Verify against expected answer if known

### Implementation
```python
def test_actual_input():
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Verify we read all particles
    assert len(lines) == 1000, f"Expected 1000 particles, got {len(lines)}"

    particles = parse_particles(lines)

    # Verify all particles parsed
    assert len(particles) == 1000

    # Verify each particle has correct structure
    for i, particle in enumerate(particles):
        assert particle['index'] == i
        assert len(particle['p']) == 3
        assert len(particle['v']) == 3
        assert len(particle['a']) == 3

    # Get result
    result = find_closest_particle(particles)

    # Verify result is valid
    assert isinstance(result, int), f"Result should be int, got {type(result)}"
    assert 0 <= result < 1000, f"Result {result} out of range [0, 999]"

    print(f"✓ Actual input validation passed")
    print(f"  Answer for actual input: {result}")

    # Optional: Verify against expected answer (uncomment once answer is known)
    # EXPECTED_ANSWER = None  # Replace with actual answer once verified
    # if EXPECTED_ANSWER is not None:
    #     assert result == EXPECTED_ANSWER, f"Expected {EXPECTED_ANSWER}, got {result}"
    #     print(f"  ✓ Answer verified correct: {result}")
```

## Test 6: Edge Cases

### Objective
Test edge cases that might break the solution.

### Test Cases

**Edge Case 1**: All particles identical
```
Should return particle 0 (first in list when all are equal)
```

**Edge Case 2**: Single particle
```
Should return particle 0 (only option)
```

**Edge Case 3**: Acceleration towards origin (negative acceleration away from position)
```
Verify that acceleration magnitude is used, not direction
A particle accelerating towards origin still has acceleration magnitude
```

### Implementation
```python
def test_edge_cases():
    # All identical particles
    particles1 = [
        {'index': 0, 'p': (1,1,1), 'v': (1,1,1), 'a': (1,1,1)},
        {'index': 1, 'p': (1,1,1), 'v': (1,1,1), 'a': (1,1,1)},
        {'index': 2, 'p': (1,1,1), 'v': (1,1,1), 'a': (1,1,1)}
    ]
    assert find_closest_particle(particles1) == 0  # First one wins ties

    # Single particle
    particles2 = [
        {'index': 0, 'p': (100,200,300), 'v': (10,20,30), 'a': (1,2,3)}
    ]
    assert find_closest_particle(particles2) == 0

    print("✓ Edge cases tests passed")
```

## Test Execution Plan

### Order of Execution
1. Run unit tests first (manhattan_distance, parsing)
2. Run integration tests (known cases)
3. Run edge case tests
4. Run simulation validation (takes longer)
5. Run actual input validation last

### Expected Runtime
- Unit tests: < 1 second
- Integration tests: < 1 second
- Edge case tests: < 1 second
- Simulation validation: 5-15 seconds (100,000 simulation steps for 10 particles)
- Actual input validation: < 1 second
- **Total**: < 20 seconds

**Note**: Simulation validation is the longest test due to 100,000 iteration simulations.
This is necessary to ensure asymptotic behavior dominates over initial velocity differences.

### Test File Structure
Create a file `test_solution.py` that imports the solution and runs all tests:

```python
from solution import *

def run_all_tests():
    print("Running test suite...")
    print()

    print("Test 1: Manhattan Distance")
    test_manhattan_distance()
    print()

    print("Test 2: Input Parsing")
    test_parsing()
    print()

    print("Test 3: Known Cases")
    test_known_cases()
    print()

    print("Test 4: Edge Cases")
    test_edge_cases()
    print()

    print("Test 5: Simulation Validation")
    test_simulation_validation()
    print()

    print("Test 6: Actual Input")
    test_actual_input()
    print()

    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)

if __name__ == '__main__':
    run_all_tests()
```

## Success Criteria

The solution is verified correct if:
1. ✓ All unit tests pass
2. ✓ All integration tests pass
3. ✓ All edge case tests pass
4. ✓ Simulation validation confirms our mathematical approach for subset of particles
5. ✓ Actual input produces a valid result (integer in range 0-999)
6. ✓ No runtime errors or exceptions

## Debugging Strategy (If Tests Fail)

### If parsing fails:
- Print the regex matches for failing lines
- Check for unexpected input format variations
- Verify handling of negative numbers

### If known cases fail:
- Print the candidates list to see the (accel, vel, pos, index) tuples
- Verify tuple comparison is working correctly
- Check that manhattan_distance is being called correctly

### If simulation validation fails:
- Print distances at multiple time steps to see convergence
- Check if particles have very similar accelerations but different velocities
- May need to increase simulation steps beyond 100,000 for extreme cases
- Verify the simulation logic matches the problem description:
  1. Update velocity by acceleration first
  2. Then update position by new velocity
- Print the acceleration, velocity, and position magnitudes of competing particles

### If actual input fails:
- Test with a smaller subset first (e.g., first 100 particles)
- Print statistics about the particles (min/max/avg magnitudes)
- Check for any particles with unusual values
