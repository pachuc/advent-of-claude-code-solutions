# Testing Plan: Particle Swarm Part 2 - Collision Detection

## Testing Philosophy
We need to verify:
1. **Correctness**: Solution produces the right answer
2. **Physics accuracy**: Particles update according to rules
3. **Collision detection**: All collisions are detected and handled properly
4. **Termination**: Simulation stops at the right time

## Test Categories

---

## 1. Example Verification Test

### Test 1.1: Given Example from Problem Statement
**Purpose**: Verify our solution matches the example provided

**Input**:
```
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
```

**Expected Output**: `1` (only particle 3 survives)

**Manual Trace**:
- Tick 0: particles at -6, -4, -2, 3
- Tick 1: particles at -3, -2, -1, 2
- Tick 2: particles at 0, 0, 0, 1 → collision! Remove 0, 1, 2
- Tick 3+: only particle 3 remains at position 0, -1, -2, ...

**Test Method**:
```python
def test_given_example():
    input_lines = [
        "p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>",
        "p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>",
        "p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>",
        "p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>"
    ]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Given example test passed")
```

**Success Criteria**: Output is exactly 1

---

## 2. Particle Update Correctness Tests

### Test 2.1: Single Particle Update (No Acceleration)
**Purpose**: Verify velocity integration works correctly

**Test**:
- Initial: p=(0,0,0), v=(1,2,3), a=(0,0,0)
- After 1 tick: p=(1,2,3), v=(1,2,3)
- After 2 ticks: p=(2,4,6), v=(1,2,3)

**Test Method**:
```python
def test_particle_update_no_accel():
    particle = {'index': 0, 'p': (0,0,0), 'v': (1,2,3), 'a': (0,0,0)}
    updated = update_particle(particle)
    assert updated['p'] == (1,2,3), "Position should be (1,2,3)"
    assert updated['v'] == (1,2,3), "Velocity should be (1,2,3)"
    print("✓ No acceleration update test passed")
```

### Test 2.2: Single Particle Update (With Acceleration)
**Purpose**: Verify velocity is updated BEFORE position

**Test**:
- Initial: p=(0,0,0), v=(0,0,0), a=(1,1,1)
- After 1 tick:
  - v becomes (1,1,1) first
  - then p becomes (1,1,1)
  - Result: p=(1,1,1), v=(1,1,1)
- After 2 ticks:
  - v becomes (2,2,2) first
  - then p becomes (3,3,3) [1+2=3]
  - Result: p=(3,3,3), v=(2,2,2)

**Test Method**:
```python
def test_particle_update_with_accel():
    particle = {'index': 0, 'p': (0,0,0), 'v': (0,0,0), 'a': (1,1,1)}

    # First tick
    particle = update_particle(particle)
    assert particle['p'] == (1,1,1), "After tick 1: position should be (1,1,1)"
    assert particle['v'] == (1,1,1), "After tick 1: velocity should be (1,1,1)"

    # Second tick
    particle = update_particle(particle)
    assert particle['p'] == (3,3,3), "After tick 2: position should be (3,3,3)"
    assert particle['v'] == (2,2,2), "After tick 2: velocity should be (2,2,2)"

    print("✓ With acceleration update test passed")
```

### Test 2.3: Negative Values
**Purpose**: Ensure negative coordinates work correctly

**Test**:
- Initial: p=(10,10,10), v=(-2,-3,-4), a=(-1,-1,-1)
- After 1 tick:
  - v becomes (-3,-4,-5)
  - p becomes (7,6,5)

**Test Method**:
```python
def test_negative_values():
    particle = {'index': 0, 'p': (10,10,10), 'v': (-2,-3,-4), 'a': (-1,-1,-1)}
    particle = update_particle(particle)
    assert particle['p'] == (7,6,5), "Position should handle negatives"
    assert particle['v'] == (-3,-4,-5), "Velocity should handle negatives"
    print("✓ Negative values test passed")
```

---

## 3. Collision Detection Tests

### Test 3.1: Two Particles Collide
**Purpose**: Basic collision detection

**Test**:
```python
def test_two_particle_collision():
    particles = [
        {'index': 0, 'p': (5,5,5), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 1, 'p': (5,5,5), 'v': (0,0,0), 'a': (0,0,0)}
    ]
    collisions = detect_collisions(particles)
    assert collisions == {0, 1}, "Both particles should be marked for removal"
    print("✓ Two-particle collision test passed")
```

### Test 3.2: Three Particles Collide at Same Point
**Purpose**: Verify multi-particle collisions destroy ALL particles

**Test**:
```python
def test_three_particle_collision():
    particles = [
        {'index': 0, 'p': (0,0,0), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 1, 'p': (0,0,0), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 2, 'p': (0,0,0), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 3, 'p': (1,1,1), 'v': (0,0,0), 'a': (0,0,0)}
    ]
    collisions = detect_collisions(particles)
    assert collisions == {0, 1, 2}, "All three colliding particles should be removed"
    assert 3 not in collisions, "Non-colliding particle should not be removed"
    print("✓ Three-particle collision test passed")
```

