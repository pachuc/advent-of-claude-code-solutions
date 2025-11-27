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


def verify_guard_minute(filename, target_guard, target_minute):
    """Manually verify the frequency of a specific guard-minute pair"""
    records = parse_input(filename)
    sorted_records = sorted(records, key=lambda x: x[0])

    current_guard = None
    sleep_start = None
    count = 0
    occurrences = []

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

            # Check if target guard and target minute is in range
            if current_guard == target_guard:
                if sleep_start <= target_minute < wake_minute:
                    count += 1
                    occurrences.append(f"  {timestamp.date()} - asleep {sleep_start:02d}-{wake_minute:02d}")

            sleep_start = None

    print(f"Guard #{target_guard} at minute {target_minute}:")
    print(f"Frequency: {count} times")
    print(f"Occurrences:")
    for occ in occurrences:
        print(occ)

    return count


if __name__ == '__main__':
    # Verify the reported answer
    count = verify_guard_minute('input.md', 2789, 34)
    print(f"\nVerification: Guard #2789 was asleep at minute 34 exactly {count} times")
    print(f"Expected from solution: 17 times")
    print(f"Match: {count == 17}")
