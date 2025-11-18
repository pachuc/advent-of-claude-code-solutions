from solution import *
import time

def test_actual_input_performance():
    """Test performance on actual input"""
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
    return result

def test_answer_stability():
    """Run simulation multiple times with different termination thresholds"""
    with open('input.md', 'r') as f:
        lines = f.readlines()

    print("\nTesting answer stability with different termination thresholds...")
    print("-" * 50)

    # Test with threshold of 30, 50, and 100 ticks
    results = []
    for threshold in [30, 50, 100]:
        particles = parse_particles(lines)
        start_time = time.time()
        result = simulate_with_collisions(particles, max_ticks_without_collision=threshold)
        elapsed = time.time() - start_time
        results.append(result)
        print(f"Threshold {threshold:3d}: {result} particles remaining (took {elapsed:.3f}s)")

    # All results should be the same
    assert results[0] == results[1] == results[2], \
        f"Results should be stable across thresholds: {results}"

    print("✓ Answer stability test passed - all thresholds give same answer")
    return results[0]

if __name__ == '__main__':
    result1 = test_actual_input_performance()
    result2 = test_answer_stability()

    print("\n" + "=" * 50)
    print(f"FINAL ANSWER: {result1}")
    print("=" * 50)