### Test 3.3: No Collisions
**Purpose**: Verify no false positives

**Test**:
```python
def test_no_collisions():
    particles = [
        {'index': 0, 'p': (0,0,0), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 1, 'p': (1,1,1), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 2, 'p': (2,2,2), 'v': (0,0,0), 'a': (0,0,0)}
    ]
    collisions = detect_collisions(particles)
    assert len(collisions) == 0, "No collisions should be detected"
    print("✓ No collisions test passed")
```

### Test 3.4: Multiple Separate Collision Groups
**Purpose**: Verify multiple independent collisions are handled

**Test**:
```python
def test_multiple_collision_groups():
    particles = [
        # Group 1: collide at (0,0,0)
        {'index': 0, 'p': (0,0,0), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 1, 'p': (0,0,0), 'v': (0,0,0), 'a': (0,0,0)},
        # Group 2: collide at (5,5,5)
        {'index': 2, 'p': (5,5,5), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 3, 'p': (5,5,5), 'v': (0,0,0), 'a': (0,0,0)},
        # Survivor
        {'index': 4, 'p': (10,10,10), 'v': (0,0,0), 'a': (0,0,0)}
    ]
    collisions = detect_collisions(particles)
    assert collisions == {0, 1, 2, 3}, "All colliding particles should be removed"
    assert 4 not in collisions, "Survivor should not be removed"
    print("✓ Multiple collision groups test passed")
```

---

## 4. Simulation Integration Tests

### Test 4.1: All Particles Collide Eventually
**Purpose**: Verify simulation handles total annihilation

**Test**:
```python
def test_all_particles_collide():
    input_lines = [
        "p=<-1,0,0>, v=<1,0,0>, a=<0,0,0>",  # Moving right
        "p=<1,0,0>, v=<-1,0,0>, a=<0,0,0>"   # Moving left
    ]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 0, "All particles should be destroyed"
    print("✓ All particles collide test passed")
```

### Test 4.2: No Collisions Ever Occur
**Purpose**: Verify simulation terminates when particles diverge

**Test**:
```python
def test_no_collisions_diverging():
    input_lines = [
        "p=<0,0,0>, v=<1,0,0>, a=<1,0,0>",   # Moving right, accelerating right
        "p=<0,1,0>, v=<0,1,0>, a=<0,1,0>",   # Moving up, accelerating up
        "p=<0,0,1>, v=<0,0,1>, a=<0,0,1>"    # Moving forward, accelerating forward
    ]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 3, "All 3 particles should survive"
    print("✓ No collisions diverging test passed")
```

### Test 4.3: Sequential Collisions (Not Simultaneous)
**Purpose**: Verify collisions at different times are handled

**Test**:
```python
def test_sequential_collisions():
    """
    Particle 0 and 1 collide at tick 1
    Particles 2 and 3 collide at tick 2
    """
    input_lines = [
        # First collision pair (meet at origin at t=1)
        "p=<-1,0,0>, v=<1,0,0>, a=<0,0,0>",
        "p=<1,0,0>, v=<-1,0,0>, a=<0,0,0>",
        # Second collision pair (meet at origin at t=2)
        "p=<-2,1,0>, v=<1,0,0>, a=<0,0,0>",
        "p=<2,1,0>, v=<-1,0,0>, a=<0,0,0>"
    ]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 0, "All particles should eventually collide and be destroyed"
    print("✓ Sequential collisions test passed")
```

---

## 5. Edge Cases and Special Scenarios

### Test 5.1: Single Particle
**Purpose**: Verify single particle never collides with itself

**Test**:
```python
def test_single_particle():
    input_lines = ["p=<0,0,0>, v=<1,1,1>, a=<1,1,1>"]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 1, "Single particle should survive"
    print("✓ Single particle test passed")
```

### Test 5.2: Particles Start at Same Position
**Purpose**: Verify immediate collisions are detected

**CRITICAL TEST**: This test verifies that particles starting at the same position are detected
as colliding BEFORE the first update. The implementation must check for initial collisions
before entering the simulation loop.

**Test**:
```python
def test_particles_start_same_position():
    input_lines = [
        "p=<0,0,0>, v=<1,0,0>, a=<0,0,0>",
        "p=<0,0,0>, v=<0,1,0>, a=<0,0,0>"
    ]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 0, "Particles starting at same position should collide immediately"
    print("✓ Same starting position test passed")
```

### Test 5.3: Particles Pass Through Each Other (Different Times)
**Purpose**: Verify we only detect exact position matches, not near-misses

**Test Scenario**:
- Create scenario where particles would collide in continuous space but miss on discrete ticks
- Particles pass by each other but never occupy the same position at the same tick

