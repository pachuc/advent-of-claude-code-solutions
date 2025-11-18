from solution import *

def test_given_example():
    """Test the example from the problem statement"""
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

def test_particle_update_no_accel():
    """Test particle update without acceleration"""
    particle = {'index': 0, 'p': (0,0,0), 'v': (1,2,3), 'a': (0,0,0)}
    updated = update_particle(particle)
    assert updated['p'] == (1,2,3), "Position should be (1,2,3)"
    assert updated['v'] == (1,2,3), "Velocity should be (1,2,3)"
    print("✓ No acceleration update test passed")

def test_particle_update_with_accel():
    """Test particle update with acceleration"""
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

def test_negative_values():
    """Test negative values work correctly"""
    particle = {'index': 0, 'p': (10,10,10), 'v': (-2,-3,-4), 'a': (-1,-1,-1)}
    particle = update_particle(particle)
    assert particle['p'] == (7,6,5), "Position should handle negatives"
    assert particle['v'] == (-3,-4,-5), "Velocity should handle negatives"
    print("✓ Negative values test passed")

def test_two_particle_collision():
    """Test basic collision detection"""
    particles = [
        {'index': 0, 'p': (5,5,5), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 1, 'p': (5,5,5), 'v': (0,0,0), 'a': (0,0,0)}
    ]
    collisions = detect_collisions(particles)
    assert collisions == {0, 1}, "Both particles should be marked for removal"
    print("✓ Two-particle collision test passed")

def test_three_particle_collision():
    """Test multi-particle collision"""
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

def test_no_collisions():
    """Test no false positives"""
    particles = [
        {'index': 0, 'p': (0,0,0), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 1, 'p': (1,1,1), 'v': (0,0,0), 'a': (0,0,0)},
        {'index': 2, 'p': (2,2,2), 'v': (0,0,0), 'a': (0,0,0)}
    ]
    collisions = detect_collisions(particles)
    assert len(collisions) == 0, "No collisions should be detected"
    print("✓ No collisions test passed")

def test_all_particles_collide():
    """Test simulation handles total annihilation"""
    input_lines = [
        "p=<-1,0,0>, v=<1,0,0>, a=<0,0,0>",  # Moving right
        "p=<1,0,0>, v=<-1,0,0>, a=<0,0,0>"   # Moving left
    ]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 0, "All particles should be destroyed"
    print("✓ All particles collide test passed")

def test_no_collisions_diverging():
    """Test simulation terminates when particles diverge"""
    input_lines = [
        "p=<0,0,0>, v=<1,0,0>, a=<1,0,0>",   # Moving right, accelerating right
        "p=<0,1,0>, v=<0,1,0>, a=<0,1,0>",   # Moving up, accelerating up
        "p=<0,0,1>, v=<0,0,1>, a=<0,0,1>"    # Moving forward, accelerating forward
    ]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 3, "All 3 particles should survive"
    print("✓ No collisions diverging test passed")

def test_single_particle():
    """Test single particle never collides with itself"""
    input_lines = ["p=<0,0,0>, v=<1,1,1>, a=<1,1,1>"]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 1, "Single particle should survive"
    print("✓ Single particle test passed")

def test_particles_start_same_position():
    """Test particles starting at same position are detected"""
    input_lines = [
        "p=<0,0,0>, v=<1,0,0>, a=<0,0,0>",
        "p=<0,0,0>, v=<0,1,0>, a=<0,0,0>"
    ]
    particles = parse_particles(input_lines)
    result = simulate_with_collisions(particles)
    assert result == 0, "Particles starting at same position should collide immediately"
    print("✓ Same starting position test passed")

def run_all_tests():
    """Run all unit and integration tests"""
    print("Running unit tests...")
    print("-" * 50)

    # Unit tests
    test_particle_update_no_accel()
    test_particle_update_with_accel()
    test_negative_values()

    test_two_particle_collision()
    test_three_particle_collision()
    test_no_collisions()

    print("\nRunning integration tests...")
    print("-" * 50)

    # Integration tests
    test_given_example()
    test_all_particles_collide()
    test_no_collisions_diverging()

    # Edge cases
    test_single_particle()
    test_particles_start_same_position()

    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)

if __name__ == '__main__':
    run_all_tests()
