"""Verification script for Part 2 solution."""
import re
from solution import (
    parse_input, is_safe_floor, State,
    generate_valid_moves, canonicalize_state, solve
)

def test_initial_state_setup():
    """Test 1: Verify initial state setup with 4 new items."""
    print("Test 1: Verifying initial state setup...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    initial_floors = parse_input(input_text)

    # Add the 4 new items
    initial_floors[0].add(('elerium', 'G'))
    initial_floors[0].add(('elerium', 'M'))
    initial_floors[0].add(('dilithium', 'G'))
    initial_floors[0].add(('dilithium', 'M'))

    print(f"  Floor 0 items: {sorted(initial_floors[0])}")
    print(f"  Total items on floor 0: {len(initial_floors[0])}")

    # Verify expected items
    expected_items = {
        ('strontium', 'G'), ('strontium', 'M'),
        ('plutonium', 'G'), ('plutonium', 'M'),
        ('elerium', 'G'), ('elerium', 'M'),
        ('dilithium', 'G'), ('dilithium', 'M')
    }

    assert initial_floors[0] == expected_items, f"Floor 0 items mismatch!"
    assert len(initial_floors[0]) == 8, "Floor 0 should have 8 items"

    print("  ✓ All 8 expected items present on floor 0")
    print()

def test_safety_rules():
    """Test 2: Safety rule validation with new items."""
    print("Test 2: Testing safety rules...")

    # Case 2a: Safe - matching pair
    test_floor = {('elerium', 'G'), ('elerium', 'M')}
    assert is_safe_floor(test_floor) == True
    print("  ✓ Case 2a: Elerium matching pair is safe")

    # Case 2b: Safe - multiple matching pairs
    test_floor = {('elerium', 'G'), ('elerium', 'M'),
                  ('dilithium', 'G'), ('dilithium', 'M')}
    assert is_safe_floor(test_floor) == True
    print("  ✓ Case 2b: Both new pairs together is safe")

    # Case 2c: Unsafe - unprotected microchip
    test_floor = {('elerium', 'M'), ('dilithium', 'G')}
    assert is_safe_floor(test_floor) == False
    print("  ✓ Case 2c: Elerium chip with dilithium generator is unsafe")

    # Case 2d: Safe - microchips alone
    test_floor = {('elerium', 'M'), ('dilithium', 'M'), ('strontium', 'M'),
                  ('plutonium', 'M'), ('thulium', 'M'), ('ruthenium', 'M'),
                  ('curium', 'M')}
    assert is_safe_floor(test_floor) == True
    print("  ✓ Case 2d: All 7 microchips together is safe")
    print()

def test_initial_state_validity():
    """Test 3: Initial state validity."""
    print("Test 3: Verifying initial state validity...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    initial_floors = parse_input(input_text)
    initial_floors[0].add(('elerium', 'G'))
    initial_floors[0].add(('elerium', 'M'))
    initial_floors[0].add(('dilithium', 'G'))
    initial_floors[0].add(('dilithium', 'M'))

    initial_state = State(
        elevator_floor=0,
        floors=tuple(frozenset(initial_floors[i]) for i in range(4))
    )

    assert initial_state.is_valid() == True
    print("  ✓ Initial state is valid")

    # Verify each floor
    for i in range(4):
        assert is_safe_floor(initial_state.floors[i])
        print(f"  ✓ Floor {i} is safe ({len(initial_state.floors[i])} items)")
    print()

def test_goal_state_detection():
    """Test 4: Goal state detection with 14 items."""
    print("Test 4: Testing goal state detection...")

    # Create a goal state with all 14 items on floor 3
    goal_floors = (
        frozenset(),
        frozenset(),
        frozenset(),
        frozenset([
            ('elerium', 'G'), ('elerium', 'M'),
            ('dilithium', 'G'), ('dilithium', 'M'),
            ('strontium', 'G'), ('strontium', 'M'),
            ('plutonium', 'G'), ('plutonium', 'M'),
            ('thulium', 'G'), ('thulium', 'M'),
            ('ruthenium', 'G'), ('ruthenium', 'M'),
            ('curium', 'G'), ('curium', 'M')
        ])
    )

    goal_state = State(elevator_floor=3, floors=goal_floors)
    assert goal_state.is_goal() == True
    assert len(goal_state.floors[3]) == 14
    print("  ✓ Goal state correctly identified with 14 items on floor 3")
    print()

def test_move_generation():
    """Test 5: Move generation from initial state."""
    print("Test 5: Testing move generation...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    initial_floors = parse_input(input_text)
    initial_floors[0].add(('elerium', 'G'))
    initial_floors[0].add(('elerium', 'M'))
    initial_floors[0].add(('dilithium', 'G'))
    initial_floors[0].add(('dilithium', 'M'))

    initial_state = State(
        elevator_floor=0,
        floors=tuple(frozenset(initial_floors[i]) for i in range(4))
    )

    valid_moves = generate_valid_moves(initial_state)
    print(f"  Number of valid first moves: {len(valid_moves)}")

    # Verify all moves are valid
    for move in valid_moves:
        assert move.is_valid() == True
    print("  ✓ All generated moves are valid states")

    # Verify moves go to floor 1
    for move in valid_moves:
        assert move.elevator_floor == 1
    print("  ✓ All first moves go to floor 1 (only valid direction)")

    # Check items moved
    initial_count = len(initial_state.floors[0])
    for move in valid_moves:
        items_moved = initial_count - len(move.floors[0])
        assert 1 <= items_moved <= 2
    print("  ✓ All moves carry 1-2 items")
    print()

def test_canonicalization():
    """Test 6: State canonicalization."""
    print("Test 6: Testing state canonicalization...")

    # Case 6a: Equivalent states canonicalize identically
    state1_floors = (
        frozenset([('elerium', 'G'), ('elerium', 'M')]),
        frozenset([('dilithium', 'G'), ('dilithium', 'M')]),
        frozenset(),
        frozenset()
    )
    state1 = State(elevator_floor=0, floors=state1_floors)

    state2_floors = (
        frozenset([('dilithium', 'G'), ('dilithium', 'M')]),
        frozenset([('elerium', 'G'), ('elerium', 'M')]),
        frozenset(),
        frozenset()
    )
    state2 = State(elevator_floor=0, floors=state2_floors)

    canonical1 = canonicalize_state(state1)
    canonical2 = canonicalize_state(state2)
    assert canonical1 == canonical2
    print("  ✓ Equivalent states canonicalize identically")

    # Case 6b: Different states remain different
    state3_floors = (
        frozenset([('elerium', 'G'), ('dilithium', 'M')]),
        frozenset(),
        frozenset(),
        frozenset()
    )
    state3 = State(elevator_floor=0, floors=state3_floors)

    state4_floors = (
        frozenset([('elerium', 'G'), ('elerium', 'M')]),
        frozenset(),
        frozenset(),
        frozenset()
    )
    state4 = State(elevator_floor=0, floors=state4_floors)

    canonical3 = canonicalize_state(state3)
    canonical4 = canonicalize_state(state4)
    assert canonical3 != canonical4
    print("  ✓ Different states remain different after canonicalization")
    print()

def test_solution():
    """Test 7: Solution existence and reasonableness."""
    print("Test 7: Testing solution...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    initial_floors = parse_input(input_text)
    initial_floors[0].add(('elerium', 'G'))
    initial_floors[0].add(('elerium', 'M'))
    initial_floors[0].add(('dilithium', 'G'))
    initial_floors[0].add(('dilithium', 'M'))

    initial_state = State(
        elevator_floor=0,
        floors=tuple(frozenset(initial_floors[i]) for i in range(4))
    )

    min_steps = solve(initial_state)
    print(f"  Minimum steps: {min_steps}")

    # Reasonableness checks
    assert min_steps > 0, "Solution should require at least 1 step"
    print("  ✓ Solution requires at least 1 step")

    assert min_steps > 37, "Part 2 should take more steps than Part 1 (37 steps)"
    print(f"  ✓ Solution ({min_steps}) > Part 1 answer (37)")

    assert min_steps < 200, "Solution should be found in reasonable number of steps"
    print(f"  ✓ Solution ({min_steps}) < 200 (reasonable upper bound)")

    # Run twice to verify determinism
    min_steps_2 = solve(initial_state)
    assert min_steps == min_steps_2, "Solution should be deterministic"
    print("  ✓ Solution is deterministic (same result on second run)")
    print()

    return min_steps

def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Part 2 Solution Verification")
    print("=" * 60)
    print()

    try:
        test_initial_state_setup()
        test_safety_rules()
        test_initial_state_validity()
        test_goal_state_detection()
        test_move_generation()
        test_canonicalization()
        answer = test_solution()

        print("=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print(f"Final Answer: {answer}")
        print()

        return answer

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return None
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    main()