**Test Method**:
```python
def test_particles_miss_on_discrete_ticks():
    """
    Verify we only detect exact position matches on the same tick.

    Particle 0: positions at each tick: 0, 3, 6, 9, 12, ...
    Particle 1: positions at each tick: 7, 5, 3, 1, -1, ...

    They never occupy the same position at the same time, so no collision.
    """
    input_lines = [
        "p=<0,0,0>, v=<3,0,0>, a=<0,0,0>",
        "p=<7,0,0>, v=<-2,0,0>, a=<0,0,0>"
    ]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 2, "Particles that pass by but don't coincide should survive"
    print("✓ Discrete miss test passed")
```

---

## 6. Actual Input Validation

### Test 6.1: Run on Actual Input
**Purpose**: Verify solution completes in reasonable time

**Test Method**:
```python
import time

def test_actual_input_performance():
    with open('input.md', 'r') as f:
        lines = f.readlines()

    particles = parse_particles(lines)
    print(f"Loaded {len(particles)} particles")

    start_time = time.time()
    result = simulate_with_collisions(particles)
    elapsed = time.time() - start_time

    print(f"Result: {result} particles remaining")
    print(f"Computation time: {elapsed:.3f} seconds")

    assert elapsed < 2.0, "Should complete in under 2 seconds"
    assert result >= 0, "Result should be non-negative"
    assert result <= len(particles), "Result should not exceed initial particle count"

    print("✓ Actual input performance test passed")
```

**Success Criteria**:
- Completes in <2 seconds (should be well under 1 second for typical inputs)
- Returns a reasonable number (between 0 and 1000)
- Result is deterministic (same answer on repeated runs)

### Test 6.2: Verify Answer Stability
**Purpose**: Ensure termination threshold is sufficient

**Test Method**:
```python
def test_answer_stability():
    """Run simulation multiple times with different termination thresholds"""
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Test with threshold of 50, 100, and 200 ticks
    results = []
    for threshold in [50, 100, 200]:
        particles = parse_particles(lines)
        # Use the max_ticks_without_collision parameter (updated function signature)
        result = simulate_with_collisions(particles, max_ticks_without_collision=threshold)
        results.append(result)

    # All results should be the same
    assert results[0] == results[1] == results[2], \
        f"Results should be stable across thresholds: {results}"

    print("✓ Answer stability test passed")
```

---

## 7. Testing Execution Strategy

### Phase 1: Unit Tests (Component Level)
Run in order:
1. Particle update tests (2.1, 2.2, 2.3)
2. Collision detection tests (3.1, 3.2, 3.3, 3.4)

### Phase 2: Integration Tests
3. Given example test (1.1) - MUST PASS
4. Simulation tests (4.1, 4.2, 4.3)
5. Edge case tests (5.1, 5.2, 5.3)

### Phase 3: Validation
6. Actual input test (6.1)
7. Stability test (6.2) - optional but recommended

### Test Implementation Approach
Create a simple test file `test_solution.py`:
```python
from solution import *

def run_all_tests():
    # Unit tests
    test_particle_update_no_accel()
    test_particle_update_with_accel()
    test_negative_values()

    test_two_particle_collision()
    test_three_particle_collision()
    test_no_collisions()
    test_multiple_collision_groups()

    # Integration tests
    test_given_example()
    test_all_particles_collide()
    test_no_collisions_diverging()
    test_sequential_collisions()

    # Edge cases
    test_single_particle()
    test_particles_start_same_position()
    test_particles_miss_on_discrete_ticks()

    # Validation
    test_actual_input_performance()

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)

if __name__ == '__main__':
    run_all_tests()
```

---

## 8. Manual Verification Steps

### Step 1: Verify Example by Hand
Trace through the given example step-by-step and confirm output is 1.

### Step 2: Check Sanity of Final Answer
- Should be between 0 and 1000 (initial particle count)
- Typical range varies based on input, but result should be reasonable

### Step 3: Check for Common Bugs
- **Bug**: Particles starting at same position not detected
  - **Fix**: Check for initial collisions BEFORE entering simulation loop
  - **Symptom**: Test 5.2 will fail if this bug exists
- **Bug**: Particles removed before all collisions detected in a tick
  - **Fix**: Detect all collisions first, then remove all at once
- **Bug**: Velocity updated after position
  - **Fix**: Update velocity first, then position (order matters!)
- **Bug**: Only 2 particles removed in 3-way collision
  - **Fix**: Remove ALL particles at same position
- **Bug**: Simulation runs forever
  - **Fix**: Implement MAX_ITERATIONS safety limit and termination threshold

---

## Success Criteria Summary

### Must Pass:
1. ✓ Given example returns 1
2. ✓ Particle update follows correct order (v then p)
3. ✓ All colliding particles removed (including 3+ particle collisions)
4. ✓ Particles starting at same position are detected (test 5.2)
5. ✓ Actual input completes in <2 seconds
6. ✓ Result is deterministic and stable across different thresholds

### Should Pass:
7. All unit tests pass
8. All edge case tests pass
9. Performance is reasonable (<1 second for 1000 particles)

### Quality Indicators:
- Code is clear and well-commented
- Answer makes sense (between 0 and initial particle count)
- Simulation terminates naturally (not via max iteration limit)
- Function signature matches: `simulate_with_collisions(particles, max_ticks_without_collision=50)`
