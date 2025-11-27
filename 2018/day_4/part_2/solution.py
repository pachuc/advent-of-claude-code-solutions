import re
from datetime import datetime
from collections import defaultdict


def parse_input(filename):
    """Parse input file and return list of (datetime, event) tuples"""
    records = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Extract timestamp and event
            match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.+)', line)
            if match:
                timestamp_str = match.group(1)
                event = match.group(2)
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
                records.append((timestamp, event))

    return records


def sort_records(records):
    """Sort records chronologically"""
    return sorted(records, key=lambda x: x[0])


def track_sleep_patterns(sorted_records):
    """Process records and build guard sleep tracking"""
    guard_sleep_minutes = defaultdict(lambda: [0] * 60)

    current_guard = None
    sleep_start = None

    for timestamp, event in sorted_records:
        # Check if guard begins shift
        guard_match = re.match(r'Guard #(\d+) begins shift', event)
        if guard_match:
            current_guard = int(guard_match.group(1))
            sleep_start = None  # Reset sleep state for new guard
            continue

        # Check if falls asleep
        if event == 'falls asleep':
            assert current_guard is not None, "Guard must be on duty before falling asleep"
            assert sleep_start is None, "Guard cannot fall asleep twice without waking"
            sleep_start = timestamp.minute
            continue

        # Check if wakes up
        if event == 'wakes up':
            assert current_guard is not None, "Guard must be on duty before waking up"
            assert sleep_start is not None, "Guard must be asleep before waking up"
            wake_minute = timestamp.minute

            # Mark all minutes from sleep_start (inclusive) to wake_minute (exclusive)
            for minute in range(sleep_start, wake_minute):
                guard_sleep_minutes[current_guard][minute] += 1

            sleep_start = None  # Reset sleep state
            continue

    return guard_sleep_minutes


def find_most_frequent_guard_minute(guard_sleep_minutes):
    """Find the (guard, minute) pair with highest frequency across all guards"""
    max_frequency = 0
    best_guard = None
    best_minute = None

    # Iterate through all guards
    for guard_id, sleep_array in guard_sleep_minutes.items():
        # For this guard, check all 60 minutes
        for minute in range(60):
            frequency = sleep_array[minute]
            # Track the maximum frequency across all combinations
            if frequency > max_frequency:
                max_frequency = frequency
                best_guard = guard_id
                best_minute = minute

    return best_guard, best_minute, max_frequency


def solve(filename='input.md'):
    """Main solution function"""
    # Parse and sort records
    records = parse_input(filename)
    sorted_records = sort_records(records)

    # Track sleep patterns (builds guard_sleep_minutes)
    guard_sleep_minutes = track_sleep_patterns(sorted_records)

    # Find the guard-minute pair with highest frequency
    best_guard, best_minute, max_frequency = find_most_frequent_guard_minute(guard_sleep_minutes)

    # Calculate answer
    answer = best_guard * best_minute

    # Print results
    print(f"Guard #{best_guard} was asleep most frequently at minute {best_minute}")
    print(f"Frequency: asleep {max_frequency} times at this minute")
    print(f"Answer: {best_guard} × {best_minute} = {answer}")

    return answer


if __name__ == '__main__':
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    solve(filename)
