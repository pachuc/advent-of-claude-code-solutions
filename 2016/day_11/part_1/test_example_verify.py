#!/usr/bin/env python3
"""Test the example from the problem statement (should be 11 steps)."""

from solution import State, solve

def test_example():
    """Test the 11-step example from problem statement."""

    print("Testing example from problem statement...")
    print("Initial state:")
    print("F4 .  .  .  .  .")
    print("F3 .  .  .  LG .")
    print("F2 .  HG .  .  .")
    print("F1 E  .  HM .  LM")
    print()

    # Create initial state
    # Floor 0 (F1): Hydrogen microchip, Lithium microchip
    # Floor 1 (F2): Hydrogen generator
    # Floor 2 (F3): Lithium generator
    # Floor 3 (F4): Empty

    floor_0 = frozenset({('hydrogen', 'M'), ('lithium', 'M')})
    floor_1 = frozenset({('hydrogen', 'G')})
    floor_2 = frozenset({('lithium', 'G')})
    floor_3 = frozenset()

    initial_state = State(
        elevator_floor=0,
        floors=(floor_0, floor_1, floor_2, floor_3)
    )

    # Solve
    result = solve(initial_state)
    expected = 11

    print(f"Expected: {expected} steps")
    print(f"Got: {result} steps")

    if result == expected:
        print("\n✓ TEST PASSED - Example produces 11 steps as expected!")
        return True
    else:
        print(f"\n✗ TEST FAILED - Expected {expected}, got {result}")
        return False

if __name__ == '__main__':
    success = test_example()
    exit(0 if success else 1)
