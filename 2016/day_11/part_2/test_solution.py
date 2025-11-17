import re
from solution import parse_input, is_safe_floor, State, generate_valid_moves, canonicalize_state

def test_initial_state():
    """Test that initial state is correctly set up with 4 new items."""
    print("Test 1: Verify Initial State Setup")
    print("=" * 50)

    with open('input.md', 'r') as f:
        input_text = f.read()

    initial_floors = parse_input(input_text)

    # Add the 4 new items to first floor
    initial_floors[0].add(('elerium', 'G'))
    initial_floors[0].add(('elerium', 'M'))
    initial_floors[0].add(('dilithium', 'G'))
    initial_floors[0].add(('dilithium', 'M'))

    print(f"Floor 0 items: {sorted(initial_floors[0])}")
    print(f"Total items on floor 0: {len(initial_floors[0])}")
    print(f"Floor 1 items: {sorted(initial_floors[1])}")
    print(f"Floor 2 items: {sorted(initial_floors[2])}")
    print(f"Floor 3 items: {sorted(initial_floors[3])}")

    # Verify all expected items are present
    expected_floor_0 = {
        ('strontium', 'G'), ('strontium', 'M'),
        ('plutonium', 'G'), ('plutonium', 'M'),
        ('elerium', 'G'), ('elerium', 'M'),
        ('dilithium', 'G'), ('dilithium', 'M')
    }

    assert initial_floors[0] == expected_floor_0, "Floor 0 doesn't have expected items!"
    print("\nPASS: All 8 items correctly on floor 0")
    print()


def test_safety_rules():
    """Test safety rules with new items."""
    print("Test 2: Safety Rule Validation")
    print("=" * 50)

    # Test safe configuration - matching pairs
    test_floor = {('elerium', 'G'), ('elerium', 'M')}
    assert is_safe_floor(test_floor) == True
    print("PASS: Elerium matching pair is safe")

    # Test safe configuration - multiple matching pairs
    test_floor = {('elerium', 'G'), ('elerium', 'M'), ('dilithium', 'G'), ('dilithium', 'M')}
    assert is_safe_floor(test_floor) == True
    print("PASS: Both new pairs together are safe")

    # Test unsafe configuration - unprotected microchip
    test_floor = {('elerium', 'M'), ('dilithium', 'G')}
    assert is_safe_floor(test_floor) == False
    print("PASS: Elerium chip with dilithium generator is unsafe")

    # Test safe configuration - microchips alone
    test_floor = {('elerium', 'M'), ('dilithium', 'M'), ('strontium', 'M'),
                  ('plutonium', 'M'), ('thulium', 'M'), ('ruthenium', 'M'), ('curium', 'M')}
    assert is_safe_floor(test_floor) == True
    print("PASS: All 7 microchips together are safe")
    print()


def test_initial_state_validity():
    """Test that initial state is valid."""
    print("Test 3: Initial State Validity")
    print("=" * 50)

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
    print("PASS: Initial state is valid")
    print()


def test_goal_detection():
    """Test goal state detection with 14 items."""
    print("Test 4: Goal State Detection")
    print("=" * 50)

    # Create a goal state with all 14 items on floor 3
    goal_floors = (
        frozenset(),
        frozenset(),
        frozenset(),
        frozenset([
            ('elerium', 'G'), ('elerium', 'M'), ('dilithium', 'G'), ('dilithium', 'M'),
            ('strontium', 'G'), ('strontium', 'M'), ('plutonium', 'G'), ('plutonium', 'M'),
            ('thulium', 'G'), ('thulium', 'M'), ('ruthenium', 'G'), ('ruthenium', 'M'),
            ('curium', 'G'), ('curium', 'M')
        ])
    )
    goal_state = State(elevator_floor=3, floors=goal_floors)

    assert goal_state.is_goal() == True
    print("PASS: Goal state correctly detected")
    print()


def test_move_generation():
    """Test move generation from initial state."""
    print("Test 5: Move Generation Validation")
    print("=" * 50)

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
    print(f"Number of valid first moves: {len(valid_moves)}")

    # Verify all generated moves are valid
    for move in valid_moves:
        assert move.is_valid() == True, "Generated invalid move!"
    print("PASS: All generated moves are valid")

    # Verify moves are logical (from floor 0 to floor 1)
    for move in valid_moves:
        assert move.elevator_floor == 1, "First move should be to floor 1"
    print("PASS: All first moves go to floor 1")

    # Check that items moved make sense (1-2 items left floor 0)
    initial_count = len(initial_state.floors[0])
    for move in valid_moves:
        items_moved = initial_count - len(move.floors[0])
        assert 1 <= items_moved <= 2, "Should move 1-2 items per move"
    print("PASS: All moves carry 1-2 items")
    print()


def test_canonicalization():
    """Test canonicalization with 7 element pairs."""
    print("Test 6: Canonicalization")
    print("=" * 50)

    # Two states that differ only in element names but have same structure
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

    # These should canonicalize to the same state
    canonical1 = canonicalize_state(state1)
    canonical2 = canonicalize_state(state2)
    assert canonical1 == canonical2
    print("PASS: Equivalent states canonicalize identically")

    # State with split pair vs. matched pair should be different
    state3_floors = (
        frozenset([('elerium', 'G'), ('elerium', 'M')]),
        frozenset(),
        frozenset(),
        frozenset()
    )
    state3 = State(elevator_floor=0, floors=state3_floors)

    canonical3 = canonicalize_state(state3)
    assert canonical1 != canonical3
    print("PASS: Different states remain different after canonicalization")
    print()


if __name__ == '__main__':
    test_initial_state()
    test_safety_rules()
    test_initial_state_validity()
    test_goal_detection()
    test_move_generation()
    test_canonicalization()

    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
