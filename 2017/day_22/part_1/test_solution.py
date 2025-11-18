"""
Test script for Sporifica Virus Simulation
"""

from solution import parse_input, simulate_virus


def test_example():
    """Test with the example from problem statement."""
    print("Testing example input...")

    # Parse example input
    infected_nodes, center = parse_input('test_example.txt')

    print(f"Center position: {center}")
    print(f"Initial infected nodes: {infected_nodes}")
    print(f"Number of initial infected: {len(infected_nodes)}")
    print()

    # Test after 7 bursts (expected: 5 infections)
    result_7 = simulate_virus(infected_nodes, center, 7)
    print(f"After 7 bursts: {result_7} infections (expected: 5)")

    # Test after 70 bursts (expected: 41 infections)
    result_70 = simulate_virus(infected_nodes, center, 70)
    print(f"After 70 bursts: {result_70} infections (expected: 41)")

    # Test after 10,000 bursts (expected: 5587 infections)
    result_10000 = simulate_virus(infected_nodes, center, 10000)
    print(f"After 10,000 bursts: {result_10000} infections (expected: 5587)")
    print()

    # Check results
    all_passed = True
    if result_7 == 5:
        print("✓ 7 bursts test PASSED")
    else:
        print("✗ 7 bursts test FAILED")
        all_passed = False

    if result_70 == 41:
        print("✓ 70 bursts test PASSED")
    else:
        print("✗ 70 bursts test FAILED")
        all_passed = False

    if result_10000 == 5587:
        print("✓ 10,000 bursts test PASSED")
    else:
        print("✗ 10,000 bursts test FAILED")
        all_passed = False

    return all_passed


if __name__ == '__main__':
    passed = test_example()
    if passed:
        print("\nAll tests PASSED!")
    else:
        print("\nSome tests FAILED!")
