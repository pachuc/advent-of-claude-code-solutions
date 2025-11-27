#!/usr/bin/env python3
"""
Test script for mine cart collision detection solution.
"""

from solution import turn_left, turn_right, apply_curve, parse_input, Cart, simulate
import sys

def test_turn_left():
    """Test left turn function."""
    tests = [
        ('UP', 'LEFT'),
        ('LEFT', 'DOWN'),
        ('DOWN', 'RIGHT'),
        ('RIGHT', 'UP')
    ]

    print("Testing turn_left()...")
    for direction, expected in tests:
        result = turn_left(direction)
        status = "PASS" if result == expected else "FAIL"
        print(f"  {direction} -> {result} (expected {expected}): {status}")
        if status == "FAIL":
            return False
    return True


def test_turn_right():
    """Test right turn function."""
    tests = [
        ('UP', 'RIGHT'),
        ('RIGHT', 'DOWN'),
        ('DOWN', 'LEFT'),
        ('LEFT', 'UP')
    ]

    print("\nTesting turn_right()...")
    for direction, expected in tests:
        result = turn_right(direction)
        status = "PASS" if result == expected else "FAIL"
        print(f"  {direction} -> {result} (expected {expected}): {status}")
        if status == "FAIL":
            return False
    return True


def test_curve_forward_slash():
    """Test / curve transformations."""
    tests = [
        ('UP', 'RIGHT'),
        ('RIGHT', 'UP'),
        ('DOWN', 'LEFT'),
        ('LEFT', 'DOWN')
    ]

    print("\nTesting '/' curve...")
    for direction, expected in tests:
        result = apply_curve(direction, '/')
        status = "PASS" if result == expected else "FAIL"
        print(f"  {direction} -> {result} (expected {expected}): {status}")
        if status == "FAIL":
            return False
    return True


def test_curve_backslash():
    """Test \\ curve transformations."""
    tests = [
        ('UP', 'LEFT'),
        ('LEFT', 'UP'),
        ('DOWN', 'RIGHT'),
        ('RIGHT', 'DOWN')
    ]

    print("\nTesting '\\' curve...")
    for direction, expected in tests:
        result = apply_curve(direction, '\\')
        status = "PASS" if result == expected else "FAIL"
        print(f"  {direction} -> {result} (expected {expected}): {status}")
        if status == "FAIL":
            return False
    return True


def test_simple_collision():
    """Test simple head-on collision."""
    print("\nTesting simple collision: >--<")

    # Create a simple track
    track = [
        ['-', '-', '-', '-']
    ]

    # Create two carts facing each other
    carts = [
        Cart(0, 0, 'RIGHT'),
        Cart(3, 0, 'LEFT')
    ]

    # Simulate
    collision_x, collision_y = simulate(track, carts)

    # They should collide somewhere in the middle
    # Cart 1 at (0,0) moves to (1,0)
    # Cart 2 at (3,0) moves to (2,0)
    # They collide at (1,0) or (2,0) depending on move order

    print(f"  Collision at: ({collision_x}, {collision_y})")

    # Check that collision happened on the track
    if collision_y == 0 and 0 <= collision_x <= 3:
        print(f"  PASS: Collision detected on track")
        return True
    else:
        print(f"  FAIL: Unexpected collision position")
        return False


def test_actual_input():
    """Test the actual input."""
    print("\nTesting actual input...")

    track, carts = parse_input('input.md')

    print(f"  Track dimensions: {len(track[0])} x {len(track)} (width x height)")
    print(f"  Number of carts: {len(carts)}")

    # Run simulation
    collision_x, collision_y = simulate(track, carts)

    print(f"  First collision at: ({collision_x}, {collision_y})")

    # Verify the result format
    result = f"{collision_x},{collision_y}"
    print(f"  Result format: {result}")

    # Verify collision is within bounds
    if 0 <= collision_y < len(track) and 0 <= collision_x < len(track[0]):
        track_char = track[collision_y][collision_x]
        print(f"  Track character at collision: '{track_char}'")

        # Check that it's a valid track piece
        valid_chars = ['|', '-', '/', '\\', '+']
        if track_char in valid_chars:
            print(f"  PASS: Collision on valid track")
            return True, result
        else:
            print(f"  FAIL: Collision not on valid track character")
            return False, result
    else:
        print(f"  FAIL: Collision out of bounds")
        return False, result


def main():
    """Run all tests."""
    print("=" * 60)
    print("Mine Cart Collision Detection - Test Suite")
    print("=" * 60)

    all_passed = True

    # Unit tests
    all_passed &= test_turn_left()
    all_passed &= test_turn_right()
    all_passed &= test_curve_forward_slash()
    all_passed &= test_curve_backslash()

    # Integration tests
    all_passed &= test_simple_collision()
    passed, result = test_actual_input()
    all_passed &= passed

    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED!")
        print(f"Final answer: {result}")
        print("=" * 60)
        return result
    else:
        print("SOME TESTS FAILED")
        print("=" * 60)
        return None


if __name__ == "__main__":
    result = main()
    if result is None:
        sys.exit(1)
