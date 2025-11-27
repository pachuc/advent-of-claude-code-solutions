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
            match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.+)', line)
            if match:
                timestamp_str = match.group(1)
                event = match.group(2)
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
                records.append((timestamp, event))
    return records


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
            sleep_start = None
            continue

        # Check if falls asleep
        if event == 'falls asleep':
            sleep_start = timestamp.minute
            continue

        # Check if wakes up
        if event == 'wakes up':
            wake_minute = timestamp.minute
            for minute in range(sleep_start, wake_minute):
                guard_sleep_minutes[current_guard][minute] += 1
            sleep_start = None

    return guard_sleep_minutes


def find_top_frequencies(guard_sleep_minutes, top_n=10):
    """Find top N (guard, minute) pairs by frequency"""
    all_combinations = []

    for guard_id, sleep_array in guard_sleep_minutes.items():
        for minute in range(60):
            frequency = sleep_array[minute]
            if frequency > 0:
                all_combinations.append((frequency, guard_id, minute))

    # Sort by frequency descending
    all_combinations.sort(reverse=True)

    return all_combinations[:top_n]


if __name__ == '__main__':
    records = parse_input('input.md')
    sorted_records = sorted(records, key=lambda x: x[0])
    guard_sleep_minutes = track_sleep_patterns(sorted_records)

    top = find_top_frequencies(guard_sleep_minutes, 10)

    print("Top 10 (guard, minute) pairs by frequency:")
    print("=" * 60)
    for i, (freq, guard, minute) in enumerate(top, 1):
        print(f"{i}. Guard #{guard} at minute {minute}: {freq} times (answer: {guard * minute})")

    print("\n" + "=" * 60)
    print(f"Winner: Guard #{top[0][1]} at minute {top[0][2]}")
    print(f"Answer: {top[0][1]} × {top[0][2]} = {top[0][1] * top[0][2]}")
