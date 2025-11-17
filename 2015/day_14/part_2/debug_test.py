import solution

def calculate_distance_formula(speed, fly_time, rest_time, total_time):
    """Calculate distance using mathematical formula for verification."""
    cycle_time = fly_time + rest_time
    complete_cycles = total_time // cycle_time
    remainder = total_time % cycle_time

    distance = complete_cycles * fly_time * speed
    distance += min(remainder, fly_time) * speed

    return distance

def debug_dancer_1000():
    """Debug Dancer's movement for first few cycles."""
    # Dancer: 27 km/s for 5 seconds, rest 132 seconds
    # Cycle = 137 seconds

    dancer_data = [('Dancer', 27, 5, 132)]
    reindeer_list = solution.initialize_reindeer(dancer_data)
    dancer = reindeer_list[0]

    print("Dancer movement analysis:")
    print(f"Speed: {dancer['speed']} km/s")
    print(f"Fly time: {dancer['fly_time']} seconds")
    print(f"Rest time: {dancer['rest_time']} seconds")
    print(f"Cycle length: {dancer['fly_time'] + dancer['rest_time']} seconds\n")

    # Track first 150 seconds
    for second in range(1, 151):
        solution.update_reindeer_position(dancer)

        if second <= 10 or second in [137, 138, 139]:
            print(f"Second {second:3d}: distance={dancer['distance']:4d} km, "
                  f"is_flying={dancer['is_flying']}, time_in_state={dancer['time_in_state']}")

    print(f"\nAt 1000 seconds:")
    # Continue to 1000
    for second in range(151, 1001):
        solution.update_reindeer_position(dancer)

    print(f"Distance: {dancer['distance']} km")

    # Calculate expected distance
    expected = calculate_distance_formula(27, 5, 132, 1000)
    print(f"Expected (formula): {expected} km")

    # Manual calculation
    cycle_time = 5 + 132  # 137
    complete_cycles = 1000 // 137  # 7
    remainder = 1000 % 137  # 41
    flying_in_remainder = min(remainder, 5)  # 5
    manual_distance = complete_cycles * 5 * 27 + flying_in_remainder * 27
    print(f"Manual calculation: {complete_cycles} complete cycles * 5 * 27 + {flying_in_remainder} * 27 = {manual_distance} km")

def debug_comet_1000():
    """Debug Comet's movement."""
    # Comet: 18 km/s for 6 seconds, rest 103 seconds
    # Cycle = 109 seconds

    comet_data = [('Comet', 18, 6, 103)]
    reindeer_list = solution.initialize_reindeer(comet_data)
    comet = reindeer_list[0]

    print("\n\nComet movement analysis:")
    print(f"Speed: {comet['speed']} km/s")
    print(f"Fly time: {comet['fly_time']} seconds")
    print(f"Rest time: {comet['rest_time']} seconds")
    print(f"Cycle length: {comet['fly_time'] + comet['rest_time']} seconds\n")

    # Simulate 1000 seconds
    for second in range(1, 1001):
        solution.update_reindeer_position(comet)

    print(f"At 1000 seconds:")
    print(f"Distance: {comet['distance']} km")

    # Calculate expected distance
    expected = calculate_distance_formula(18, 6, 103, 1000)
    print(f"Expected (formula): {expected} km")

    # Manual calculation
    cycle_time = 6 + 103  # 109
    complete_cycles = 1000 // 109  # 9
    remainder = 1000 % 109  # 19
    flying_in_remainder = min(remainder, 6)  # 6
    manual_distance = complete_cycles * 6 * 18 + flying_in_remainder * 18
    print(f"Manual calculation: {complete_cycles} complete cycles * 6 * 18 + {flying_in_remainder} * 18 = {manual_distance} km")

if __name__ == '__main__':
    debug_dancer_1000()
    debug_comet_1000()
