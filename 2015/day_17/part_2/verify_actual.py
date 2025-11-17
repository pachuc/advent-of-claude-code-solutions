from itertools import combinations
from solution import parse_input

# Parse the actual input
containers = parse_input('input.md')
target = 150

print(f"Total containers: {len(containers)}")
print(f"Containers: {containers}")
print(f"Target: {target}\n")

# Find the minimum size by testing each size
min_size = None
for k in range(1, len(containers) + 1):
    count = sum(1 for c in combinations(containers, k) if sum(c) == target)
    print(f"Size {k}: {count} combinations")
    if count > 0:
        min_size = k
        min_count = count
        break

print(f"\nMinimum size: {min_size} containers")
print(f"Count at minimum size: {min_count}")

# Verify no solutions exist at size (min_size - 1)
if min_size and min_size > 1:
    count_smaller = sum(1 for c in combinations(containers, min_size - 1) if sum(c) == target)
    print(f"Count at size {min_size - 1}: {count_smaller} (should be 0)")

# Show a few examples to verify correctness
print(f"\nExample combinations (showing first 5):")
examples = [c for c in combinations(containers, min_size) if sum(c) == target][:5]
for i, ex in enumerate(examples, 1):
    print(f"  {i}. {ex} = {sum(ex)}")
