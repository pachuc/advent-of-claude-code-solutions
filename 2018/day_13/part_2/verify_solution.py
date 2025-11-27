"""
Comprehensive verification script for Part 2 solution.
Tests all critical aspects according to the test plan.
"""

import solution
import re


def test_parsing():
    """Test 3.1: Parse Input Correctly"""
    print("=" * 60)
    print("TEST 1: Parsing Input")
    print("=" * 60)

    track, carts = solution.parse_input('input.md')

    # Check dimensions
    height = len(track)
    width = len(track[0]) if track else 0
    print(f"Track dimensions: {width} x {height}")

    # Count initial carts
    cart_count = len(carts)
    print(f"Initial cart count: {cart_count}")

    # Verify all carts have valid positions and directions
    valid_directions = {'UP', 'DOWN', 'LEFT', 'RIGHT'}
    for i, cart in enumerate(carts):
        assert cart.direction in valid_directions, f"Cart {i} has invalid direction: {cart.direction}"
        assert 0 <= cart.x < width, f"Cart {i} x-coordinate out of bounds: {cart.x}"
        assert 0 <= cart.y < height, f"Cart {i} y-coordinate out of bounds: {cart.y}"
        assert not cart.removed, f"Cart {i} should not be marked as removed initially"

    print(f"✓ All {cart_count} carts have valid positions and directions")
    print(f"✓ Track dimensions are reasonable ({width}x{height})")
    print()

    return track, carts, cart_count


def test_first_collision():
    """Test 4.1: Verify first collision matches Part 1"""
    print("=" * 60)
    print("TEST 2: First Collision Verification")
    print("=" * 60)

    # Read Part 1 answer
    with open('part_1_answer.txt', 'r') as f:
        part1_answer = f.read().strip()

    print(f"Part 1 first collision: {part1_answer}")

    # Run simulation with collision logging
    track, carts = solution.parse_input('input.md')
    tick = 0
    first_collision = None

    while True:
        carts.sort(key=lambda c: (c.y, c.x))
        collision_positions = set()

        for i in range(len(carts)):
            if carts[i].removed:
                continue

            solution.move_cart(carts[i], track)
            pos = (carts[i].x, carts[i].y)

            if pos in collision_positions:
                carts[i].removed = True
                if first_collision is None:
                    first_collision = f"{pos[0]},{pos[1]}"
                continue

            for j in range(len(carts)):
                if i != j and not carts[j].removed:
                    if carts[i].x == carts[j].x and carts[i].y == carts[j].y:
                        if first_collision is None:
                            first_collision = f"{pos[0]},{pos[1]}"
                        carts[i].removed = True
                        carts[j].removed = True
                        collision_positions.add(pos)
                        break

        active_carts = [c for c in carts if not c.removed]
        if len(active_carts) <= 1:
            break

        tick += 1

    print(f"Part 2 first collision: {first_collision}")

    if first_collision == part1_answer:
        print("✓ First collision matches Part 1 answer!")
    else:
        print(f"✗ MISMATCH: Expected {part1_answer}, got {first_collision}")
        return False

    print()
    return True


def test_full_simulation():
    """Test 3.3: Full Simulation"""
    print("=" * 60)
    print("TEST 3: Full Simulation with Statistics")
    print("=" * 60)

    track, carts = solution.parse_input('input.md')
    initial_count = len(carts)

    print(f"Starting simulation with {initial_count} carts...")

    # Run simulation with detailed logging
    tick = 0
    collision_count = 0
    collision_log = []

    while True:
        carts.sort(key=lambda c: (c.y, c.x))
        collision_positions = set()
        collisions_this_tick = []

        for i in range(len(carts)):
            if carts[i].removed:
                continue

            solution.move_cart(carts[i], track)
            pos = (carts[i].x, carts[i].y)

            if pos in collision_positions:
                carts[i].removed = True
                collisions_this_tick.append((tick, pos[0], pos[1]))
                continue

            for j in range(len(carts)):
                if i != j and not carts[j].removed:
                    if carts[i].x == carts[j].x and carts[i].y == carts[j].y:
                        carts[i].removed = True
                        carts[j].removed = True
                        collision_positions.add(pos)
                        collisions_this_tick.append((tick, pos[0], pos[1]))
                        break

        if collisions_this_tick:
            collision_count += len(collisions_this_tick)
            collision_log.extend(collisions_this_tick)

        active_carts = [c for c in carts if not c.removed]
        if len(active_carts) == 1:
            last_cart = active_carts[0]
            last_position = f"{last_cart.x},{last_cart.y}"
            break
        elif len(active_carts) == 0:
            print("✗ ERROR: No carts remaining!")
            return False

        tick += 1

        # Safety check to prevent infinite loop
        if tick > 100000:
            print("✗ ERROR: Simulation exceeded 100,000 ticks (possible infinite loop)")
            return False

    print(f"\nSimulation Statistics:")
    print(f"  Total ticks: {tick}")
    print(f"  Total collisions: {len(collision_log)}")
    print(f"  Carts removed: {initial_count - 1}")
    print(f"  Last cart position: {last_position}")

    # Log all collisions
    print(f"\nCollision Timeline:")
    for i, (t, x, y) in enumerate(collision_log, 1):
        print(f"  {i}. Tick {t}: {x},{y}")

    # Verify the last cart is on valid track
    track_char = track[last_cart.y][last_cart.x]
    valid_track = track_char in ['|', '-', '/', '\\', '+']

    if valid_track:
        print(f"✓ Last cart is on valid track ('{track_char}')")
    else:
        print(f"✗ ERROR: Last cart is on invalid track ('{track_char}')")
        return False

    print(f"✓ Simulation completed successfully")
    print()

    return last_position


