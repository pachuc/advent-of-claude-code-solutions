import re

def parse_input(filename):
    """Parse the input file and extract reindeer data."""
    reindeer_data = []
    pattern = r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.'

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                match = re.match(pattern, line)
                if match:
                    name = match.group(1)
                    speed = int(match.group(2))
                    fly_time = int(match.group(3))
                    rest_time = int(match.group(4))
                    reindeer_data.append((name, speed, fly_time, rest_time))

    return reindeer_data

def initialize_reindeer(parsed_data):
    """Initialize reindeer data structures with starting state."""
    reindeer_list = []
    for name, speed, fly_time, rest_time in parsed_data:
        reindeer = {
            'name': name,
            'speed': speed,
            'fly_time': fly_time,
            'rest_time': rest_time,
            'distance': 0,
            'points': 0,
            'time_in_state': 0,
            'is_flying': True
        }
        reindeer_list.append(reindeer)
    return reindeer_list

def update_reindeer_position(reindeer):
    """Update a single reindeer's position and state."""
    if reindeer['is_flying']:
        # Move forward while flying
        reindeer['distance'] += reindeer['speed']
        reindeer['time_in_state'] += 1

        # Check if we've completed the flying period
        if reindeer['time_in_state'] >= reindeer['fly_time']:
            # Transition to resting
            reindeer['is_flying'] = False
            reindeer['time_in_state'] = 0
    else:  # resting
        # No movement while resting
        reindeer['time_in_state'] += 1

        # Check if we've completed the resting period
        if reindeer['time_in_state'] >= reindeer['rest_time']:
            # Transition to flying
            reindeer['is_flying'] = True
            reindeer['time_in_state'] = 0

def find_leaders(reindeer_list):
    """Find all reindeer with the maximum distance."""
    max_distance = max(r['distance'] for r in reindeer_list)
    leaders = [r for r in reindeer_list if r['distance'] == max_distance]
    return leaders

def simulate_race(reindeer_list, duration):
    """Simulate the race for the specified duration and return max points."""
    for second in range(1, duration + 1):
        # Update all reindeer positions
        for reindeer in reindeer_list:
            update_reindeer_position(reindeer)

        # Find leaders
        leaders = find_leaders(reindeer_list)

        # Award points to leaders
        for leader in leaders:
            leader['points'] += 1

    # Return maximum points
    max_points = max(r['points'] for r in reindeer_list)
    return max_points

def main():
    """Main function to orchestrate the solution."""
    # Parse input
    reindeer_data = parse_input('input.md')
    reindeer_list = initialize_reindeer(reindeer_data)

    # Run simulation for 2503 seconds
    max_points = simulate_race(reindeer_list, 2503)

    # Print result
    print(max_points)

if __name__ == '__main__':
    main()
