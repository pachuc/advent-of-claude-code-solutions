from solution import *

def test_manhattan_distance():
    assert manhattan_distance((0, 0, 0)) == 0
    assert manhattan_distance((1, 2, 3)) == 6
    assert manhattan_distance((-1, -2, -3)) == 6
    assert manhattan_distance((1, -2, 3)) == 6
    assert manhattan_distance((-5, 0, 5)) == 10
    assert manhattan_distance((100, 200, 300)) == 600
    print("✓ Manhattan distance tests passed")

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

def test_known_cases():
    # Test Case 1: Clear winner (different accelerations)
    particles1 = [
        {'index': 0, 'p': (0,0,0), 'v': (0,0,0), 'a': (10,0,0)},
        {'index': 1, 'p': (0,0,0), 'v': (0,0,0), 'a': (1,0,0)},
        {'index': 2, 'p': (0,0,0), 'v': (0,0,0), 'a': (5,0,0)}
    ]
    assert find_closest_particle(particles1) == 1

    # Test Case 2: Tiebreaker by velocity
    particles2 = [
        {'index': 0, 'p': (0,0,0), 'v': (10,0,0), 'a': (1,0,0)},
        {'index': 1, 'p': (0,0,0), 'v': (2,0,0), 'a': (1,0,0)},
        {'index': 2, 'p': (0,0,0), 'v': (5,0,0), 'a': (1,0,0)}
    ]
    assert find_closest_particle(particles2) == 1

    # Test Case 3: Tiebreaker by position
    particles3 = [
        {'index': 0, 'p': (100,0,0), 'v': (1,0,0), 'a': (1,0,0)},
        {'index': 1, 'p': (10,0,0), 'v': (1,0,0), 'a': (1,0,0)},
        {'index': 2, 'p': (50,0,0), 'v': (1,0,0), 'a': (1,0,0)}
    ]
    assert find_closest_particle(particles3) == 1

    # Test Case 4: Negative accelerations
    particles4 = [
        {'index': 0, 'p': (0,0,0), 'v': (0,0,0), 'a': (-3,-4,0)},
        {'index': 1, 'p': (0,0,0), 'v': (0,0,0), 'a': (5,5,0)},
        {'index': 2, 'p': (0,0,0), 'v': (0,0,0), 'a': (-4,-4,0)}
    ]
    assert find_closest_particle(particles4) == 0

    # Test Case 5: 3D vectors
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
