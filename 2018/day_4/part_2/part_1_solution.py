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


def find_sleepiest_guard(guard_sleep_minutes):
    """Find guard with most total sleep minutes"""
    guard_total_sleep = {}
    for guard_id, sleep_array in guard_sleep_minutes.items():
        guard_total_sleep[guard_id] = sum(sleep_array)

    sleepiest_guard = max(guard_total_sleep, key=guard_total_sleep.get)
    total_minutes = guard_total_sleep[sleepiest_guard]

    return sleepiest_guard, total_minutes


def find_best_minute(guard_sleep_minutes, guard_id):
    """Find minute when guard is asleep most frequently"""
    sleep_array = guard_sleep_minutes[guard_id]
    best_minute = max(range(60), key=lambda m: sleep_array[m])
    frequency = sleep_array[best_minute]

    return best_minute, frequency


def solve(filename='input.md'):
    """Main solution function"""
    # Parse and sort records
    records = parse_input(filename)
    sorted_records = sort_records(records)

    # Track sleep patterns
    guard_sleep_minutes = track_sleep_patterns(sorted_records)

    # Find sleepiest guard
    sleepiest_guard, total_sleep = find_sleepiest_guard(guard_sleep_minutes)

    # Find best minute for sleepiest guard
    best_minute, frequency = find_best_minute(guard_sleep_minutes, sleepiest_guard)

    # Calculate answer
    answer = sleepiest_guard * best_minute

    # Print results
    print(f"Sleepiest Guard: #{sleepiest_guard} ({total_sleep} total minutes asleep)")
    print(f"Most frequent sleep minute: {best_minute} (asleep {frequency} times at this minute)")
    print(f"Answer: {sleepiest_guard} × {best_minute} = {answer}")

    return answer


if __name__ == '__main__':
    solve()
