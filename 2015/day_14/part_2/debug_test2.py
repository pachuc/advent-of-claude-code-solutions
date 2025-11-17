import solution

def test_state_machine():
    """Test the state machine for Dancer in detail."""
    # Dancer: 27 km/s for 5 seconds, rest 132 seconds

    dancer_data = [('Dancer', 27, 5, 132)]
    reindeer_list = solution.initialize_reindeer(dancer_data)
    dancer = reindeer_list[0]

    print("Testing state transitions for Dancer:")
    print("Expected: Fly seconds 1-5, Rest seconds 6-137, Fly again 138-142, etc.\n")

    # Track the state before and after update
    for second in range(1, 11):
        print(f"Before second {second}: is_flying={dancer['is_flying']}, time_in_state={dancer['time_in_state']}, distance={dancer['distance']}")
        solution.update_reindeer_position(dancer)
        print(f"After second {second}:  is_flying={dancer['is_flying']}, time_in_state={dancer['time_in_state']}, distance={dancer['distance']}\n")

    # The issue might be that after flying for 5 seconds, we transition to resting
    # Let's check what happens at the boundary
    print("\nChecking boundary at second 5:")
    print("After second 5, should transition from flying to resting")
    print("time_in_state should reset to 0 and is_flying should become False")

test_state_machine()
