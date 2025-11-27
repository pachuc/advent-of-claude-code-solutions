import re
from datetime import datetime
from collections import defaultdict

def parse_input(filename):
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

def sort_records(records):
    return sorted(records, key=lambda x: x[0])

def track_sleep_patterns(sorted_records):
    guard_sleep_minutes = defaultdict(lambda: [0] * 60)
    current_guard = None
    sleep_start = None

    for timestamp, event in sorted_records:
        guard_match = re.match(r'Guard #(\d+) begins shift', event)
        if guard_match:
            current_guard = int(guard_match.group(1))
            sleep_start = None
            continue

        if event == 'falls asleep':
            sleep_start = timestamp.minute
            continue

        if event == 'wakes up':
            wake_minute = timestamp.minute
            for minute in range(sleep_start, wake_minute):
                guard_sleep_minutes[current_guard][minute] += 1
            sleep_start = None
            continue

    return guard_sleep_minutes

records = parse_input('input.md')
sorted_records = sort_records(records)
guard_sleep_minutes = track_sleep_patterns(sorted_records)

# Verify Guard #2789 at minute 34
print(f"Guard #2789 was asleep at minute 34: {guard_sleep_minutes[2789][34]} times")
print()

# Find the top 5 most frequent guard-minute pairs
top_pairs = []
for guard_id, sleep_array in guard_sleep_minutes.items():
    for minute in range(60):
        frequency = sleep_array[minute]
        if frequency > 0:
            top_pairs.append((frequency, guard_id, minute))

top_pairs.sort(reverse=True)
print("Top 5 most frequent (guard, minute) pairs:")
for freq, guard_id, minute in top_pairs[:5]:
    print(f"  Guard #{guard_id} at minute {minute}: {freq} times")