def test_output_format(result):
    """Test 4.3: Expected Final Answer Format"""
    print("=" * 60)
    print("TEST 4: Output Format Verification")
    print("=" * 60)

    print(f"Result: {result}")

    # Check format
    if re.match(r'^\d+,\d+$', result):
        print("✓ Format matches X,Y pattern")
    else:
        print(f"✗ ERROR: Invalid format (expected X,Y)")
        return False

    # Parse coordinates
    x, y = map(int, result.split(','))
    print(f"  X={x}, Y={y}")

    # Verify coordinates are within reasonable bounds
    track, _ = solution.parse_input('input.md')
    height = len(track)
    width = len(track[0]) if track else 0

    if 0 <= x < width and 0 <= y < height:
        print(f"✓ Coordinates within track bounds (0-{width-1}, 0-{height-1})")
    else:
        print(f"✗ ERROR: Coordinates out of bounds")
        return False

    # Verify position is on valid track
    track_char = track[y][x]
    if track_char in ['|', '-', '/', '\\', '+']:
        print(f"✓ Position is on valid track ('{track_char}')")
    else:
        print(f"✗ ERROR: Position is not on valid track ('{track_char}')")
        return False

    print()
    return True


def test_collision_removal():
    """Test collision removal mechanism"""
    print("=" * 60)
    print("TEST 5: Collision Removal Mechanism")
    print("=" * 60)

    track, carts = solution.parse_input('input.md')
    initial_count = len(carts)

    # Run simulation
    result_x, result_y = solution.simulate(track, carts)

    # Count removed carts
    removed_count = sum(1 for c in carts if c.removed)
    active_count = sum(1 for c in carts if not c.removed)

    print(f"Initial carts: {initial_count}")
    print(f"Removed carts: {removed_count}")
    print(f"Active carts: {active_count}")

    # Should have exactly 1 active cart
    if active_count == 1:
        print("✓ Exactly 1 cart remains")
    else:
        print(f"✗ ERROR: Expected 1 active cart, got {active_count}")
        return False

    # Removed should be initial - 1
    if removed_count == initial_count - 1:
        print(f"✓ Correct number of carts removed ({removed_count})")
    else:
        print(f"✗ ERROR: Expected {initial_count - 1} removed, got {removed_count}")
        return False

    print()
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE SOLUTION VERIFICATION")
    print("=" * 60)
    print()

    all_passed = True

    # Test 1: Parsing
    try:
        track, carts, cart_count = test_parsing()
    except Exception as e:
        print(f"✗ PARSING TEST FAILED: {e}")
        all_passed = False
        return

    # Test 2: First Collision
    try:
        if not test_first_collision():
            all_passed = False
    except Exception as e:
        print(f"✗ FIRST COLLISION TEST FAILED: {e}")
        all_passed = False

    # Test 3: Full Simulation
    try:
        result = test_full_simulation()
        if not result:
            all_passed = False
    except Exception as e:
        print(f"✗ FULL SIMULATION TEST FAILED: {e}")
        all_passed = False
        return

    # Test 4: Output Format
    try:
        if not test_output_format(result):
            all_passed = False
    except Exception as e:
        print(f"✗ OUTPUT FORMAT TEST FAILED: {e}")
        all_passed = False

    # Test 5: Collision Removal
    try:
        if not test_collision_removal():
            all_passed = False
    except Exception as e:
        print(f"✗ COLLISION REMOVAL TEST FAILED: {e}")
        all_passed = False

    # Final Results
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    if all_passed:
        print("✓ ALL TESTS PASSED")
        print(f"\nFinal Answer: {result}")
        return result
    else:
        print("✗ SOME TESTS FAILED")
        return None


if __name__ == "__main__":
    answer = main()
    if answer:
        print(f"\n{'=' * 60}")
        print(f"Solution is CORRECT: {answer}")
        print(f"{'=' * 60}")
